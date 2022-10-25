import streamlit as st

from common.uncc_logo import logo


def main():
    st.set_page_config(page_title="Search", page_icon="❓")

    logo()

    st.markdown("# Search")


if __name__ == "__main__":
    main()
