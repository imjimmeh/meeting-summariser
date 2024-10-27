from PyQt6.QtCore import QObject, pyqtSignal


class Worker(QObject):
    finished = pyqtSignal()
