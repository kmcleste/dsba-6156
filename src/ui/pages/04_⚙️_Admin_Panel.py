import json
import requests

import streamlit as st

from common.uncc_logo import logo


def main():
    st.set_page_config(page_title="Admin Config", page_icon="⚙️")

    logo()

    st.markdown("# Admin Config")

    # TODO: Define callback to save/load settings to/from json

    # def write_settings():
    #     with open("settings.json", "w") as f:
    #         f.write(json.dumps(st.session_state["deployment-method"], indent=4))

    # st.selectbox(label="Deployment Method", options=["docker","cli"], key="deployment-method", on_change=write_settings)

    st.selectbox(
        label="Deployment Method", options=["docker", "cli"], key="deployment-method"
    )

    if "docker" in st.session_state.get("deployment-method"):
        st.session_state["api_base_url"] = "http://api:8000/"
    else:
        st.session_state["api_base_url"] = "http://127.0.0.1:8000/"

    try:
        r: requests.Response = requests.get(url=st.session_state.get("api_base_url"))

        st.write(f"API Status: {'OK' if r.status_code else 'DEGRADED'}")
    except Exception:
        st.error("Unable to connect to Search API")

    st.button(label="Refresh 🔄", help="Click to get updated Search API status")


if __name__ == "__main__":
    main()
