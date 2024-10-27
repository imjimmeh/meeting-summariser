from pydantic import BaseModel


class AudioOptions(BaseModel):
    no_speech_prob_silence_threshold: float = 0.04  # Greater than
    avg_logprob_silence_threshold: float = -0.7  # less than

    silence_threshold_seconds: float = 2.0
