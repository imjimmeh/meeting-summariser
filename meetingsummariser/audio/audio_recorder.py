import logging
import wave
from datetime import datetime

import numpy as np
from pyaudio import PyAudio, paContinue, paInt16

from meetingsummariser.audio.audio_chunk import (
    AddAudioChunkToQueueCallabale,
    AudioChunk,
)
from meetingsummariser.files import Files
from meetingsummariser.options.options_manager import OptionsManager

FORMAT = paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 4096
SILENCE_THRESHOLD = 250
FRAMES_PER_SECOND = 2


class AudioRecorder:
    device_index: int = -1
    frames = []
    silent_frames = 0
    chunk_counter = 0
    add_to_queue: AddAudioChunkToQueueCallabale
    py_audio: PyAudio
    should_record = False
    streaming_task = None
    chunk_started = False
    files: Files
    logger = logging.getLogger(__name__)
    options: OptionsManager

    def __init__(
        self,
        py_audio: PyAudio,
        add_to_queue: AddAudioChunkToQueueCallabale,
        files: Files,
        options: OptionsManager,
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        chunk=CHUNK,
    ):
        self.format = format
        self.channels = channels
        self.rate = rate
        self.chunk = chunk
        self.stream = None
        self.add_to_queue = add_to_queue
        self.py_audio = py_audio
        self.files = files
        self.options = options

    def start_recording(self, device_index):
        if device_index is None:
            raise ValueError("No audio device selected.")

        if device_index != self.device_index:
            self.logger = logging.getLogger(f"{__name__}-{device_index}")

        self.logger.info("Starting recording")
        self.device_index = device_index
        self.start_stream()
        self.on_new_chunk_start()
        self.logger.info("Recording started")

    def start_stream(self):
        self.stream = self.py_audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            input_device_index=self.device_index,
            frames_per_buffer=self.chunk,
            stream_callback=self.stream_callback,
        )

        self.stream.start_stream()

    def stop_recording(self):
        self.logger.info("Stopping recording")
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()

        self.save_audio_chunk()
        self.logger.info("Audio stream closed.")
        self.chunk_counter = 0

    def audio_is_silent(self, data):
        audio_data = np.frombuffer(data, dtype=np.int16)
        amplitude = np.abs(audio_data).mean()
        is_silent = amplitude < SILENCE_THRESHOLD
        return is_silent

    def on_new_chunk_start(self):
        self.logger.info("Initialising new chunk")
        self.chunk_start_time = datetime.now()
        self.frames = []
        self.chunk_started = False
        self.chunk_counter = self.chunk_counter + 1

    def stream_callback(self, data, frame_count, time_info, status):
        """
        Callback function for the audio stream; called whenever new data is available from the audio device.
        Appends data to existing frames, starts a new chunk if silence threshold has been surpassed
        """
        self.frames.append(data)

        is_silent = self.audio_is_silent(data)
        if is_silent:
            self.silent_frames += 1
        else:
            self.silent_frames = 0
            self.chunk_started = True

        if (
            self.silent_frames
            >= self.options.audio_options.silence_threshold_seconds * FRAMES_PER_SECOND
            and self.chunk_started is True
        ):
            self.logger.info("Sielnce exceeds limit; stopping chunk.")
            self.save_audio_chunk()

        return (None, paContinue)

    def save_audio_chunk(self):
        self.logger.info("Saving chunk")
        if len(self.frames) == 0:
            self.logger.info("No audio data to save.")
            return
        elif not self.chunk_started:
            self.logger.info(f"Chunk has no audio; returning")
            return

        filename = self.get_chunk_filename()
        try:
            with wave.open(filename, "wb") as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(self.py_audio.get_sample_size(self.format))
                wf.setframerate(self.rate)
                wf.writeframes(b"".join(self.frames))
            self.logger.info(f"Saved audio chunk to {filename}.")
        except Exception as e:
            self.logger.error(f"Error saving audio chunk: {e}")

        audio_chunk = AudioChunk(filename, self.chunk_start_time, self.device_index)
        self.add_to_queue(audio_chunk)
        self.on_new_chunk_start()

    def get_chunk_filename(self) -> str:
        return self.files.get_output_path(
            f"device_{self.device_index}_audio_chunk_{self.chunk_counter}.wav"
        )
