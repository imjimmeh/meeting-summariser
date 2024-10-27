from PyQt6.QtWidgets import QDialog, QPushButton, QVBoxLayout, QWidget

from meetingsummariser.gui.options_gui import OptionsGUI
from meetingsummariser.options import OptionsManager


class OptionsButton(QWidget):
    """
    Shows the options screen
    """

    def __init__(self, parent: QWidget, options: OptionsManager):
        super().__init__(parent)
        self.options = options
        self.create_options_button()

    def create_options_button(self):
        layout = QVBoxLayout()

        self.show_options_button = QPushButton("Options", self)
        self.show_options_button.clicked.connect(self.show_options)

        self.setLayout(layout)

    def show_options(self):
        editor_menu = QDialog(self)
        editor = OptionsGUI(editor_menu, self.options)

        editor_menu.setWindowTitle("Options")
        editor_menu.exec()
