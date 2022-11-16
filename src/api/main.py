import os
import pathlib

from fastapi import FastAPI, status, File, UploadFile
from fastapi.responses import HTMLResponse
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
    """Override default swagger page html by including UNCC logo as the page favicon"""
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="DSBA 6156: Applied Machine Learning",
        swagger_favicon_url="https://raw.githubusercontent.com/kmcleste/dsba-6156/main/src/api/static/favicon.ico",
    )


@app.get("/redoc", include_in_schema=False)
def overridden_redoc():
    """Override default redoc page html by including UNCC logo as the page favicon"""
    return get_redoc_html(
        openapi_url="/openapi.json",
        title="DSBA 6156: Applied Machine Learning",
        redoc_favicon_url="https://raw.githubusercontent.com/kmcleste/dsba-6156/main/src/api/static/favicon.ico",
    )


@app.get(path="/", include_in_schema=False)
async def root():
    content = """
        <body>
        <form action="/upload-files/" enctype="multipart/form-data" method="post">
        <input name="files" type="file" multiple>
        <input type="submit">
        </form>
        </body>
    """
    return HTMLResponse(content=content)


@app.post(
    path="/search",
    status_code=status.HTTP_200_OK,
    response_model=Answer,
    tags=["search"],
)
def search(query: Query):
    """Query the index using extractive search and return an answer.

    **Args**:

        query (Query): A dictionary containing:

            - query (str): a natural language question

            - params (dict): additional search parameters, see: INSERT_LINK

            - debug (bool): enable verbose logging, defaults to `false`

    **Returns**:

        Answer: A dictionary containing:

            - answer (str): extracted answer from index

            - score (float): computed relevance score

            - context (str): surrounding document context the answer was found

            - document_id (str): unique identifier
    """
    return _haystack.extractive_search(
        query=query.query, params=query.params, debug=query.debug
    )["answers"][0]


@app.post(
    path="/upload-files",
    status_code=status.HTTP_201_CREATED,
    response_model=Files,
    tags=["documents"],
)
async def upload_files(
    files: list[UploadFile] = File(...),
):
    await _haystack.write_files(files=files)
    return _haystack.write_documents(
        documents=pathlib.Path(os.getcwd(), "src", "api", "data")
    )


@app.post(
    path="/fetch-documents",
    status_code=status.HTTP_200_OK,
    response_model=Documents,
    tags=["documents"],
)
def fetch_documents(index: Index):
    """Fetch all of the documents in a selected index

    **Args**:

        index (Index): A dictionary containing:

            - index (str): name of the desired index

    """
    return {"documents": _haystack.document_store.get_all_documents(index=index.index)}


@app.post(
    path="/documents-by-id",
    status_code=status.HTTP_200_OK,
    response_model=Documents,
    tags=["documents"],
)
def documents_by_id(input: DocumentsID):
    """Fetch specific documents by their unique id

    **Args**:

        input (DocumentsID): A dictionary containing:

            - index (str): name of the desired index

            - document_ids (list): comma-serpated document id's

    """
    return {
        "documents": _haystack.document_store.get_documents_by_id(
            ids=input.document_ids, index=input.index
        )
    }


@app.post(
    path="/describe-documents",
    status_code=status.HTTP_200_OK,
    response_model=Summary,
    tags=["documents"],
)
def describe_documents_(input: Index):
    """Summary statistics for a given index

    **Args**:

        input (Index): A dictionary containing:

            - index (str): name of the desired index

    """
    return _haystack.document_store.describe_documents(index=input.index)


# TODO: Add endpoint to index documents found in 'data' directory
