from PyQt6.QtWidgets import QTextEdit, QWidget

from meetingsummariser.gui.shared import TextBoxWithLabel
from meetingsummariser.options import OptionsManager


class ContextBox(TextBoxWithLabel):
    """
    Textbox for adding context to the AI summary requests
    """

    options: OptionsManager

    def __init__(
        self,
        options: OptionsManager,
        parent: QWidget = None,
        width: int = 50,
        height: int = 10,
    ):
        super().__init__(
            parent,
            label="Summarisation context",
            width=width,
            height=height,
            read_only=False,
        )
        self.options = options
        self.text_box.focusOutEvent = self.on_focus_out
        self.text_box.setToolTip(
            "Provide context to the AI for the summarisation - optional."
        )

    def on_focus_out(self, event):
        self.update_context()
        QTextEdit.focusOutEvent(self.text_box, event)

    def update_context(self):
        self.options.ai_options.prompts.meeting_context = self.get_text_box_value()

    def get_text_box_value(self):
        return self.text_box.toPlainText()
