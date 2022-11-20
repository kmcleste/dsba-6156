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
        query: str = st.text_input(
            label="Query", key="query", placeholder="Enter a full sentence question"
        )

        search_kwargs: dict = {"json": {"query": query, "params": {}, "debug": True}}

        submit = st.form_submit_button(label="Search")

        if submit:
            with st.spinner(text="🧠 Performing neural search..."):
                r: requests.Response = Request.post(endpoint="/search", **search_kwargs)
            if r is not None:
                if not isinstance(r.json(), list):
                    st.json(r.json())
                else:
                    df: pd.DataFrame = pd.DataFrame(r.json())
                    df = df[["answer", "score", "context", "document_id"]]
                    st.dataframe(df)
            else:
                st.info("Index is empty")


if __name__ == "__main__":
    main()
