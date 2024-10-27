import asyncio
import logging
from typing import List, Optional

from openai import AsyncOpenAI
from openai.types.chat.chat_completion import ChatCompletion
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

from meetingsummariser.options import OptionsManager
from meetingsummariser.transcriptions.tokeniser import Tokeniser

context_instructions = "The context for the meeting is below. You should focus on information that falls within this context, and ignore anything outside of it that does not seem relevant."


class AISummaryCreator(QObject):
    """
    Generates meeting summary from transcription using OpenAI compatible endpoint
    """

    client: AsyncOpenAI
    model: str = "llama3.2:3b"
    temperature = 0.7
    url: str = "http://localhost:11434/v1"
    max_retry_count: int = 3
    tokeniser: Tokeniser
    logger = logging.getLogger(__name__)
    options: OptionsManager

    status: str = ""
    summary_finished: pyqtSignal = pyqtSignal(str)

    def __init__(self, options: OptionsManager, event_loop):
        super().__init__()
        self.options = options
        self.options.add_save_callback("summary_creator", self.__on_options_change)
        self.create_openai_client()
        self.tokeniser = Tokeniser()
        self.set_model()
        self.set_temperature()
        self.event_loop = event_loop

    def create_openai_client(self):
        self.url = self.options.ai_options.url
        self.client = AsyncOpenAI(
            api_key="cant-be-empty",
            base_url=self.url,
            max_retries=self.max_retry_count * 2,
        )

    def set_model(self):
        self.model = self.options.ai_options.model

    def set_temperature(self):
        self.temperature = self.options.ai_options.temperature

    def set_transcription(self, transcription: str):
        self.transciption = transcription

    async def split_and_summarise(self, transcript: str) -> List[str]:
        """
        Split the transcript up into paragraphs using a tokeniser, then summarise/extract key information from each one using the LLM.
        """
        self.logger.info("Splitting transcript into paragraphs and creating summaries.")

        paragraphs = self.tokeniser.split_text_by_similarity(transcript)

        self.logger.info(f"Summarising {len(paragraphs)} paragraphs.")

        prompt = self.add_context_to_prompt(
            self.options.ai_options.prompts.summarise_paragraphs
        )

        return await self.execute_in_batches(
            prompt, paragraphs, status_message="Creating initial summaries"
        )

    async def aggregate_summaries(
        self, summaries: List[str], summary_group_size: int = 5
    ) -> List[str]:
        """
        Combine/aggregate the summaries into groups, then summarise/extract key information from the aggregated summary.
        """
        prompt = self.add_context_to_prompt(
            self.options.ai_options.prompts.aggregate_summaries
        )

        # Create groups of summaries
        groups = [
            "\n".join(summaries[i : i + summary_group_size])
            for i in range(0, len(summaries), summary_group_size)
        ]

        return await self.execute_in_batches(
            prompt, groups, status_message="Creating aggregate summaries"
        )

    async def execute_in_batches(
        self,
        prompt: str,
        items: List[str],
        batch_size: int = 10,
        status_message: str = "",
    ) -> list:
        """
        Execute the get_ai_result method in batches of a specified size.
        """
        tasks = []
        results = []

        for i in range(0, len(items), batch_size):
            batch = items[i : i + batch_size]

            self.logger.info(f"Processing batch {i}")
            tasks.extend([self.get_ai_result(prompt, item) for item in batch])

            if len(tasks) >= batch_size:
                self.status = f"{status_message}: executing {len(tasks) + i} out of {len(items)} requests"
                self.logger.info("Tasks exceeds batch size - awaiting")
                results.extend(await asyncio.gather(*tasks))
                tasks.clear()

        self.logger.info("Finished loop")

        if tasks:
            self.status = f"{status_message}: {len(tasks)} out of {len(items)} requests"
            self.logger.info("Awaiting final tasks")
            results.extend(await asyncio.gather(*tasks))

        self.logger.info("Returning results")
        return results

    async def create_final_summary(self, aggregated_summaries):
        prompt = self.add_context_to_prompt(
            self.options.ai_options.prompts.final_output
        )

        self.status = "Creating final summary"
        final_result = await self.get_ai_result(
            prompt,
            "\n".join(aggregated_summaries),
        )

        self.status = ""
        return final_result

    async def aggregate_to_max_count(
        self,
        summaries: List[str],
        summary_group_size: int = 5,
        max_aggregate_size: int = 30,
    ):
        aggregated_summaries = await self.aggregate_summaries(
            summaries, summary_group_size
        )

        while len(aggregated_summaries) > max_aggregate_size:
            self.logger.info(
                f"Aggregating aggregated summaries of length {len(aggregated_summaries)}"
            )
            aggregated_summaries = await self.aggregate_summaries(
                aggregated_summaries, summary_group_size
            )

        return aggregated_summaries

    def summarise_transcription(self):
        self.event_loop.run_until_complete(self.create_summary(self.transciption))

    @pyqtSlot()
    async def create_summary(self, transcript: str, try_count: int = 0):
        """
        Creates a meeting summary of the provided transcript.

        We split the transcript up into paragraphs and summarise each one, then we group the summaries up into groups and summarise _those_, then
        we finally create a final output summary of the aggregated summaries. This should ensure that we capture all key information, and prevent
        important points getting lost by the LLM.

        :param transcript: The transcript of the meeting to create a summary for
        :param try_count: How many times we should try to create a summary before failing.
        """
        if try_count >= self.max_retry_count:
            self.logger.error("Exceeded retry count - failing.")
            return None

        try:
            self.status = "Creating initial summaries"
            summaries = await self.split_and_summarise(transcript)
            aggregated_summaries = await self.aggregate_to_max_count(summaries)
            self.logger.info(
                f"Creating final AI result with {len(aggregated_summaries)} aggregates"
            )

            result = await self.create_final_summary(aggregated_summaries)

            self.summary_finished.emit(result)
        except Exception as e:
            self.logger.error(f"Error creating summary of transcript: {e}")
            await self.create_summary(transcript, try_count + 1)

    async def get_ai_result(
        self, system_prompt: str, input: str, try_count: int = 0
    ) -> Optional[str]:
        if try_count >= self.max_retry_count:
            self.logger.error(
                f"Exceeded max retry count for prompt and input. Failing.\nSystem prompt: {system_prompt}\nInput: {input}."
            )
            return None

        try:
            messages = [
                self.create_message("system", system_prompt),
                self.create_message("user", input),
            ]

            self.logger.info("Sending AI chat completion request")
            self.logger.info(messages)

            response = await self.client.chat.completions.create(
                model=self.model, messages=messages, temperature=self.temperature
            )

            self.logger.info("Have AI chat response")
            self.logger.info(response)

            return self.get_response_content(response)
        except Exception as e:
            self.logger.error(f"Error sending messages: {e}")
            return self.get_ai_result(system_prompt, input, try_count + 1)

    def create_message(self, role: str, text: str) -> dict:
        return {"role": role, "content": text}

    def get_response_content(self, response: ChatCompletion) -> str | None:
        if response and response.choices:
            first_choice = response.choices[0]
            message = first_choice.message
            content = message.content
            return content

        self.logger.info("No choice or content or message")
        return None

    def __on_options_change(self, options: OptionsManager) -> None:
        if options.ai_options.model != self.model:
            self.set_model()

        if options.ai_options.temperature != self.temperature:
            self.set_temperature()

        if options.ai_options.url != self.url:
            self.create_openai_client()

    def add_context_to_prompt(self, prompt: str):
        if (
            self.options.ai_options.prompts.meeting_context is None
            or self.options.ai_options.prompts.meeting_context == ""
        ):
            return prompt

        return f"""
{prompt}

{context_instructions}:
{self.options.ai_options.prompts.meeting_context}
"""
