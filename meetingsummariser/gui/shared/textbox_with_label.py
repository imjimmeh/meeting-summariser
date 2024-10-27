from PyQt6.QtWidgets import QLabel, QTextEdit, QVBoxLayout, QWidget

from meetingsummariser.gui.shared.styles import header_label


class TextBoxWithLabel(QWidget):
    width: int = 50
    height: int = 10
    read_only: bool = True

    def __init__(
        self,
        parent=None,
        label: str = "",
        width: int = 50,
        height: int = 12,
        read_only: bool = True,
    ):
        super().__init__(parent)

        self.width = width
        self.height = height
        self.read_only = read_only

        self.layout = QVBoxLayout()
        self.create_label(text=label)
        self.create_display()

        self.setLayout(self.layout)

    def create_label(self, text: str):
        self.label = QLabel(text)
        self.layout.addWidget(self.label)
        self.label.setStyleSheet(header_label)

    def create_display(self):
        self.text_box = QTextEdit()
        self.text_box.setFixedHeight(self.height * 20)
        self.text_box.setFixedWidth(self.width * 10)
        self.text_box.setReadOnly(self.read_only)
        self.layout.addWidget(self.text_box)
