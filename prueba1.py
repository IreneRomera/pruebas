import streamlit as st

st.sidebar.header("Datos del paciente")

edad = st.sidebar.number_input(
    "Edad",
    min_value=0,
    max_value=120,
    step=1
)

genero = st.sidebar.radio(
    "Género",
    options=["H - Hombre", "M - Mujer"]
)

pesokg = st.sidebar.number_input(
    "Peso (kg)",
    min_value=0.0,
    max_value=400.0,
    step=0.1
)

tallacm = st.sidebar.number_input(
    "Talla (cm)",
    min_value=0.0,
    max_value=250.0,
    step=0.1
)
