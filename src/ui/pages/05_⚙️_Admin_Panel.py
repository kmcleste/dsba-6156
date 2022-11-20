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


if __name__ == "__main__":
    main()
