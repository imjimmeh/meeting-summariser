import asyncio
import logging
from typing import List

from pyaudio import PyAudio
from PyQt6.QtCore import QObject, pyqtSignal

from meetingsummariser.audio import AudioChunk, AudioRecorder
from meetingsummariser.files import Files
from meetingsummariser.options import OptionsManager
from meetingsummariser.thread_runner import ThreadRunner
from meetingsummariser.transcriptions import TranscriptionService, WhisperService
from meetingsummariser.transcriptions.transcription_worker import TranscriptionWorker


class MultiAudioTranscriptionService(QObject):
    """
    Responsible for directly managing audio recorders + transcription service
    """

    chunk_queue: asyncio.Queue
    files: Files
    options: OptionsManager
    py_audio: PyAudio
    transcription_service: TranscriptionService
    whisper: WhisperService

    cancellation_requested = False
    logger = logging.getLogger(__name__)

    finished = pyqtSignal()

    def __init__(
        self,
        py_audio: PyAudio,
        files: Files,
        options: OptionsManager,
    ):
        super().__init__()
        self.py_audio = py_audio
        self.files = files
        self.options = options
        self.thread_runner = ThreadRunner()
        self.thread_runner.finished.connect(lambda: self.finished.emit())

    def initialise_services(self):
        self.logger.info("initialising services")
        self.whisper = WhisperService(self.options)
        self.transcription_service = TranscriptionService(self.whisper)
        self.chunk_queue = asyncio.Queue()
        self.logger.info("Initialised services")

    def create_recorders(self, device_indices: List[int]):
        self.device_indices = device_indices
        self.audio_recorders = {
            device: AudioRecorder(
                self.py_audio, self.add_to_queue, self.files, self.options
            )
            for device in device_indices
        }

    def add_to_queue(self, audio_chunk: AudioChunk):
        self.logger.info(f"Add to queue - {audio_chunk.filename}")
        self.chunk_queue.put_nowait(audio_chunk)

    def start_recorders(self):
        self.logger.info(f"Starting processes for {len(self.device_indices)} devices")
        for device_index in self.device_indices:
            self.logger.info(f"Starting process for {device_index}")
            recorder = self.audio_recorders[device_index]
            recorder.start_recording(device_index)

    def run(self):
        """Start tasks for recording and transcribing on all selected devices."""
        self.logger.info(f"Starting processes for {len(self.device_indices)} devices")
        self.start_recorders()
        self.transcription_worker = TranscriptionWorker(
            self.transcription_service, self.chunk_queue
        )
        self.thread_runner.run(self.transcription_worker)

    def stop(self):
        for device_index in self.device_indices:
            recorder = self.audio_recorders[device_index]
            recorder.stop_recording()

        self.transcription_service.request_cancellation()

    def get_queue_count(self) -> int:
        return self.chunk_queue.qsize()
