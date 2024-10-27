from PyQt6.QtWidgets import (
    QFrame,
    QLayout,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class CollapsibleFrame(QFrame):
    """
    A frame with a button that shows/hides the inner widgets
    """

    showing: bool = True
    toggle_button: QPushButton
    parent: QWidget
    parent_layout: QLayout

    def __init__(
        self, parent: QWidget, parent_layout: QLayout, create_button: bool = True
    ):
        self.parent = parent
        self.parent_layout = parent_layout

        if create_button:
            self.create_toggle_button()

        super(CollapsibleFrame, self).__init__(parent)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.size_policy = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.setSizePolicy(self.size_policy)
        self._activate()

    def _activate(self):
        if not self.showing:
            self.hide()
            self.on_hiding()
        else:
            self.show()
            self.on_showing()

    def create_toggle_button(self):
        self.toggle_button = QPushButton("Toggle", self.parent)
        self.toggle_button.clicked.connect(self.toggle)
        self.parent_layout.addWidget(self.toggle_button)

    def toggle(self):
        self.showing = not self.showing
        self._activate()

    def on_showing(self):
        pass

    def on_hiding(self):
        pass
