import logging
from typing import List

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QPushButton, QSizePolicy, QVBoxLayout, QWidget, QScrollArea, QGroupBox, QFormLayout

from meetingsummariser.gui.options import AIOptionsGUI, AudioOptionsGUI, PromptOptionsGUI, SummaryOptionsGUI, WhisperOptionsGUI, OptionsSection
from meetingsummariser.options import OptionsManager


class OptionsGUI(QWidget):
    """
    GUI for options menu
    """

    sections: List[OptionsSection] = []
    logger = logging.getLogger(__name__)

    options_classes = [
        WhisperOptionsGUI,
        AIOptionsGUI,
        SummaryOptionsGUI,
        PromptOptionsGUI,
        AudioOptionsGUI
    ]

    def __init__(self, parent: QWidget, options: OptionsManager):
        super().__init__(parent)
        self.options = options
        self.setWindowTitle("Options")

        self.container_widget = QWidget()
        self.scroll_layout = QVBoxLayout()
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.create_all_options()
        self.create_save_button()
        self.configure_scroll()

    def configure_scroll(self):
        self.container_widget.setLayout(self.scroll_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.container_widget)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFixedHeight(1024)

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.addWidget(self.scroll_area)

        self.size_policy = QSizePolicy(
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum
        )
        self.setSizePolicy(self.size_policy)
        self.container_widget.setSizePolicy(self.size_policy)
        self.scroll_area.adjustSize()
        self.adjustSize()

    def load(self):
        self.options.load()

    def create_all_options(self):
        for options_class in self.options_classes:
            options_instance = options_class(self, self.scroll_layout, self.options)
            self.scroll_layout.addWidget(options_instance)
            self.sections.append(options_instance)
            options_instance.saved.connect(self.save_options)

    def create_save_button(self):
        self.save_button = QPushButton("Save", self)
        self.save_button.clicked.connect(self.save_options)
        self.scroll_layout.addWidget(self.save_button)

    def save_options(self):
        for section in self.sections:
            section.on_save()

        self.options.save()
        self.logger.info("Options saved")
