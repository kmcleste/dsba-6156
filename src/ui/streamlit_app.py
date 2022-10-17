import streamlit as st

st.markdown("# Welcome!")

st.text_input(label="Query", key="query")

st.write(st.session_state.get("query"))
