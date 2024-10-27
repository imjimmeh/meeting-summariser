import logging
from datetime import UTC, datetime

from meetingsummariser.files import Files


class OutputWriter:
    """
    Handles saving transcripts + summaries
    """

    transcript_filename = "transcript-"
    summary_filename = "summary-"

    files: Files

    logger = logging.getLogger(__name__)

    def __init__(self, files: Files):
        self.files = files

    def write_transcript(self, transcript: str) -> None:
        self.logger.info("Writing transcript")
        self.__write_file(self.transcript_filename, transcript, "txt")

    def write_summary(self, summary: str) -> None:
        self.logger.info("Writing summary")
        self.__write_file(self.summary_filename, summary, "md")

    def __write_file(self, file_name: str, contents: str, extension: str) -> None:
        path = self.__get_path(file_name, extension)
        self.files.write_file(path, contents)

    def get_now_str(self) -> str:
        return datetime.now(UTC).strftime("%Y%m%d%H%M%S")

    def __get_path(self, file_name: str, extension: str) -> str:
        return f"{file_name}{self.get_now_str()}.{extension}"
