# Meeting Summarisers

Records audio, transcribes the recordings, and then creates a summary using an LLM.

## Technologies used

- asyncio: to have a module that sounds like a spell from a certain author's books
- faster-whisper: Audio transcribing using Whisper models
- nltk: tokenisation
- numpy: _maths_
- OpenAI SDK: Used for AI requests, to an OpenAI compatible API, to summarise the transcript
- PyAudio: Audio recording + processing
- pyqt6: GUI
- transformers: Embeddings

## Usage

- Download
- Create and use a virtual environment using your preferred method
- `pip install -r requirements.txt`
- `python -m meetingsummariser.main`
- Setup the options
- Choose devices you want to record/transcribe/summarise
- Click start
- When you're finished, click stop

### Additional usage information

- There is a "Context" box. If you provide information about _what_ is being transcribed here it will be provided to the AI when the initial summaries are created. This does not have to be overly detailed, something short like "Sprint planning meeting" would be useful.

### Notes

- Only records inputs, so you'll need a way to record your output audio device as an input. E.g. [blackhole](https://formulae.brew.sh/cask/blackhole-2ch)

### Building instructions

- Build with `python setup.py sdist bdist_wheel`
- Install (using `pipx` but YMMV); `pipx install -f ./dist/meeting_summariser-0.1.9-py3-none-any.whl`. Note: version/filename might be different.
    - Note: actual file name depends on version
- Now available from the CLI by running `meetingsummariser`

## Additional information

- [Architecture](/docs/architecture.md)
- [Options](/docs/options.md)
- [TODO](/TODO.md)
- [Changelog](/CHANGELOG.md)
