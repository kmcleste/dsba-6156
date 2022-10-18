from typing import List, Union

from pydantic import BaseModel


class Root(BaseModel):
    author: Union[str, List[str]]
    version: str
    fastapi: str


class Query(BaseModel):
    query: str = "When was Marcus born?"
    params: Union[dict, None] = None
    debug: Union[bool, None] = None


class Answer(BaseModel):
    answer: str
    score: float
    context: str
    document_id: str
