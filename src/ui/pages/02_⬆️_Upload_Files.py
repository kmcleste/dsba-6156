import streamlit as st

from common.uncc_logo import logo
from common.requests_common import Request


def main():
    st.set_page_config(page_title="Upload Files", page_icon="⬆️")

    logo()

    st.markdown("# Upload Files")

    with st.form(key="upload-file-form"):
        st.selectbox(label="Index", key="upload-index", options=["semantic"])
        st.file_uploader(
            label="Upload File(s)",
            key="file-uploader",
            accept_multiple_files=True,
            type=["TXT", "PDF", "DOCX", "MD"],
        )

        submit: bool = st.form_submit_button(label="Process")

        if submit:
            if st.session_state.get("file-uploader"):
                with st.spinner(text="⬆️ Uploading files..."):
                    upload_files_kwargs: dict = {
                        "files": {
                            "files": x for x in st.session_state.get("file-uploader")
                        }
                    }
                    r = Request.post(endpoint="/upload-files", **upload_files_kwargs)
                if r:
                    st.write(r.json().get("message"))


if __name__ == "__main__":
    main()
