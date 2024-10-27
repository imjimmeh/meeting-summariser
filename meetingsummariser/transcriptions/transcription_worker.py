from asyncio import Queue

from meetingsummariser.transcriptions.transcription_service import TranscriptionService
from meetingsummariser.worker import Worker


class TranscriptionWorker(Worker):
    transcription_service: TranscriptionService
    chunk_queue: Queue

    def __init__(self, transcription_service: TranscriptionService, chunk_queue: Queue):
        super().__init__()
        self.chunk_queue = chunk_queue
        self.transcription_service = transcription_service

    def run(self):
        self.transcription_service.start_transcription(self.chunk_queue)
        self.finished.emit()
        print("Transcription worker emitted finsihed")
