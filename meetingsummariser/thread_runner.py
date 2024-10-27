from PyQt6.QtCore import QObject, QThread, pyqtSignal, pyqtSlot

from meetingsummariser.worker import Worker


class ThreadRunner(QObject):
    finished = pyqtSignal()
    thread: QThread

    def run(self, worker: Worker):
        self.quit_old_thread()

        self.thread = QThread()
        self.worker = worker
        self.worker.finished.connect(self.on_worker_finished)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)

        self.thread.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def quit_old_thread(self):
        if self.thread is None or type(self.thread) is not QThread:
            return

        self.thread.quit()
        self.thread.wait()
        self.thread = None

    @pyqtSlot()
    def on_worker_finished(self):
        self.finished.emit()
        self.quit_old_thread()
