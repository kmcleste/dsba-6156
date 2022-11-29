from typing import Union

from haystack import Answer, Document
from pydantic import BaseModel


class Query(BaseModel):
    query: str = "What is the meaning of life?"
    params: Union[dict, None] = {"Retriever": {"top_k": 10}}
    debug: Union[bool, None] = False


class QuestionGeneration(BaseModel):
    ids: list[str]
    params: Union[dict, None] = None
    debug: Union[bool, None] = False


class ExtractedAnswer(BaseModel):
    query: str
    no_ans_gap: float
    answers: list[Answer]


class DocumentSearch(BaseModel):
    documents: list[Document]
    root_node: str
    params: dict
    query: str
    node_id: str


class SearchSummarization(BaseModel):
    documents: list[Document]
    root_node: str
    params: dict
    query: str
    node_id: str


class GeneratedQuestions(BaseModel):
    generated_questions: list[dict]
    documents: list[Document]
    root_node: str
    params: dict
    node_id: str


class QuestionAnswerGeneration(BaseModel):
    queries: list[str]
    answers: list[list[Answer]]
    no_ans_gaps: list[float]
    documents: list[list[Document]]
    root_node: str
    params: dict
    node_id: str


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
