from fastapi import FastAPI, status, File, UploadFile
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html

from models import Answer, Query, Files, Index, Documents, DocumentsID, Summary
from search import HaystackHelper

app = FastAPI(
    title="DSBA 6156: Applied Machine Learning",
    docs_url=None,
    redoc_url=None,
    version="0.1.0",
)

_haystack = HaystackHelper(index="semantic")


@app.get("/docs", include_in_schema=False)
def overridden_swagger():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="DSBA 6156: Applied Machine Learning",
        swagger_favicon_url="https://raw.githubusercontent.com/kmcleste/dsba-6156/main/src/api/static/favicon.ico",
    )


@app.get("/redoc", include_in_schema=False)
def overridden_redoc():
    return get_redoc_html(
        openapi_url="/openapi.json",
        title="DSBA 6156: Applied Machine Learning",
        redoc_favicon_url="https://raw.githubusercontent.com/kmcleste/dsba-6156/main/src/api/static/favicon.ico",
    )


@app.get(path="/", include_in_schema=False)
def root():
    return {
        "author": "Kyle McLester",
        "version": "0.1.0",
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
