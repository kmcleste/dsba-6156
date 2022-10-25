import streamlit as st

from common.uncc_logo import logo


def main():
    st.set_page_config(page_title="Admin Config", page_icon="⚙️")

    logo()

    st.markdown("# Admin Config")


if __name__ == "__main__":
    main()
