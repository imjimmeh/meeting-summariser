from meetingsummariser.gui.shared import UpdatableTextBox


class TranscriptBox(UpdatableTextBox):
    def __init__(self, root):
        super().__init__(root, "Transcript")

    def update_transcript(self, transcription: str):
        self.set_text(transcription)
