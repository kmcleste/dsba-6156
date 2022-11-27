from typing import Union

from haystack import Answer
from pydantic import BaseModel


class Query(BaseModel):
    query: str = "What is the meaning of life?"
    params: Union[dict, None] = {"Retriever": {"top_k": 10}}
    debug: Union[bool, None] = False


class ExtractedAnswer(BaseModel):
    query: str
    no_ans_gap: float
    answers: list[Answer]


class Files(BaseModel):
    message: str


class Index(BaseModel):
    index: str = "semantic"


class Documents(BaseModel):
    documents: list


class DocumentsID(Index):
    document_ids: Union[list[str], None]


class Summary(BaseModel):
    count: int
    chars_mean: float
    chars_max: int
    chars_min: int
    chars_median: int


class HTTPError(BaseModel):
    detail: str

    class Config:
        schema_extra = {"example": {"detail": "string"}}
