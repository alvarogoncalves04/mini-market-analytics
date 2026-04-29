import streamlit as st

def mostrar(df_filtrado):
    st.markdown("<h1>🗂️ Datos Completos</h1>", unsafe_allow_html=True)
    st.dataframe(df_filtrado, use_container_width=True, height=500)