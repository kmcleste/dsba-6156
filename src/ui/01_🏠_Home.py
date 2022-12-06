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
        semantic search, summarization, and various other NLP-related tasks.

        ## Table of Contents

        1. Home (⭐️ you are here)
        2. [Upload Files](http://127.0.0.1:8501/Upload_Files)
            - Upload txt, pdf, docx, and md files to search database
        3. [Index Viewer](http://127.0.0.1:8501/Index_Viewer)
            - See database metrics and explore the indexed documents
        4. [Search](http://127.0.0.1:8501/Search)
            - Perform natural-language semantic search across the index
        5. [Generation](http://127.0.0.1:8501/%EF%B8%8F_Generation)
            - Generate potential questions that the search engine will attempt to answer
        6. [Admin Panel](http://127.0.0.1:8501/Admin_Panel)
            - API status

    """
    )


if __name__ == "__main__":
    main()
