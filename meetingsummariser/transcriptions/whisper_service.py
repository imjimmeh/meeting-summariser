import logging
from threading import Thread
from typing import List

from faster_whisper import WhisperModel

from meetingsummariser.models import Segment
from meetingsummariser.options import OptionsManager


class WhisperService:
    """
    Transcribes audio using local Whisper models.

    Uses faster_whisper for extra vrrooooooommmmm.
    """

    whisper_model: WhisperModel = None
    model: str = ""
    model_loaded: bool = False
    options: OptionsManager
    logger = logging.getLogger(__name__)

    def __init__(self, options: OptionsManager):
        self.options = options
        self.__create_whisper_model()
        self.options.add_save_callback(
            key="whisper_service", callback=self.on_options_change
        )

    def __create_whisper_model(self):
        self.model_loaded = False
        self.model = self.options.whisper_options.model
        self.logger.info(f"Initialising Whisper model {self.model}")
        self.whisper_model = WhisperModel(self.model, compute_type="float32")
        self.model_loaded = True

    def transcribe_segments(self, filepath: str) -> List[Segment]:
        try:
            self.logger.info(f"Transcribing {filepath}")
            segments, info = self.whisper_model.transcribe(
                filepath, beam_size=5, language="en", condition_on_previous_text=False
            )
            segments = [
                Segment.from_segment(
                    segment,
                    self.options.audio_options.no_speech_prob_silence_threshold,
                    self.options.audio_options.avg_logprob_silence_threshold,
                )
                for segment in segments
            ]
            self.logger.info(f"Finished transcribing {filepath}")
            self.logger.info(segments)
            return segments
        except Exception as e:
            self.logger.error(f"Error transcribing segments: {e}")
            return []

    def on_options_change(self, options: OptionsManager) -> None:
        if options.whisper_options.model != self.model:
            self.logger.info(
                f"Model changed from {self.model} to {options.whisper_options.model}"
            )
            self.thread = Thread(target=self.__create_whisper_model)
            self.thread.start()
