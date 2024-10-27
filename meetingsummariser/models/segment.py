import logging

logger = logging.getLogger(__name__)


class Segment:
    """
    A slither of a transcript returned from Whisper
    """

    no_speech_prob_silence_threshold: float = 0.04
    avg_logprob_silence_threshold: float = -0.7

    def __init__(
        self,
        id,
        seek,
        start,
        end,
        text,
        tokens,
        temperature,
        avg_logprob,
        compression_ratio,
        no_speech_prob,
        words=None,
        no_speech_prob_silence_threshold: float = 0.04,  # This value and avg_logprob_silence_threshold come from the options we set; used for filtering out silent segments
        avg_logprob_silence_threshold: float = -0.7,
    ):
        self.id = id
        self.seek = seek
        self.start = start
        self.end = end
        self.text = text
        self.tokens = tokens
        self.temperature = temperature
        self.avg_logprob = avg_logprob
        self.compression_ratio = compression_ratio
        self.no_speech_prob = no_speech_prob
        self.words = words
        self.no_speech_prob_silence_threshold = no_speech_prob_silence_threshold
        self.avg_logprob_silence_threshold = avg_logprob_silence_threshold

    def __repr__(self):
        return (
            f"Segment(id={self.id}, seek={self.seek}, start={self.start}, "
            f"end={self.end}, text='{self.text}', tokens={self.tokens}, "
            f"temperature={self.temperature}, avg_logprob={self.avg_logprob}, "
            f"compression_ratio={self.compression_ratio}, no_speech_prob={self.no_speech_prob}, "
            f"words={self.words})"
        )

    @property
    def is_silent(self):
        if self.no_speech_prob is None or self.avg_logprob is None:
            return False

        return (
            self.no_speech_prob > self.no_speech_prob_silence_threshold
            and self.avg_logprob < self.avg_logprob_silence_threshold
        )

    @staticmethod
    def from_segment(
        segment,
        no_speech_prod_silence_threshold: float,
        avg_logprob_silence_threshold: float,
    ):
        return Segment(
            id=segment.id,
            seek=segment.seek,
            start=segment.start,
            end=segment.end,
            text=segment.text,
            tokens=segment.tokens,
            temperature=segment.temperature,
            avg_logprob=segment.avg_logprob,
            compression_ratio=segment.compression_ratio,
            no_speech_prob=segment.no_speech_prob,
            words=segment.words,
            no_speech_prob_silence_threshold=no_speech_prod_silence_threshold,
            avg_logprob_silence_threshold=avg_logprob_silence_threshold,
        )

    @staticmethod
    def from_json(json):
        return Segment(
            id=json["id"],
            seek=json["seek"],
            start=json["start"],
            end=json["end"],
            text=json["text"],
            tokens=json["tokens"],
            temperature=json["temperature"],
            avg_logprob=json["avg_logprob"],
            compression_ratio=json["compression_ratio"],
            no_speech_prob=json["no_speech_prob"],
            words=json.get("words"),
        )
