from meetingsummariser.summaries.ai_summary_creator import AISummaryCreator
from meetingsummariser.worker import Worker


class SummaryWorker(Worker):
    summary_service: AISummaryCreator

    def __init__(self, summary_service: AISummaryCreator):
        super().__init__()
        self.summary_service = summary_service

    def run(self):
        self.summary_service.summarise_transcription()
