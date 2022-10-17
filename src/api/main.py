import os
import pathlib

from fastapi import FastAPI, status

from search import HaystackHelper
from utils.logger import logger

app = FastAPI(
    title="DSBA 6156: Applied Machine Learing",
    description="This API offers neural search capabilities for the UNCC Code of Ethics.",
    version="0.1.0",
)

_haystack = HaystackHelper(index="semantic")


@app.get(path="/", status_code=status.HTTP_200_OK)
async def root():
    return True if _haystack else False


@app.get(path="/search", status_code=status.HTTP_200_OK)
async def search(query: str):
    return _haystack.extractive_search(query=query)["answers"][0]


@app.post(path="/index-documents", status_code=status.HTTP_201_CREATED)
async def index_documents():
    path = pathlib.Path(os.getcwd(), "api", "data")
    _haystack.write_documents(documents=path)
    return 200
