from PyQt6.QtWidgets import QLayout, QWidget

from meetingsummariser.gui.options.options_section import OptionsSection
from meetingsummariser.options import OptionsManager


class SummaryOptionsGUI(OptionsSection):
    def __init__(
        self, parent: QWidget, parent_layout: QLayout, options: OptionsManager
    ):
        super().__init__(parent, parent_layout, options, "Summary Options")
        self.add_options()

    def add_options(self):
        self.create_option_widget(
            "Sentences per summary",
            "QLineEdit",
            self.options.summary_options,
            "sentences_per_paragraph",
            var_type="int"
        )
        self.create_option_widget(
            "Summaries per aggregate",
            "QLineEdit",
            self.options.summary_options,
            "summaries_per_aggregate",
            var_type="int"
        )
