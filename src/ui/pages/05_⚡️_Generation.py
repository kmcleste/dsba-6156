import pandas as pd
import requests
import streamlit as st

from common.uncc_logo import logo
from common.requests_common import Request


def main():
    st.set_page_config(page_title="Generation", page_icon="⚡️", layout="wide")

    logo()

    st.markdown("# Generation")
    st.markdown("#### `experimental`")

    fetch_kwargs: dict = {"json": {"index": "semantic"}}
    resp = Request.post(endpoint="/fetch-documents", **fetch_kwargs)

    # TODO: Update all to check if json method is callable first
    if "documents" in resp.json():
        if len(resp.json()["documents"]) > 0:
            options = [x["id"] for x in resp.json()["documents"]]
            st.multiselect(
                label="Document selection", options=options, key="generation-docs"
            )

    with st.form(key="query-form"):
        st.selectbox(
            label="Generation type",
            options=["Question Generation", "Question:Answer Generation"],
            key="generation-type",
        )

        submit = st.form_submit_button(label="Search")

        if submit:
            if st.session_state.get("generation-docs"):
                with st.spinner(text="🧠 Generating text..."):
                    generation_kwargs: dict = {
                        "json": {
                            "ids": st.session_state.get("generation-docs"),
                            "params": {},
                            "debug": False,
                        }
                    }
                    if "Question Generation" in st.session_state.get("generation-type"):
                        r: requests.Response = Request.post(
                            endpoint="/question-generation", **generation_kwargs
                        )
                        if r is not None:
                            if "generated_questions" in r.json():
                                docs: list[dict] = r.json().get("generated_questions")
                                for doc in docs:
                                    st.write(f"`{doc.get('document_id')}`")
                                    df: pd.DataFrame = pd.DataFrame(
                                        doc.get("questions"), columns=["questions"]
                                    )
                                    st.dataframe(df, use_container_width=True)
                            else:
                                st.error(r.json().get("message"))
                    if "Question:Answer Generation" in st.session_state.get(
                        "generation-type"
                    ):
                        r: requests.Response = Request.post(
                            endpoint="/question-answer-generation", **generation_kwargs
                        )

                        json_exists = getattr(r, "json", None)
                        if callable(json_exists):
                            if "queries" in r.json():
                                resp: dict = r.json()
                                queries = resp.get("queries")
                                answers = resp.get("answers")

                                for idx, query in enumerate(queries):
                                    st.write(query)
                                    df: pd.DataFrame = pd.DataFrame(answers[idx])
                                    st.dataframe(
                                        df[
                                            [
                                                "answer",
                                                "score",
                                                "context",
                                                "document_id",
                                            ]
                                        ],
                                        use_container_width=True,
                                    )
                            else:
                                st.error(r.json()["message"])

            else:
                st.info("Nothing was selected")


if __name__ == "__main__":
    main()
