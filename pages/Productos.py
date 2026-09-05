import streamlit as st

st.set_page_config(page_title="Productos", layout="wide")
if st.button("Volver a Principal"):
    st.switch_page("app.py")


st.title("🥤 Productos")