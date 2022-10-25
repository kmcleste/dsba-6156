import streamlit as st

from common.uncc_logo import logo


def main():
    st.set_page_config(page_title="Home", page_icon="🏠")

    logo()

    st.markdown("# Welcome! 👋")

    # TODO: Make this sound better...
    st.markdown(
        """
        For the DSBA 6156: Applied Machine Learning project we created a neural-based search engine.
        This search engine leverages the open-source framework "Haystack" which enables us to perform
        semantic search, summarization, and text generation.

        ## Overview

        This is the overview section.

        ## Usage

        This is the usage section.

        ## Something

        This is another section that should probably have information but I can't think of anything atm.

    """
    )


if __name__ == "__main__":
    main()
