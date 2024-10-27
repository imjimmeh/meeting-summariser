from pydantic import BaseModel

available_whisper_models = [
    "Systran/faster-distil-whisper-large-v3",
    "Systran/faster-distil-whisper-large-v2",
    "Systran/faster-distil-whisper-medium.en",
    "Systran/faster-distil-whisper-small.en",
    "Systran/faster-whisper-medium.en",
    "Systran/faster-whisper-base.en",
]


class WhisperOptions(BaseModel):
    model: str = "Systran/faster-distil-whisper-medium.en"
