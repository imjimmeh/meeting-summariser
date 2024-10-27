from pydantic import BaseModel

from .ai_options import AIOptions
from .audio_options import AudioOptions
from .summary_options import SummaryOptions
from .whisper_options import WhisperOptions


class Options(BaseModel):
    ai_options: AIOptions = AIOptions()
    whisper_options: WhisperOptions = WhisperOptions()
    summary_options: SummaryOptions = SummaryOptions()
    audio_options: AudioOptions = AudioOptions()
