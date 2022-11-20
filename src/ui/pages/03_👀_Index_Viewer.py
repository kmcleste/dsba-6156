import pandas as pd
import streamlit as st

from common.uncc_logo import logo
from common.requests_common import Request


def main():
    st.set_page_config(page_title="Index Viewer", page_icon="👀", layout="wide")

    logo()

    st.markdown("# Index Viewer")

    metrics_kwargs: dict = {"json": {"index": "semantic"}}

    metrics = Request.post(endpoint="/describe-documents", **metrics_kwargs)

    if metrics is not None:
        if isinstance(metrics.json(), dict):
            metrics: dict = metrics.json()
            col1, col2, col3 = st.columns(3)

            col1.metric(label="Documents", value=metrics.get("count"))
            col2.metric(label="Average Characters", value=metrics.get("chars_mean"))
            col3.metric(label="Maximum Characters", value=metrics.get("chars_max"))
            col1.metric(label="Minimum Characters", value=metrics.get("chars_min"))
            col2.metric(label="Median Characters", value=metrics.get("chars_median"))

    fetch_kwargs: dict = {"json": {"index": "semantic"}}

    docs = Request.post(endpoint="/fetch-documents", **fetch_kwargs)

    if docs is not None:
        st.markdown("## Documents in Index")
        if docs.json().get("documents"):
            df: pd.DataFrame = pd.DataFrame(data=docs.json()["documents"])
            st.dataframe(df[["id", "content"]], use_container_width=True)
        else:
            st.info("No documents in the index")


if __name__ == "__main__":
    main()
