from fastapi import FastAPI, status, File, UploadFile
import fastapi

from models import Answer, Query, Root, Files, Index, Documents, DocumentsID, Summary
from search import HaystackHelper

app = FastAPI(
    title="DSBA 6156: Applied Machine Learing",
    description="This API offers neural search capabilities for the UNCC Code of Ethics.",
    version="0.1.0",
)

_haystack = HaystackHelper(index="semantic")


@app.get(path="/", status_code=status.HTTP_200_OK, response_model=Root)
def _root():
    return {
        "author": "Kyle McLester",
        "version": "0.1.0",
        "fastapi": fastapi.__version__,
    }


@app.post(path="/search", status_code=status.HTTP_200_OK, response_model=Answer)
def search(query: Query):
    return _haystack.extractive_search(
        query=query.query, params=query.params, debug=query.debug
    )["answers"][0]


@app.post(
    path="/upload-files", status_code=status.HTTP_201_CREATED, response_model=Files
)
async def upload_files(
    files: list[UploadFile] = File(...),
):
    return await _haystack.write_files(files=files)


@app.post(
    path="/fetch-documents", status_code=status.HTTP_200_OK, response_model=Documents
)
def fetch_documents(index: Index):
    return {"documents": _haystack.document_store.get_all_documents(index=index.index)}


@app.post(
    path="/documents-by-id", status_code=status.HTTP_200_OK, response_model=Documents
)
def documents_by_id(input: DocumentsID):
    return {
        "documents": _haystack.document_store.get_documents_by_id(
            ids=input.document_ids, index=input.index
        )
    }


@app.post(
    path="/describe-documents", status_code=status.HTTP_200_OK, response_model=Summary
)
def describe_documents_(input: Index):
    return _haystack.document_store.describe_documents(index=input.index)


# TODO: Add endpoint to index documents found in 'data' directory
