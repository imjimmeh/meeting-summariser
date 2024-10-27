from PyQt6.QtWidgets import QLayout, QWidget, QLabel

from meetingsummariser.gui.options.options_section import OptionsSection
from meetingsummariser.options import OptionsManager

class AudioOptionsGUI(OptionsSection):
    def __init__(
        self, parent: QWidget, parent_layout: QLayout, options: OptionsManager
    ):
        super().__init__(parent, parent_layout, options, "Audio Options")
        self.add_options()

    def add_options(self):
        self.create_option_widget(
            "no_speech_prob silence threshold", "QLineEdit", self.options.audio_options, "no_speech_prob_silence_threshold",  var_type="float"
        )
        self.create_option_widget(
            "avg_logprob silence threshold", "QLineEdit", self.options.audio_options, "avg_logprob_silence_threshold",var_type="float", helper_label_text="A transcription chunk is determined to be wrong, and therefore dropped, if the no_speech_prob > no_speech_prob_silence_threshold AND avg_logprob < avg_logprob_silence_threshold"
        )

        self.create_option_widget(
            "Seconds silence threshold", "QLineEdit", self.options.audio_options, "silence_threshold_seconds", var_type="float", helper_label_text="How many seconds of silence should exist before the current audio chunk is stopped, and a new one started"
        )
