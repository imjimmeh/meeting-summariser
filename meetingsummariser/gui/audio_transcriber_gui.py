import asyncio
import logging
from typing import List

from pyaudio import PyAudio
from PyQt6.QtCore import QTimer, pyqtSlot
from PyQt6.QtWidgets import QLabel, QMessageBox, QPushButton, QVBoxLayout, QWidget

from meetingsummariser.files import Files
from meetingsummariser.gui.main import (
    ContextBox,
    DeviceSelection,
    OptionsButton,
    SummaryBox,
    TranscriptBox,
)
from meetingsummariser.meeting_summariser import MeetingSummariser
from meetingsummariser.models import SummarisationStatus
from meetingsummariser.options import OptionsManager
from meetingsummariser.output_writer import OutputWriter


class AudioTranscriberGUI(QWidget):
    """
    Class for the main app screen
    """

    meeting_summariser: MeetingSummariser
    device_indices: List[int] = []
    options_visible = False
    pyaudio_instance: PyAudio
    start_recording_text = "Start"
    transcription = None
    summary = None
    output_writer: OutputWriter
    options: OptionsManager
    files: Files
    logger = logging.getLogger(__name__)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Audio Recorder & Transcription")
        self.setGeometry(100, 100, 400, 650)

        self.pyaudio_instance = PyAudio()
        self.files = Files()
        self.options = OptionsManager(self.files)
        self.device_indices = []

        self.create_ui_components()
        self.setup_event_loop_and_subscriptions()

    def create_start_button(self):
        self.start_button = QPushButton(self.start_recording_text)
        self.start_button.clicked.connect(self.toggle_recording)
        self.layout.addWidget(self.start_button)

    def create_status_labels(self):
        self.status_label = QLabel("Ready to record")
        self.layout.addWidget(self.status_label)

        self.queue_label = QLabel("Audio queue length: 0")
        self.layout.addWidget(self.queue_label)

        self.detail_status_label = QLabel("")
        self.layout.addWidget(self.detail_status_label)

    def create_text_boxes(self):
        self.context_box = ContextBox(self.options, self)
        self.transcription_display = TranscriptBox(self)
        self.summary_display = SummaryBox(self)
        self.layout.addWidget(self.context_box)
        self.layout.addWidget(self.transcription_display)
        self.layout.addWidget(self.summary_display)

    def create_ui_components(self):
        self.layout = QVBoxLayout()
        self.device_selection = DeviceSelection(
            self, self.layout, self.pyaudio_instance
        )
        self.layout.addWidget(self.device_selection)

        self.create_start_button()
        self.create_status_labels()
        self.create_text_boxes()

        self.options_button = OptionsButton(self, self.options)
        self.layout.addWidget(self.options_button)

        self.setLayout(self.layout)

    def setup_event_loop_and_subscriptions(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.meeting_summariser = MeetingSummariser(
            self.pyaudio_instance, self.options, self.files, self.loop
        )
        self.meeting_summariser.create_audio_service()
        self.meeting_summariser.summary_creator.summary_finished.connect(
            self.summary_display.update_summary
        )
        self.meeting_summariser.audio_service.transcription_service.transcription_updated.connect(
            self.transcription_display.update_transcript
        )
        self.meeting_summariser.status_change.connect(self.on_status_change)

    @pyqtSlot()
    def toggle_recording(self):
        device_indices = self.device_selection.get_selected_device_indices()
        if not device_indices:
            QMessageBox.critical(self, "Error", "Please select at least one device.")
            return

        if self.meeting_summariser.status in [
            SummarisationStatus.RECORDING_AND_TRANSCRIBING,
            SummarisationStatus.SUMMARISING,
        ]:
            self.stop_recording()
        else:
            self.start_recording(device_indices)

    def start_recording(self, device_indices: List[int]):
        self.transcription_display.reset()
        self.summary_display.reset()

        self.logger.info("Starting recording")
        self.update_button_text("Stop")
        self.status_label.setText("Recording and transcription started.")
        self.meeting_summariser.init_thread(device_indices)
        self.start_label_update_timer()

    def stop_recording(self):
        self.logger.info("Stopping recording")
        self.meeting_summariser.stop_recording()
        self.update_button_text(self.start_recording_text)

    def update_button_text(self, text: str):
        self.start_button.setText(text)

    def on_status_change(self, status: SummarisationStatus):
        match status:
            case SummarisationStatus.RECORDING_AND_TRANSCRIBING:
                label = "Recording and transcribing audio."
            case SummarisationStatus.FINISHING_RECORDING:
                label = "Finishing recording and transcribing remaining audio."
            case SummarisationStatus.SUMMARISING:
                label = "Creating meeting summary."
            case _:
                label = "Finished"

        self.status_label.setText(label)

    def start_label_update_timer(self):
        self.queue_timer = QTimer(self)
        self.queue_timer.timeout.connect(self.update_status_labels)
        self.queue_timer.start(150)

    @pyqtSlot()
    def update_status_labels(self):
        queue_size = self.meeting_summariser.audio_service.get_queue_count()
        self.queue_label.setText(f"Audio queue length: {queue_size}")
        detail_status_label_text = ""

        currently_transcribing = (
            self.meeting_summariser.audio_service.transcription_service.currently_transcribing
            and (
                self.meeting_summariser.status
                == SummarisationStatus.RECORDING_AND_TRANSCRIBING
                or self.meeting_summariser.status
                == SummarisationStatus.FINISHING_RECORDING
            )
        )
        if currently_transcribing:
            detail_status_label_text = "Currently transcribing audio"
        elif self.meeting_summariser.status == SummarisationStatus.SUMMARISING:
            detail_status_label_text = self.meeting_summariser.summary_creator.status

        self.detail_status_label.setText(detail_status_label_text)
