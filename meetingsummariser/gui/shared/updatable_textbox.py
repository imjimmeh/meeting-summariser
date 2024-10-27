from PyQt6.QtGui import QTextCursor

from .textbox_with_label import TextBoxWithLabel


class UpdatableTextBox(TextBoxWithLabel):
    def __init__(self, parent=None, label: str = "", width: int = 50, height: int = 10):
        super().__init__(parent, label, width, height)
        self.text = ""
        self.label = label

    def reset(self):
        self.set_text("")

    def set_text(self, text: str):
        self.text = text
        self.update_display()

    def update_display(self):
        self.text_box.clear()
        self.text_box.setPlainText(self.text)
        self.text_box.moveCursor(QTextCursor.MoveOperation.End)

    def on_main_event(self, status: str):
        if status == "Starting":
            self.reset()
