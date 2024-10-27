import logging
from typing import List

import nltk
import numpy as np
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.metrics.pairwise import cosine_similarity
from transformers import BertModel, BertTokenizer


class Tokeniser:
    """
    A class to split text into smaller chunks, to make the AI more likely to succeed in summarising them.

    1. Split the text into sentences using tokenisation (using nltk)
    2. Combine the sentences again up to a _minimum_ word length
    3. Continue combining the sentences until either:
        a. we exceed a _maximum_ word length
        or b. the next sentence is too different semantically (determined using embeddings - transformers + Bert model)
    - We also overlap the chunks slightly either side to ensure there is as little context lost as possible per chunk.
    """

    logger = logging.getLogger(__name__)
    sentences_per_paragraph: int = 10

    def __init__(
        self, tokeniser_model: str = "punkt_tab", sentences_per_paragraph: int = 10
    ) -> None:
        nltk.download(tokeniser_model)
        self.sentences_per_paragraph = sentences_per_paragraph
        self.tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
        self.model = BertModel.from_pretrained("bert-base-uncased")

    def get_embeddings(self, text: str):
        inputs = self.tokenizer(
            text, return_tensors="pt", truncation=True, padding=True
        )
        outputs = self.model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).detach().numpy()

    def get_similarity(self, a: str, b: str) -> float:
        embedding_1 = self.get_embeddings(" ".join(a))
        embedding_2 = self.get_embeddings(b)
        similarity = cosine_similarity(embedding_1, embedding_2)
        return np.mean(similarity)

    def split_text_by_similarity(
        self,
        text: str,
        max_words_per_chunk: int = 256,
        min_words_per_chunk: int = 128,
        sentence_overlap: int = 3,
        similarity_threshold=0.8,
    ):
        """
        Splits the text into semantic chunks using BERT embeddings.

        Args:
        text (str): The input text to be split.
        max_words_per_chunk (int): Maximum number of words per chunk.
        min_words_per_chunk (int): Minimum number of words per chunk
        sentence_overlap (int): How many sentences should overlap each side of the chunk.
        similarity_threshold (float): Threshold for cosine similarity to split chunks.

        Returns:
        list: A list of chunks split based on semantic similarity.
        """
        sentences: List[str] = sent_tokenize(text)
        chunks: List[str] = []
        current_chunk: List[str] = []
        current_chunk_word_count = 0

        for x, sentence in enumerate(sentences):
            current_chunk.append(sentence)
            current_chunk_word_count += len(word_tokenize(sentence))

            if current_chunk_word_count < min_words_per_chunk:
                continue

            if x + 1 < len(sentences):
                similarity = self.get_similarity(
                    " ".join(current_chunk), sentences[x + 1]
                )

                if (
                    current_chunk_word_count >= max_words_per_chunk
                    or similarity < similarity_threshold
                ):
                    chunks.append(" ".join(current_chunk))

                    overlap_start = max(0, len(current_chunk) - sentence_overlap)
                    current_chunk = current_chunk[overlap_start:]
                    current_chunk_word_count = sum(
                        len(word_tokenize(sentence)) for sentence in current_chunk
                    )

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks
