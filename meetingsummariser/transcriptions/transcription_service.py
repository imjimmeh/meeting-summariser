import logging
import os
import time
from asyncio import Queue
from typing import List

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

from meetingsummariser.audio import AudioChunk
from meetingsummariser.models.segment import Segment
from meetingsummariser.transcriptions.whisper_service import WhisperService


class TranscriptionService(QObject):
    whisper: WhisperService
    is_running = False
    cancellation_requested = False
    transcription: str
    logger = logging.getLogger(__name__)
    transcription_results = []

    transcription_updated = pyqtSignal(str)

    currently_transcribing = False

    def __init__(self, whisper: WhisperService):
        super().__init__()
        self.transcription_results = []
        self.whisper = whisper

    def transcribe_audio_local(self, audio_chunk: AudioChunk) -> List[Segment]:
        segments = self.whisper.transcribe_segments(audio_chunk.filename)
        return segments

    def transcribe_and_save(self, audio_chunk: AudioChunk):
        segments = self.transcribe_audio_local(audio_chunk)
        os.remove(audio_chunk.filename)
        if segments:
            audio_chunk.add_transcriptions(segments)
            self.transcription_results.append(audio_chunk)
            return self.merge_transcriptions()
        else:
            self.logger.warning("No transcription available for appending.")
            return None

    def merge_transcriptions(self) -> str:
        """
        Merges the existing Segments from the AudioChunks in the transcription_results list,
        and combines a combined transcript of the transcription so far.

        Has very basic formatting; adds a new line if:
        - The device index changed from the last audio chunk
        - There is a period of silence of greater than 5 seconds between the two segments
        """
        all_segments = [
            (chunk, segment)
            for chunk in self.transcription_results
            for segment in chunk.segments
        ]
        sorted_segments = sorted(all_segments, key=lambda x: x[1].start)

        merged_text = ""
        last_device_index = None
        last_end_time = None

        for chunk, segment in sorted_segments:
            if (
                last_device_index is not None
                and chunk.device_index != last_device_index
            ) or (
                last_end_time is not None
                and (segment.start - last_end_time).total_seconds() > 5
            ):
                merged_text += "\n"

            merged_text += f"{segment.text} "

            last_device_index = chunk.device_index
            last_end_time = segment.end

        return merged_text.strip()

    def process_chunk(self, chunk_queue: Queue):
        self.logger.info("Processing chunk from queue")
        audio_chunk = chunk_queue.get_nowait()
        self.logger.info(
            f"Received chunk {audio_chunk.filename} starting at {audio_chunk.start_time}"
        )
        self.currently_transcribing = True
        transcription = self.transcribe_and_save(audio_chunk)
        self.currently_transcribing = False
        self.logger.info("Received merged transcription")
        self.logger.info(transcription)
        if transcription is not None:
            self.transcription_updated_event(transcription=transcription)
        return transcription

    def try_get_from_queue(self, chunk_queue):
        """
        Tries get an item from the queue and processes if existing.
        Returns true/false of whether we should continue processing the queue or not
        """
        should_continue = True
        if not chunk_queue.empty():
            self.process_chunk(chunk_queue)
            return True

        stop_requested = not self.is_running and self.cancellation_requested is False

        if stop_requested:
            self.logger.info("Cancellation requested - cancelling chunk transcribing")
            self.cancellation_requested = True
            return True

        is_stopping = not self.is_running and self.cancellation_requested
        if is_stopping:
            if chunk_queue.empty():
                self.logger.info("Queue finished - finished transcribing task")
                should_continue = False
            else:
                self.logger.info("Cancellation requested but queue not empty")

        return should_continue

    def start_transcription(self, chunk_queue: Queue) -> str:
        """Task to process and transcribe chunks from a specific device."""
        self.is_running = True
        self.transcription_results = []

        have_finished = False
        while True:
            should_continue = self.try_get_from_queue(chunk_queue)
            if should_continue is False and have_finished is False:
                have_finished = True
                time.sleep(3)
            elif should_continue is False and have_finished is True:
                break

            time.sleep(0.25)

    def request_cancellation(self):
        self.is_running = False

    @pyqtSlot()
    def transcription_updated_event(self, transcription: str) -> None:
        self.transcription = transcription
        self.transcription_updated.emit(self.transcription)
