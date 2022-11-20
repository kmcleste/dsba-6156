from typing import Union

from pydantic import BaseModel


class Query(BaseModel):
    query: str = "What is the meaning of life?"
    params: Union[dict, None] = {"top_k": 10}
    debug: Union[bool, None] = False


class Answer(BaseModel):
    answer: list[dict]


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


class HTTPError(BaseModel):
    detail: str

    class Config:
        schema_extra = {"example": {"detail": "string"}}
