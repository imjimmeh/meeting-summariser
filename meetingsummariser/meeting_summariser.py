import asyncio
import logging
from threading import Thread
from typing import List

from pyaudio import PyAudio
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

from meetingsummariser.files import Files
from meetingsummariser.models import SummarisationStatus
from meetingsummariser.multiaudio_transcription_service import (
    MultiAudioTranscriptionService,
)
from meetingsummariser.options import OptionsManager
from meetingsummariser.output_writer import OutputWriter
from meetingsummariser.summaries import AISummaryCreator

from .summaries.summary_worker import SummaryWorker
from .thread_runner import ThreadRunner


class MeetingSummariser(QObject):
    """
    Runs the main process of starting audio recorders + transcription, upon transcription complete gets summary, fires summary event.
    """

    logger = logging.getLogger(__name__)
    audio_service: MultiAudioTranscriptionService
    device_indicies: List[int] = []
    summary_creator: AISummaryCreator
    output_writer: OutputWriter
    options: OptionsManager
    files: Files
    loop: asyncio.AbstractEventLoop
    status: SummarisationStatus = SummarisationStatus.NOT_STARTED
    pyaudio_instance: PyAudio
    thread: Thread | None = None
    transcription = ""
    summary = ""

    status_change = pyqtSignal(SummarisationStatus)

    def __init__(
        self,
        py_audio: PyAudio,
        options: OptionsManager,
        files: Files,
        loop: asyncio.AbstractEventLoop,
    ):
        super().__init__()
        self.pyaudio_instance = py_audio
        self.options = options
        self.files = files
        self.loop = loop
        self.output_writer = OutputWriter(files)

        self.summary_creator = AISummaryCreator(self.options, self.loop)
        self.summary_creator.summary_finished.connect(self.on_summary_finished)

        self.summary_thread_runner = ThreadRunner()

    def create_audio_service(self):
        self.logger.info("Creating audio service")
        self.audio_service = MultiAudioTranscriptionService(
            self.pyaudio_instance, self.files, self.options
        )
        self.audio_service.initialise_services()
        self.audio_service.finished.connect(self.on_transcription_finished)
        self.audio_service.transcription_service.transcription_updated.connect(
            self.on_transcription_changed
        )
        self.logger.info("Created audio service")

    def stop_recording(self):
        if self.audio_service:
            self.audio_service.stop()
            self.on_status_change(SummarisationStatus.FINISHING_RECORDING)
        else:
            self.logger.info(
                "Stop recording was requested but no audio service was found"
            )

    def init_thread(self, device_indices: List[int]):
        self.logger.info("Starting meeting summarisation thread")
        self.audio_service.create_recorders(device_indices)
        self.run()

    def run(self):
        self.summary = ""
        self.transcription = ""
        self.logger.info("Starting meeting summarisation flow")
        self.on_status_change(SummarisationStatus.RECORDING_AND_TRANSCRIBING)
        self.audio_service.run()

    def on_transcription_finished(self):
        if self.transcription is None or self.transcription == "":
            self.on_summary_finished("")
            self.logger.info("Empty transcription - returning")
            return

        self.logger.info(
            "Finished recording and transcribing; moving on to summary creation"
        )
        self.output_writer.write_transcript(self.transcription)
        self.create_meeting_summary()

    def create_meeting_summary(self):
        self.on_status_change(SummarisationStatus.SUMMARISING)
        if self.transcription is None or self.transcription == "":
            self.logger.info("Empty transcript. Skipping summarisation")
            return

        summary_worker = SummaryWorker(self.summary_creator)
        self.summary_creator.set_transcription(self.transcription)
        self.summary_thread_runner.run(summary_worker)

    def on_transcription_changed(self, transcription: str) -> None:
        self.transcription = transcription

    def on_summary_finished(self, summary: str) -> None:
        self.on_status_change(SummarisationStatus.FINISHED)

        if not isinstance(summary, str):
            self.logger.error(
                f"Summary was not a string. Received {type(summary).__name__}"
            )
            return

        self.summary = summary if summary is not None else ""
        if summary is None or summary == "":
            self.logger.error("Received empty summary")
            return

        self.output_writer.write_summary(summary)

    @pyqtSlot()
    def on_status_change(self, status: SummarisationStatus):
        self.status = status
        self.status_change.emit(self.status)
