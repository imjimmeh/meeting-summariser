## Todo

- [x] Update various services once options change
- [x] Save outputs to files
- [x] Add temperature setting back in
- [x] Save/read prompt from text file
- [x] Delete wav files once processed

### File writing

- [ ] Parent folder for outputs (e.g. `~/.meeting-summariser/outputs/MEETING-DATETIME/`)
    - [ ] Add option
    - [ ] Add functionality

### AI

- [x] Context option - put a short description of context of the meeeting in so the AI knows wag wan before transcribing
- [ ] Ability to retry summary creation
- [ ] Verify AI model + URL are correct upon/before saving
- [x] Batch requests
    - Batching of initial summaries added in v0.1.4
- [ ] Improve batch requests
    - Send up to X summary requests at one time, where X is the amount of maximum summaries per aggregate
    - Yield return summary batch
    - Queue aggregate
- [ ] Option to summarise whilst transcriptions are happening; once the maximum paragraph/token/sentence

### Audio

- [ ] Speaker diarization
- [x] Move audio stuff to subfolder
- [ ] Move audio chunk saving to `AudioChunk` class
- [ ] Ability to _pause_ recording
- [ ] Ability to pause recording per device
- [ ] Ability to set one of the devices as "you"
     - Will hopefully improve summarisation

### Bugs

- [x] Running transcription process 2nd time causes segmentation fault and crashes.
- [x] Options don't seem to be loaded correctly now with changes

### Core

- [x] Improve event driven architecture
- [ ] Further improve event driven architecture
    - Once audio recorders all finish -> fire event
      - Parent service (MultiAudioTranscriptionService???) receives these events
      - Once it's received X amount of events, where X is the amount of audio recorders it has, then end the Transcription service
    - Transcription service fires event to say done, along with transcript
    - Summary service receives event, starts summary
    - Fire events when added/removed from queue; use for status label
- [x] Refactor file handling a bit more; make the `/meetingsummariser/files.py` file a class
- [ ] Consider moving to server/client architecture, with client being web app

### Documentation

- [ ] Add documentation for rough process flow

### Options

- [x] Audio options; max silent duration, rate (? is this based on device?), silent threshold per segent
- [ ] Tokeniser options:
    - [ ] Models
    - [ ] Max/min words per chunk
    - [ ] Chunk overlap
    - [ ] Max/min sentences per chunk??
    - [ ] Disable semantic chunking - use sentences/paragraphs only
- [x] Add audio options to options menu
- [ ] Have an "advanced options" enable thing, for the more complicated/faffy stuff (e.g. audio options, chunk overlap, temperature)
- [ ] Verify settings are valid before actually saving; ensure AI model is valid, URL is correct, etc.
- [ ] Option for amount of AI requests that can happen simultaenously

### UI

- [ ] Prevent running until model loading; show loading progress
    - Loading screen?
    - Several models now (Whisper, Bert, nltk)
- [ ] Start/stop recording button; should only show start once _entire_ process has finished. "Start recording" -> "Stop recording" -> "Cancel" -> "Start recording"
- [x] Fix options menu centering
- [ ] Error messages
- [ ] More feedback on current processes:
    - [x] summarisation process state
    - [x] currently transcribing an audio chunk
    - [ ] Files written + location
    - [ ] Model loading stte
- [ ] Button to copy transcript + summary to clipboard
- [ ] Option to view individual AI summaries, and/or the aggregate summaries
- [x] Move `gui.py` and `options_editor.py` into a `gui` folder or something
- [x] Move logic out of `gui.py` where possible
- [x] Increase size
- [x] Hide/show different options sections
- [x] General UI/UX improvements
- [x] Switch to PyQT, or some other alternative

### Summarisation/tokenisation

- [ ] Ability to set summary size to be based on token length
- [x] Ability for the summary size to be based on semantics, not just paragraphs/sentence length
- [ ] Change the aggregate size to be token based
- [x] Overlap text chunks sent to AI to ensure context is not lost
- [ ] Ability to edit prompt for specific transcription
- [ ] Run tokenisation process in background IF transcription already over a certain length AND nothing is being transcribed
- [ ] Options to use OpenAI compatible embeddings URL instead of local embeddings

### Transcription

- [ ] Use word level transcription

### Refactor

- [x] Refactor `audio_transcriber_gui.py`
    - [x] Smaller components
    - [ ] Split status labels into their own things and have them be responsible for their own update
- [ ] Event bus??
- [ ] Rename things more appropriately
- [ ] Readdress the `meeting_summariser.py` and `multiaudio_transcription_service.py`
   - Do we need 2 things? Can we make their roles more explict?
