from typing import Union

from pydantic import BaseModel


class Root(BaseModel):
    author: Union[str, list[str]]
    version: str
    fastapi: str


class Query(BaseModel):
    query: str = "When was Marcus born?"
    params: Union[dict, None] = None
    debug: Union[bool, None] = False


class Answer(BaseModel):
    answer: str
    score: float
    context: str
    document_id: str


class Files(BaseModel):
    message: str


class Index(BaseModel):
    index: str = "semantic"


class Documents(BaseModel):
    documents: list


class DocumentsID(Index):
    document_ids: list[str]


class Summary(BaseModel):
    count: int
    chars_mean: float
    chars_max: int
    chars_min: int
    chars_median: int
