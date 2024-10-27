from pydantic import BaseModel

PARAGRAPH_SUMMARY_PROMPT = """You are an expert summarization assistant.
Your task is to distill the following paragraph into a concise summary that captures its essential ideas and key points. Focus on clarity and coherence.

Return your result as a markdown formatted list, with up to 10 bulletpoints. Do not return any other explanation, description, comments, etc. in your response."""

AGGREGATE_SUMMARIES_PROMPT = """You are an expert summarization assistant.
Below are summaries from various sections of a meeting transcript. Your goal is to synthesize these summaries into a cohesive overview.
Highlight the main themes, significant decisions, and any critical insights.

Return your result as a markdown formatted list. Do not return any other explanation, description, comments, etc. in your response."""

FINAL_OUTPUT_PROMPT = """You are an expert summarization assistant. Based on the following summaries, please create a structured overview of the meeting.

Ensure that the summary is coherent, concise, and easy to understand.

Return your result in markdown format.
Do not return any other explanation, description, comments, etc. in your response.
Return your result in the following format:

# <A title for the meeting>

## Purpose and summary

<Up to 5 sentences overviewing the purpose of the meeting and the meeting discussions>

## Discussion Points

<Markdown formatted bulletpoint list of the discussion points in the meeting. No more than 10>
E.g.:
- <Discussion point one>
- <Discussion point two>
<etc.>

## Key Decisions

<Markdown formatted bulletpoint list of the most important key decisions of the meeting. No more than 10>
E.g.:
- <Key decision one>
- <Key decision two>
<etc.>

## Action items

<Markdown formatted bulletpoint task list of the action items to take as a result of the meeting. No more than 10>
- [ ] <Action item one>
- [ ] <Action item two>
<etc.>
"""


class PromptOptions(BaseModel):
    summarise_paragraphs: str = PARAGRAPH_SUMMARY_PROMPT
    aggregate_summaries: str = AGGREGATE_SUMMARIES_PROMPT
    final_output: str = FINAL_OUTPUT_PROMPT
    meeting_context: str = ""
