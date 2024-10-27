import logging

from pydantic import BaseModel
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import (
    QComboBox,
    QLabel,
    QLayout,
    QLineEdit,
    QSizePolicy,
    QTextEdit,
    QWidget,
)

from meetingsummariser.gui.shared import CollapsibleFrame
from meetingsummariser.gui.shared.clickable_label import ClickableLabel
from meetingsummariser.gui.shared.styles import header_label
from meetingsummariser.options import OptionsManager

class OptionsSection(CollapsibleFrame):
    options: OptionsManager
    logger = logging.getLogger(__name__)

    saved = pyqtSignal()

    def __init__(
        self,
        parent: QWidget,
        parent_layout: QLayout,
        options: OptionsManager,
        header: str,
    ):
        super().__init__(parent, parent_layout, False)
        self.options = options
        self.create_header(header)
        self.size_policy = QSizePolicy(
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum
        )
        self.setSizePolicy(self.size_policy)

    def create_header(self, header: str):
        label = ClickableLabel(header, self.parent)
        label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        label.setStyleSheet(header_label)
        label.clicked.connect(self.toggle)
        self.parent_layout.addWidget(label)

    def on_var_change(self, variable, parent_object: BaseModel, object_key: str, var_type: str = "str"):
        value = variable.text()

        if var_type != "str":
            try:
                value = float(value) if var_type == "float" else int(value)
            except Exception as e:
                self.logger.info(f"Could not convert {value} to {var_type}")
                return

        setattr(parent_object, object_key, value)
        self.saved.emit()

    def create_option_widget(
        self,
        label_text: str,
        widget_type: str,
        parent_object: BaseModel,
        object_key: str,
        values=None,
        helper_label_text: str | None = None,
        var_type: str = "str"
    ):
        label = QLabel(label_text, self)
        self.layout.addWidget(label)

        created_widget = self.create_editor_widget(label_text, widget_type, parent_object, object_key, values, var_type=var_type)

        if not created_widget or helper_label_text is None:
            return

        helper_label = QLabel(helper_label_text)
        helper_label.setWordWrap(True)
        helper_label.setStyleSheet("font-size: 12px;")
        self.layout.addWidget(helper_label)

    #Todo: Change widget type to actual class. Or just split into separate methods
    def create_editor_widget(self, label_text: str, widget_type: str, parent_object: BaseModel, object_key: str, values=None, var_type: str = "str") -> bool:
        match widget_type:
            case "QLineEdit":
                input_field = QLineEdit(self)
                input_field.setText(str(getattr(parent_object, object_key)))
                input_field.textChanged.connect(
                    lambda: self.on_var_change(input_field, parent_object, object_key, var_type=var_type)
                )
                self.layout.addWidget(input_field)
                return True
            case "QComboBox":
                combo_box = QComboBox(self)
                combo_box.addItems(values)
                combo_box.setCurrentText(getattr(parent_object, object_key))
                combo_box.currentTextChanged.connect(
                    lambda: self.on_var_change(combo_box, parent_object, object_key, var_type=var_type)
                )
                self.layout.addWidget(combo_box)
                return True
            case _:
                self.logger.error(f"Unsupported widget type '{widget_type}'")
                return False

    def create_label_and_text(self, label_text, text_value):
        label = QLabel(label_text, self)
        self.layout.addWidget(label)

        text_widget = QTextEdit(self)
        text_widget.setPlainText(text_value)
        self.layout.addWidget(text_widget)

        return text_widget

    def on_save(self):
        pass
