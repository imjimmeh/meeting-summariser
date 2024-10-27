from pydantic import BaseModel

from .prompt_options import PromptOptions


class AIOptions(BaseModel):
    model: str = "llama3.1:8b"
    url: str = "http://localhost:11434/v1"
    temperature: float = 0.7
    prompts: PromptOptions = PromptOptions()
