import pandas as pd
import requests
import streamlit as st

from common.uncc_logo import logo
from common.requests_common import Request


def main():
    st.set_page_config(page_title="Search", page_icon="❓", layout="wide")

    logo()

    st.markdown("# Search")

    with st.form(key="query-form"):
        st.text_input(
            label="Query", key="query", placeholder="Enter a full sentence question"
        )
        st.selectbox(
            label="Search type",
            options=["Extractive QA", "Document Search", "Search Summarization"],
            key="search-type",
        )

        submit = st.form_submit_button(label="Search")

        if submit:
            with st.spinner(text="🧠 Performing neural search..."):
                if "Extractive QA" in st.session_state.get("search-type"):

                    search_kwargs: dict = {
                        "json": {
                            "query": st.session_state.get("query"),
                            "params": {
                                # number of documents to return
                                "Retriever": {"top_k": 5},
                                # number of answers to extract from a single doc
                                "Reader": {"top_k": 10},
                            },
                            "debug": True,
                        }
                    }

                    r: requests.Response = Request.post(
                        endpoint="/extractive-qa", **search_kwargs
                    )

                    if r is not None:
                        if "answers" in r.json():
                            df: pd.DataFrame = pd.DataFrame(
                                [x for x in r.json()["answers"]]
                            )
                            df = df[["answer", "score", "context", "document_id"]]
                            st.dataframe(df)
                        else:
                            st.json(r.json())
                    else:
                        st.info("Index is empty")

                else:
                    search_kwargs: dict = {
                        "json": {
                            "query": st.session_state.get("query"),
                            "params": {
                                # number of documents to return
                                "Retriever": {"top_k": 5},
                            },
                            "debug": True,
                        }
                    }
                    if "Document Search" in st.session_state.get("search-type"):
                        r: requests.Response = Request.post(
                            endpoint="/document-search", **search_kwargs
                        )

                        json_exists = getattr(r, "json", None)
                        if callable(json_exists):
                            resp: dict = r.json()
                            df = pd.DataFrame(resp["documents"])
                            st.dataframe(
                                df[["id", "content", "score"]], use_container_width=True
                            )

                    elif "Search Summarization" in st.session_state.get("search-type"):
                        r: requests.Response = Request.post(
                            endpoint="/search-summarization", **search_kwargs
                        )

                        json_exists = getattr(r, "json", None)
                        if callable(json_exists):
                            resp: dict = r.json()
                            st.markdown("### Summarization")
                            st.markdown(f"{resp['documents'][0]['meta']['summary']}")
                            st.markdown("### Original content")
                            st.markdown(f"{resp['documents'][0]['content']}")


if __name__ == "__main__":
    main()
