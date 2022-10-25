import pathlib
from PIL import Image

import streamlit as st
from streamlit.components.v1 import html

path = pathlib.Path("src", "ui", "common", "uncc_white_logo.png")
image = Image.open(path)


def logo():
    with st.sidebar:
        st.image(image=image, output_format="PNG")
