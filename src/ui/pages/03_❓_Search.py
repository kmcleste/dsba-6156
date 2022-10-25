import requests

import streamlit as st

from common.uncc_logo import logo


def main():
    st.set_page_config(page_title="Search", page_icon="❓")

    logo()

    st.markdown("# Search")

    with st.form(key="query-form"):
        query: str = st.text_input(
            label="Query", key="query", value="When was Marcus Aurelius born?"
        )
        # index: str = st.selectbox(label="Index", options=["semantic"], key="query-index")

        data: dict = {"query": query, "params": {}, "debug": False}

        submit = st.form_submit_button(label="Search")

        if submit:
            try:
                with st.spinner(text="🧠 Performing neural search..."):
                    r: requests.Response = requests.post(
                        url="http://127.0.0.1:8000/search", json=data
                    )
                    st.json(r.json())
            except Exception:
                st.error("Unable to connect to Search API")


if __name__ == "__main__":
    main()
