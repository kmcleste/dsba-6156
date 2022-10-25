from io import StringIO

import streamlit as st

from common.uncc_logo import logo


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
                for file in st.session_state["file-uploader"]:
                    try:
                        if ".txt" in file.name:
                            content: dict = {
                                "name": file.name,
                                "type": file.type,
                                "size (KB)": file.size / 1000,  # convert to kilobytes
                                "head": StringIO(
                                    file.getvalue().decode("utf-8")
                                ).read()[
                                    :500
                                ],  # print the first 500 chars of txt
                            }
                        else:
                            content: dict = {
                                "name": file.name,
                                "type": file.type,
                                "size": file.size / 1000,
                            }
                        st.write(content)
                    except Exception:
                        st.error(f"Unable to process {file.name}")
                    finally:
                        file.close()


if __name__ == "__main__":
    main()
