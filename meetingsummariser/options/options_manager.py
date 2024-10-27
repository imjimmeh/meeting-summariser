from typing import Callable, Dict

from pydantic_core import from_json

from meetingsummariser.files import Files
from meetingsummariser.options import Options

type OnSaveCallback = Callable[[OptionsManager], None]
DEFAULT_OPTIONS_FILENAME = "options.json"


class OptionsManager:
    on_save_callbacks: Dict[str, OnSaveCallback] = {}
    file_name: str
    files: Files

    options: Options

    def __init__(self, files: Files):
        self.file_name = DEFAULT_OPTIONS_FILENAME
        self.files = files
        self.options = Options()
        self.load()

    def load_options(self):
        file_contents = self.files.read_file(self.file_name)
        deserialised = Options.model_validate(
            from_json(data=file_contents, allow_partial=True)
        )
        self.options = deserialised

    def load(self):
        try:
            self.load_options()
        except FileNotFoundError:
            self.save_options()

    def save_options(self):
        json_str = self.options.model_dump_json(indent=4)
        self.files.write_file(self.file_name, json_str)

    def save(self):
        self.save_options()
        self.on_save()

    def on_save(self) -> None:
        for key, callback in self.on_save_callbacks.items():
            callback(self.options)

    def add_save_callback(self, key: str, callback: OnSaveCallback) -> None:
        self.on_save_callbacks[key] = callback

    def remove_save_callback(self, key: str) -> None:
        self.on_save_callbacks.pop(key, None)

    @property
    def ai_options(self):
        return self.options.ai_options

    @property
    def whisper_options(self):
        return self.options.whisper_options

    @property
    def summary_options(self):
        return self.options.summary_options

    @property
    def audio_options(self):
        return self.options.audio_options
