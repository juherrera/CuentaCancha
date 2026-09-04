import streamlit as st

st.set_page_config(page_title="Historial Cuentas Pagadas", layout="wide")
if st.button("Volver a cuentas"):
    st.switch_page("app.py")


st.title("📙 Historial de Cuentas Pagadas")