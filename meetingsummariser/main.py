import logging

from PyQt6.QtWidgets import QApplication

from meetingsummariser.gui import AudioTranscriberGUI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    import sys

    app = QApplication(sys.argv)
    gui = AudioTranscriberGUI()
    gui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
