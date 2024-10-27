# Options

## AI Options

| Option      | Description                                                                                                                  | Example                     |
| ----------- | ---------------------------------------------------------------------------------------------------------------------------- | --------------------------- |
| Model       | The name of the LLM to use                                                                                                   | llama3.1:8b                 |
| URL         | An OpenAI compatible base URL                                                                                                | <http://localhost:11434/v1> |
| Temperature | Responsible (partly) for the AI's "randomness" in its responses. Higher == more random == more creative == more error prone. |                             |

## Audio Options

| Option                           | Description                                                                                                             | Example |
| -------------------------------- | ----------------------------------------------------------------------------------------------------------------------- | ------- |
| no_speech_prob silence threshold | Combined with avg_logprob silence threshold to calculate whether a transcription chunk is correct or hallucinated       |         |
| avg_logprob silence threshold    |                                                                                                                         |         |
| Silence seconds threshold        | How many seconds of silence are allowed before the current audio chunk is finished + transcribed, and a new one started |         |

## Prompts

| Name                       | Description                                                            |
| -------------------------- | ---------------------------------------------------------------------- |
| Summarise prompt           | Prompt used to summarise/extract data from the small transcript chunks |
| Aggregate summaries prompt | Prompt used to summarise groups of the summaries from above            |
| Final prompt               | Final prompt used to compile the final output                          |

## Summary Options

| Option                  | Description | Example |
| ----------------------- | ----------- | ------- |
| Sentences per paragraph |             |         |
| Summaries per aggregate |             |         |

## Whisper Options

| Option | Explained                                                                                                                                                                          |
| ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Model  | What faster-whisper model to use. Small should be more than sufficient. Medium will be more accurate, especially for other languages. Medium and above will require GPU + 4GB VRAM |
