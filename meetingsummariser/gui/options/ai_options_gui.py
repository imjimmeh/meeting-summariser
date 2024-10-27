from PyQt6.QtWidgets import QLayout, QWidget

from meetingsummariser.gui.options.options_section import OptionsSection
from meetingsummariser.options import OptionsManager

class AIOptionsGUI(OptionsSection):
    def __init__(
        self, parent: QWidget, parent_layout: QLayout, options: OptionsManager
    ):
        super().__init__(parent, parent_layout, options, "AI Options")
        self.add_options()

    def add_options(self):
        self.create_option_widget(
            "Model", "QLineEdit", self.options.ai_options, "model"
        )
        self.create_option_widget("OpenAI Compatible URL", "QLineEdit", self.options.ai_options, "url")
        self.create_option_widget(
            "Temperature",
            "QLineEdit",
            self.options.ai_options,
            "temperature",
            var_type="float"
        )
