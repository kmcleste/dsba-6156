import os
import pathlib

from fastapi import FastAPI, status, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html

from models import (
    ExtractedAnswer,
    Query,
    Files,
    Index,
    Documents,
    DocumentsID,
    Summary,
    DocumentSearch,
    SearchSummarization,
    QuestionGeneration,
    GeneratedQuestions,
    QuestionAnswerGeneration,
    HTTPError,
)
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
        <style>
        body{
        background: rgba(0,0,0,0.9);
        }
        form{
        position: absolute;
        top: 50%;
        left: 50%;
        margin-top: -100px;
        margin-left: -250px;
        width: 500px;
        height: 200px;
        border: 4px dashed #fff;
        }
        form p{
        width: 100%;
        height: 100%;
        text-align: center;
        line-height: 170px;
        color: #ffffff;
        font-family: Arial;
        }
        form input{
        position: absolute;
        margin: 0;
        padding: 0;
        width: 100%;
        height: 100%;
        outline: none;
        opacity: 0;
        }
        form button{
        margin: 0;
        color: #fff;
        background: #16a085;
        border: none;
        width: 508px;
        height: 35px;
        margin-top: -20px;
        margin-left: -4px;
        border-radius: 4px;
        border-bottom: 4px solid #117A60;
        transition: all .2s ease;
        outline: none;
        }
        form button:hover{
        background: #149174;
            color: #0C5645;
        }
        form button:active{
        border:0;
        }
        </style>
        <body>
        <form action="/upload-files/" enctype="multipart/form-data" method="post">
            <input name="files" type="file" multiple>
            <p>Drag and drop your files</p>
            <button type="submit">Upload</button>
        </form>
        </body>
    """
    return HTMLResponse(content=content)


@app.get(path="/health")
async def health():
    return HTMLResponse(status_code=status.HTTP_200_OK)


@app.post(
    path="/extractive-qa",
    status_code=status.HTTP_200_OK,
    tags=["search"],
    response_model=ExtractedAnswer,
    responses={404: {"model": HTTPError, "description": "Empty Index"}},
)
def extractive_qa(query: Query):
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
    if _haystack.document_store.get_document_count() != 0:
        return _haystack.extractive_qa(
            query=query.query, params=query.params, debug=query.debug
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Index is empty"
        )


# TODO: Update documentation
@app.post(
    path="/document-search",
    status_code=status.HTTP_200_OK,
    tags=["search"],
    response_model=DocumentSearch,
    responses={404: {"model": HTTPError, "description": "Empty Index"}},
)
def document_search(query: Query):
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
    if _haystack.document_store.get_document_count() != 0:
        return _haystack.document_search(
            query=query.query, params=query.params, debug=query.debug
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Index is empty"
        )


# TODO: Update documentation
@app.post(
    path="/search-summarization",
    status_code=status.HTTP_200_OK,
    tags=["search"],
    response_model=SearchSummarization,
    responses={404: {"model": HTTPError, "description": "Empty Index"}},
)
def search_summarization(query: Query):
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
    if _haystack.document_store.get_document_count() != 0:
        return _haystack.search_summarization(
            query=query.query, params=query.params, debug=query.debug
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Index is empty"
        )


# TODO: Update documentation
@app.post(
    path="/question-generation",
    status_code=status.HTTP_200_OK,
    tags=["generation"],
    # response_model=GeneratedQuestions,
    responses={404: {"model": HTTPError, "description": "Empty Index"}},
)
def question_generation(input: QuestionGeneration):
    """Query the index using extractive search and return an answer.

    **Args**:

        input (Query): A dictionary containing:

            - ids (list): document id's

            - params (dict): additional search parameters, see: INSERT_LINK

            - debug (bool): enable verbose logging, defaults to `false`

    **Returns**:

        Answer: A dictionary containing:

            - answer (str): extracted answer from index

            - score (float): computed relevance score

            - context (str): surrounding document context the answer was found

            - document_id (str): unique identifier
    """
    if _haystack.document_store.get_document_count() != 0:
        return _haystack.question_generation(
            ids=input.ids, params=input.params, debug=input.debug
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Index is empty"
        )


# TODO: Update documentation
@app.post(
    path="/question-answer-generation",
    status_code=status.HTTP_200_OK,
    tags=["generation"],
    responses={404: {"model": HTTPError, "description": "Empty Index"}},
)
def question_answer_generation(input: QuestionGeneration):
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
    if _haystack.document_store.get_document_count() != 0:
        return _haystack.question_answer_generation(
            ids=input.ids, params=input.params, debug=input.debug
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Index is empty"
        )


# TODO: Update documentation
@app.post(
    path="/upload-files",
    status_code=status.HTTP_201_CREATED,
    response_model=Files,
    tags=["modify"],
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
    docs = _haystack.document_store.get_all_documents(index=index.index)
    return {"documents": docs}


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
def describe_documents_():
    """Summary statistics for a given index"""
    if _haystack.document_store.get_document_count() != 0:
        return _haystack.describe_documents()
    else:
        raise HTTPException(status_code=404, detail="Index is empty")


# TODO: Update documentation
@app.delete(
    path="/delete-documents",
    status_code=status.HTTP_200_OK,
    tags=["modify"],
)
def delete_documents(ids: DocumentsID):
    if _haystack.document_store.get_document_count() != 0:
        return _haystack.delete_documents(ids=ids.document_ids)
    else:
        raise HTTPException(status_code=404, detail="Index is empty")
