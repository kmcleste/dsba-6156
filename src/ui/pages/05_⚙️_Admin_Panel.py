import streamlit as st

from common.uncc_logo import logo
from common.requests_common import Request


def main():
    st.set_page_config(page_title="Admin Panel", page_icon="⚙️")

    logo()

    st.markdown("# Admin Panel")

    resp = Request.get(endpoint="/health")

    if resp:
        st.markdown("API Status: `healthy`")

    st.button(label="Refresh 🔄", help="Click to get updated Search API status")

    fetch_kwargs: dict = {"json": {"index": "semantic"}}
    resp = Request.post(endpoint="/fetch-documents", **fetch_kwargs)
    if "documents" in resp.json():
        if len(resp.json()["documents"]) > 0:
            options = [x["id"] for x in resp.json()["documents"]]
            st.multiselect(
                label="Delete Documents", options=["All"] + options, key="delete-docs"
            )

            if st.button(label="Delete"):
                if "All" in st.session_state.get("delete-docs"):
                    delete_kwargs: dict = {"json": {"index": "semantic"}}
                    resp = Request.delete(endpoint="/delete-documents", **delete_kwargs)
                    st.info(resp.json()["message"])
                else:
                    delete_kwargs: dict = {
                        "json": {
                            "index": "semantic",
                            "document_ids": st.session_state.get("delete-docs"),
                        }
                    }
                    resp = Request.delete(endpoint="/delete-documents", **delete_kwargs)
                    st.info(resp.json()["message"])


if __name__ == "__main__":
    main()
