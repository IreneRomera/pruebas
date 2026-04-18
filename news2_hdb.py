#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import streamlit as st
from streamlit_extras.buy_me_a_coffee import button

st.set_page_config(
    page_title="NEWS-2 Hospital de Barcelona",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.sidebar .sidebar-content {
    background-color: #A0E8ED !important;
}
.stButton > button {
    background-color: #2DCCD3;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px 20px;
    font-weight: bold;
}
.stButton > button:hover {
    background-color: #1ABCB8;
}
.main-result {
    font-size: 8rem !important;
    font-weight: bold !important;
    text-align: center;
    color: #2DCCD3 !important;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}
</style>
""", unsafe_allow_html=True)

if "score" not in st.session_state:
    st.session_state["score"] = False
if "riesgo" not in st.session_state:
    st.session_state["riesgo"] = None


st.title("🏥 NEWS-2 adaptado al Hospital de Barcelona 🏥")

def resetear():
    for k in ["a", "b", "c", "d", "e", "f", "g", "h", "score", "riesgo"]:
        if k in st.session_state:
            del st.session_state[k]
    st.rerun()

@st.cache_data
def calcular_news2(a, b, c, d, e, f, g, h):
    if None in (a, b, c, d, e, f, g, h):
        return None, None

    contador = 0

    if a == 2:
        contador += 2

    if 12 <= b <= 20:
        contador += 0
    elif 21 <= b <= 24:
        contador += 2
    elif b > 24:
        contador += 3
    elif 9 <= b <= 11:
        contador += 1
    elif b < 9:
        contador += 3

    if c == 1:
        if d > 95:
            contador += 0
        elif 94 <= d <= 95:
            contador += 1
        elif 92 <= d <= 93:
            contador += 2
        elif d < 92:
            contador += 3
    elif c == 2:
        if d > 96:
            contador += 3
        elif 95 <= d <= 96:
            contador += 2
        elif 93 <= d <= 94:
            contador += 1
        elif 88 <= d <= 92:
            contador += 0
        elif 86 <= d <= 87:
            contador += 1
        elif 84 <= d <= 85:
            contador += 2
        elif d < 84:
            contador += 3

    if e > 219:
        contador += 3
    elif 111 <= e <= 219:
        contador += 0
    elif 101 <= e <= 110:
        contador += 1
    elif 91 <= e <= 100:
        contador += 2
    elif e < 91:
        contador += 3

    if f > 130:
        contador += 3
    elif 111 <= f <= 130:
        contador += 2
    elif 91 <= f <= 110:
        contador += 1
    elif 51 <= f <= 90:
        contador += 0
    elif 41 <= f <= 50:
        contador += 1
    elif f < 41:
        contador += 3

    if g > 39:
        contador += 2
    elif 38.1 <= g <= 39:
        contador += 1
    elif 36.1 <= g <= 38:
        contador += 0
    elif 35.1 <= g <= 36:
        contador += 1
    elif g < 35.1:
        contador += 3

    if h == 2:
        contador += 3

    if contador >= 5:
        riesgo = "⚠️ Riesgo ALTO - Valoración emergente (<1h). Avisar Medicina Intensiva (6457)"
    elif contador == 4:
        riesgo = "⚠️ Riesgo MODERADO - Valoración prioritaria (2h). Avisar médico responsable"
    elif 1 <= contador <= 3:
        riesgo = "ℹ️ Riesgo BAJO - Valoración en 6h. Seguimiento"
    else:
        riesgo = "✅ Sin riesgo - Observación rutinaria"

    return contador, riesgo

with st.sidebar:
    st.markdown("### 📊 Introducir datos clínicos del paciente")

    a = st.selectbox(
        "¿Precisa soporte con O₂?",
        options=[None, 1, 2],
        format_func=lambda x: "No" if x == 1 else "Sí" if x == 2 else "Selecciona...",
        index=0,
        key="a"
    )

    b = st.number_input("Frecuencia respiratoria (rpm)", min_value=0, max_value=45, value=15, step=1, key="b")

    c = st.selectbox(
        "¿Paciente con enfermedad pulmonar obstructiva crónica (EPOC)?",
        options=[None, 1, 2],
        format_func=lambda x: "No" if x == 1 else "Sí" if x == 2 else "Selecciona...",
        index=0,
        key="c"
    )

    d = st.number_input("SpO₂ (%)", min_value=0, max_value=100, value=95, step=1, key="d")
    e = st.number_input("PAs (mmHg)", min_value=0, max_value=350, value=120, step=1, key="e")
    f = st.number_input("Frecuencia cardiaca (lpm)", min_value=0, max_value=250, value=80, step=1, key="f")
    g = st.number_input("Temperatura (ºC)", min_value=30.0, max_value=45.0, value=36.5, step=0.1, key="g")

    h = st.selectbox(
        "¿Existe alteración del nivel de consciencia?",
        options=[None, 1, 2],
        format_func=lambda x: "No" if x == 1 else "Sí" if x == 2 else "Selecciona...",
        index=0,
        key="h"
    )

    col1, col2 = st.columns(2)
    with col1:
        calcular = st.button("🔢 CALCULAR", use_container_width=True)
    with col2:
        st.button("🔄 RESETEAR", use_container_width=True, on_click=resetear)

    st.markdown("---")
    st.markdown("*App desarrollada para uso clínico interno*")

if calcular:
    score, riesgo = calcular_news2(a, b, c, d, e, f, g, h)
    if score is None:
        st.error("❌ Completa todos los campos antes de calcular.")
    else:
        st.session_state.score = score
        st.session_state.riesgo = riesgo

if "score" in st.session_state and st.session_state.score is not None:
    st.markdown(f'<div class="main-result">{st.session_state.score}</div>', unsafe_allow_html=True)
    st.markdown(f"### {st.session_state.riesgo}")

    st.subheader("📋 Resumen de parámetros")
    data = {
        "Parámetro": ["O₂", "FR (rpm)", "EPOC", "SpO₂ (%)", "PAs", "FC", "Temp (°C)", "Conciencia"],
        "Valor": [a, b, c, d, e, f, g, h]
    }
    st.table(data)
else:
    st.info("👆 Introduce los datos en la barra lateral y pulsa CALCULAR.")

st.markdown("---")
st.markdown("*Desarrollado para uso clínico. Validar siempre con criterio médico.*")

st.caption("App desarrollada por Irene Romera / irene.r.s@outlook.com")
st.write("Si esta calculadora te resulta útil …")

button(
    username="ireneromera",
    floating=False,
    text="Invítame a un té",
    emoji="🫖",
    bg_color="#C084FC",
    font_color="#FFFFFF"
)
