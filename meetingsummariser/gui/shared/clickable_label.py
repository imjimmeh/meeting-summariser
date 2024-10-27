from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QLabel


class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def mousePressEvent(self, ev):
        self.clicked.emit()
