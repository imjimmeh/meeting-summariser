from pydantic import BaseModel


class SummaryOptions(BaseModel):
    sentences_per_paragraph: int = 10
    summaries_per_aggregate: int = 5
