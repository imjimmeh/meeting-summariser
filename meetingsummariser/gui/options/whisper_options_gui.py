from PyQt6.QtWidgets import QLayout, QWidget

from meetingsummariser.gui.options.options_section import OptionsSection
from meetingsummariser.options import OptionsManager, available_whisper_models


class WhisperOptionsGUI(OptionsSection):
    def __init__(
        self, parent: QWidget, parent_layout: QLayout, options: OptionsManager
    ):
        super().__init__(parent, parent_layout, options, "Whisper Options")
        self.add_options()

    def add_options(self):
        self.create_option_widget(
            "Model",
            "QComboBox",
            self.options.whisper_options,
            "model",
            available_whisper_models,
        )
