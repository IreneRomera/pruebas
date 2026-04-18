#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 17:03:42 2026

@author: Prunebelly
"""

"""
Calculadora NEWS-2 adaptado al Hospital de Barcelona
App Streamlit minimalista
"""

import streamlit as st

# Configuración de página
st.set_page_config(
    page_title="NEWS-2 Hospital de Barcelona",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para sidebar turquesa claro (más claro que Pantone 319 C #2DCCD3 -> #A0E8ED)
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

# Título principal
st.title("🏥 NEWS-2 adaptado al Hospital de Barcelona")

# Sidebar para inputs
with st.sidebar:
    st.markdown("### 📊 Introducir datos del paciente")
    
    # Input a: Soporte O2
    a = st.selectbox(
        "¿Precisa soporte con O₂?",
        options=[None, 1, 2],
        format_func=lambda x: "1.- No" if x == 1 else "2.- Sí" if x == 2 else "Selecciona...",
        index=0
    )
    
    # Input b: Frecuencia respiratoria
    b = st.number_input("Frecuencia respiratoria (rpm)", min_value=0, max_value=60, value=0, step=1)
    
    # Input c: Tipo de insuficiencia respiratoria
    c = st.selectbox(
        "¿Paciente con...?",
        options=[None, 1, 2],
        format_func=lambda x: "1.- Insuficiencia respiratoria hipoxémica" if x == 1 else "2.- Hipercápnica" if x == 2 else "Selecciona...",
        index=0
    )
    
    # Input d: SpO2
    d = st.number_input("SpO₂ (%)", min_value=0, max_value=100, value=0, step=1)
    
    # Input e: PAs
    e = st.number_input("PAs (mmHg)", min_value=0, max_value=300, value=0, step=1)
    
    # Input f: FC
    f = st.number_input("Frecuencia cardiaca (lpm)", min_value=0, max_value=300, value=0, step=1)
    
    # Input g: Temperatura
    g = st.number_input("Temperatura (ºC)", min_value=20.0, max_value=45.0, value=36.5, step=0.1)
    
    # Input h: Nivel de consciencia
    h = st.selectbox(
        "¿Alteración del nivel de consciencia?",
        options=[None, 1, 2],
        format_func=lambda x: "1.- No" if x == 1 else "2.- Sí" if x == 2 else "Selecciona...",
        index=0
    )
    
    # Botones
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔢 CALCULAR", use_container_width=True):
            st.session_state.calcular = True
    with col2:
        if st.button("🔄 RESETEAR", use_container_width=True):
            st.session_state = {"calcular": False, "score": None, "riesgo": None}
    
    st.markdown("---")
    st.markdown("*App desarrollada para uso clínico interno*")

# Función de cálculo (lógica original corregida y optimizada)
@st.cache_data
def calcular_news2(a, b, c, d, e, f, g, h):
    if None in (a, b, c, d, e, f, g, h):
        return None, None
    
    contador = 0
    
    # a: Soporte O2
    if a == 2:
        contador += 2
    # elif a == 1: +0
    
    # b: Frecuencia respiratoria
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
    
    # d: SpO2 con c
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
    
    # e: PAs
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
    
    # f: FC
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
    
    # g: Temperatura
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
    
    # h: Conciencia
    if h == 2:
        contador += 3
    
    # Interpretación
    if contador >= 5:
        riesgo = "⚠️ **Riesgo ALTO** - Valoración EMERGENTE (<1h). Avisar Medicina Intensiva (6457)"
    elif 4 <= contador <= 4:
        riesgo = "⚠️ **Riesgo MODERADO** - Valoración PRIORITARIA (2h). Avisar médico responsable"
    elif 1 <= contador <= 3:
        riesgo = "ℹ️ **Riesgo BAJO** - Valoración en 6h. Seguimiento"
    else:
        riesgo = "✅ **Sin riesgo** - Observación rutinaria"
    
    return contador, riesgo

# Lógica principal
if "calcular" not in st.session_state:
    st.session_state.calcular = False
    st.session_state.score = None
    st.session_state.riesgo = None

if st.session_state.calcular:
    score, riesgo = calcular_news2(a, b, c, d, e, f, g, h)
    if score is not None:
        st.session_state.score = score
        st.session_state.riesgo = riesgo
    else:
        st.session_state.score = None
        st.error("❌ Completa todos los campos antes de calcular")

# Mostrar resultado en área central
if st.session_state.score is not None:
    st.markdown(f'<div class="main-result">{st.session_state.score}</div>', unsafe_allow_html=True)
    st.markdown(f"### {st.session_state.riesgo}")
    
    # Tabla resumen
    st.subheader("📋 Resumen de parámetros")
    data = {
        "Parámetro": ["O₂", "FR (rpm)", "Tipo IR", "SpO₂ (%)", "PAs", "FC", "Temp (°C)", "Conciencia"],
        "Valor": [f"{a}", f"{b}", f"{c}", f"{d}", f"{e}", f"{f}", f"{g}", f"{h}"]
    }
    st.table(data)
else:
    st.info("👆 Introduce los datos en la barra lateral y pulsa **CALCULAR**")

# Footer
st.markdown("---")
st.markdown("*Desarrollado para uso clínico. Validar siempre con criterio médico.*")
