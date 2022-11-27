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

        submit = st.form_submit_button(label="Search")

        if submit:
            with st.spinner(text="🧠 Performing neural search..."):
                r: requests.Response = Request.post(endpoint="/search", **search_kwargs)
            if r is not None:
                if "answers" in r.json():
                    df: pd.DataFrame = pd.DataFrame([x for x in r.json()["answers"]])
                    df = df[["answer", "score", "context", "document_id", "meta"]]
                    st.dataframe(df)
                else:
                    st.json(r.json())
            else:
                st.info("Index is empty")


if __name__ == "__main__":
    main()
