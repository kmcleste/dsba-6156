import os
import pathlib

from fastapi import FastAPI, status
import fastapi

from models import Answer, Query, Root
from search import HaystackHelper

app = FastAPI(
    title="DSBA 6156: Applied Machine Learing",
    description="This API offers neural search capabilities for the UNCC Code of Ethics.",
    version="0.1.0",
)

_haystack = HaystackHelper(index="semantic")


@app.get(path="/", status_code=status.HTTP_200_OK, response_model=Root)
async def root():
    resp = {
        "author": "Kyle McLester",
        "version": "0.1.0",
        "fastapi": fastapi.__version__,
    }
    return resp


@app.post(path="/search", status_code=status.HTTP_200_OK, response_model=Answer)
async def search(query: Query):
    resp: dict = _haystack.extractive_search(
        query=query.query, params=query.params, debug=query.debug
    )["answers"][0]
    return resp


@app.post(path="/upload-documents", status_code=status.HTTP_201_CREATED)
async def upload_documents():
    pass
