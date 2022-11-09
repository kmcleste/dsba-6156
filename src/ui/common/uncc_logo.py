import os
import pathlib
from PIL import Image

import streamlit as st

path = pathlib.Path(os.getcwd(), "ui", "common", "uncc_white_logo.png")
image = Image.open(path)


def logo():
    with st.sidebar:
        st.image(image=image, output_format="PNG")
