from meetingsummariser.gui.shared.updatable_textbox import UpdatableTextBox


class SummaryBox(UpdatableTextBox):
    def __init__(self, root):
        super().__init__(root, "Summary")

    def update_summary(self, summary: str):
        self.set_text(summary)
