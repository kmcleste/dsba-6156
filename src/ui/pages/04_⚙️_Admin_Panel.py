import requests

import streamlit as st

from common.uncc_logo import logo


def main():
    st.set_page_config(page_title="Admin Config", page_icon="⚙️")

    logo()

    st.markdown("# Admin Config")

    try:
        r: requests.Response = requests.get(url="http://0.0.0.0:8000/")

        st.write(f"API Status: {'OK' if r.status_code else 'DEGRADED'}")
    except Exception:
        st.error("Unable to connect to Search API")

    st.button(label="Refresh 🔄", help="Click to get updated Search API status")


if __name__ == "__main__":
    main()
