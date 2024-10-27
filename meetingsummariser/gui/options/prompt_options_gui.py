from PyQt6.QtWidgets import QLayout, QWidget

from meetingsummariser.gui.options.options_section import OptionsSection
from meetingsummariser.options import OptionsManager


class PromptOptionsGUI(OptionsSection):
    def __init__(
        self, parent: QWidget, parent_layout: QLayout, options: OptionsManager
    ):
        super().__init__(parent, parent_layout, options, "Prompts")
        self.add_options()

    def add_options(self):
        self.summarise_paragraphs_prompt_input = self.create_label_and_text(
            "Summarise Paragraphs:",
            self.options.ai_options.prompts.summarise_paragraphs,
        )
        self.aggregate_summaries_prompt_input = self.create_label_and_text(
            "Aggregate Summaries:", self.options.ai_options.prompts.aggregate_summaries
        )
        self.final_output_prompt_input = self.create_label_and_text(
            "Final Output:", self.options.ai_options.prompts.final_output
        )

    def update_prompt_option(self, prompt_attr, text_widget):
        setattr(self.options.ai_options.prompts, prompt_attr, text_widget.toPlainText())

    def update_prompt_options(self):
        self.update_prompt_option(
            "summarise_paragraphs", self.summarise_paragraphs_prompt_input
        )
        self.update_prompt_option(
            "aggregate_summaries", self.aggregate_summaries_prompt_input
        )
        self.update_prompt_option("final_output", self.final_output_prompt_input)

    def on_save(self):
        self.update_prompt_options()