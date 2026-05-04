#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  4 19:46:44 2026

@author: Prunebelly
"""

import streamlit as st
from datetime import datetime
from streamlit_extras.buy_me_a_coffee import button
from PIL import Image 

st.set_page_config(page_title="Calculadora de escala de fragilidad")

st.title("Calculadora del Clinical Frailty Scale (CFS) como escala de fragilidad validad en adultos de edad igual o superior a 65 años.")
st.subheader("⬅ Usa la barra lateral para introducir datos y elegir el cálculo")

# ======================
# Imagen centrada CFS
# ======================
# Carga la imagen (pon el fichero en la misma carpeta que tu script)
imagen_cfs = Image.open("CFS-espana.jpeg")

# Creamos tres columnas y usamos la del centro
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image(imagen_cfs, use_column_width=True, caption="Clinical Frailty Scale - España")
    

# ------------------------------
# Funciones de cálculo de SCOREs
# ------------------------------

def calcular_cfs_por_preguntas(c1, c2, c3, c4):
    """
    Implementa tu lógica original:
    - c1: patología de base (1-4; si 4 → CFS=9)
    - c2: AIVD (1-3)
    - c3: ABVD (1-3)
    - c4: ejercicio (1-5)
    Devuelve (cfs, texto_descriptivo).
    """
    if c1 == 4:
        return 9, "CFS 9. Paciente terminal."

    contador = 0

    # c1
    if c1 == 1:
        contador += 0
    elif c1 == 2:
        contador += 1
    elif c1 == 3:
        contador += 2

    # c2
    if c2 == 1:
        contador += 0
    elif c2 == 2:
        contador += 1
    elif c2 == 3:
        contador += 2

    # c3
    if c3 == 1:
        contador += 0
    elif c3 == 2:
        contador += 1
    elif c3 == 3:
        contador += 2

    # c4
    if c4 == 1:
        contador += 0
    elif c4 == 2:
        contador += 2
    elif c4 == 3:
        contador += 3
    elif c4 == 4:
        contador += 4
    elif c4 == 5:
        contador += 5

    # Traducción a categoría CFS
    if contador == 0:
        return 0, "CFS 1. Paciente en óptimo estado de salud."
    elif contador == 1:
        return 1, "CFS 1. Paciente en óptimo estado de salud."
    elif contador in (2, 3):
        return 2, "CFS 2. Paciente con buen estado de salud."
    elif contador == 4:
        return 3, "CFS 3. Paciente con buena autonomía."
    elif contador in (5, 6):
        return 4, "CFS 4. Paciente vulnerable."
    elif contador == 7:
        return 5, "CFS 5. Paciente ligeramente frágil."
    elif contador in (8, 9):
        return 6, "CFS 6. Paciente moderadamente frágil."
    elif contador == 10:
        return 7, "CFS 7. Paciente gravemente frágil."
    elif contador == 11:
        return 8, "CFS 8. Paciente severamente frágil."
    else:
        return None, "No se ha podido asignar un CFS con esta combinación."


def calcular_cfs_simplificado(opcion):
    """
    Recibe un código de opción (f1..f9) y devuelve (cfs, descripción).
    El orden respeta el flowchart clásico del CFS: la primera opción aplicable marca el CFS.
    """

    mapa = {
        "f1": (9, "CFS 9. Paciente terminal."),
        "f2": (8, "CFS 8. Paciente severamente frágil."),
        "f3": (7, "CFS 7. Paciente gravemente frágil."),
        "f4": (6, "CFS 6. Paciente moderadamente frágil."),
        "f5": (5, "CFS 5. Paciente ligeramente frágil."),
        "f6": (4, "CFS 4. Paciente vulnerable."),
        "f7": (3, "CFS 3. Paciente con buena autonomía."),
        "f8": (2, "CFS 2. Paciente con buen estado de salud."),
        "f9": (1, "CFS 1. Paciente en óptimo estado de salud."),
    }

    return mapa.get(opcion, (None, "No se ha podido asignar un CFS simplificado con esta opción."))



# ------------------------------
# Barra lateral: elegir tipo de cálculo
# ------------------------------

st.sidebar.markdown(
    """
    <h2 style='text-align: center; color: #003366;'>
        ¿Con qué método quieres hacer el cálculo?
    </h2>
    """,
    unsafe_allow_html=True,
)

score_elegido = st.sidebar.selectbox(
    "",
    [
        "Clinical Frailty Scale (CFS) basado en preguntas",
        "Clinical Frailty Scale (CFS) flowchart",
    ],
)


# ------------------------------
# Clinical Frailty Scale (CFS)
# ------------------------------
if score_elegido == "Clinical Frailty Scale (CFS) basado en preguntas":
    st.sidebar.subheader("Responda respecto a la situación del paciente en las últimas 2 semanas)")

    c1 = st.sidebar.selectbox(
        "Patología de base",
        options=[
            "1 - No hay",
            "2 - Está bien controlada",
            "3 - Descompensaciones frecuentes",
            "4 - Enfermedad en fase terminal",
        ],
    )
    c2 = st.sidebar.selectbox(
        "Dependencia para AIVD",
        options=[
            "1 - Totalmente independiente",
            "2 - Precisa ayuda",
            "3 - Totalmente dependiente",
        ],
    )
    c3 = st.sidebar.selectbox(
        "Dependencia para ABVD",
        options=[
            "1 - Totalmente independiente",
            "2 - Precisa ayuda",
            "3 - Totalmente dependiente",
        ],
    )
    c4 = st.sidebar.selectbox(
        "Ejercicio físico habitual",
        options=[
            "1 - Paciente deportista",
            "2 - Ejercicio ocasional (más que caminar)",
            "3 - Ejercicio limitado",
            "4 - Vida limitada",
            "5 - No realiza ejercicio (frágil)",
        ],
    )

    boton_cfs = st.sidebar.button("Calcular CFS")

    if boton_cfs:
        # Extraer el número inicial de cada opción
        c1_val = int(c1.split(" ")[0])
        c2_val = int(c2.split(" ")[0])
        c3_val = int(c3.split(" ")[0])
        c4_val = int(c4.split(" ")[0])

        cfs, descripcion = calcular_cfs_por_preguntas(c1_val, c2_val, c3_val, c4_val)

        st.subheader("Clinical Frailty Scale (CFS)")
        if cfs is not None:
            st.write(f"El Clinical Frailty Score es de **{cfs}** puntos")
        st.info(descripcion)


# ------------------------------
# CFS simplificado (flowchart)
# ------------------------------
if score_elegido == "Clinical Frailty Scale (CFS) flowchart":
    st.markdown("---")
    st.subheader("CFS simplificado (flowchart)")


    # Menú desplegable en la zona central
    opcion_cfs_simpl = st.selectbox(
        "Responda respecto a la situación del paciente en las últimas 2 semanas:",
        options=[
            "Enfermedad terminal con expectativa de vida < 6 meses",
            "Completamente dependiente y se aproxima al final de su vida",
            "Completamente dependiente para el cuidado personal y ABVD",
            "Necesita ayuda con todas las actividades fuera de casa, hogar y/o baño",
            "Necesita ayuda para AIVD (finanzas, transporte, hogar, comida, medicación)",
            "No es dependiente pero los síntomas limitan su vida diaria",
            "Problemas de salud bien controlados pero no realiza ejercicio físico más allá de caminar",
            "Sin síntomas activos y realiza ejercicio ocasional",
            "Realiza ejercicio regular y está más ágil/'fit' de lo esperado para su edad",
        ],
    )

    # Mapear texto a código f1..f9
    mapa_opciones_a_codigo = {
        "Enfermedad terminal con expectativa de vida < 6 meses": "f1",
        "Completamente dependiente y se aproxima al final de su vida": "f2",
        "Completamente dependiente para el cuidado personal y ABVD": "f3",
        "Necesita ayuda con todas las actividades fuera de casa, hogar y/o baño": "f4",
        "Necesita ayuda para AIVD (finanzas, transporte, hogar, comida, medicación)": "f5",
        "No es dependiente pero los síntomas limitan su vida diaria": "f6",
        "Problemas de salud bien controlados pero no realiza ejercicio físico más allá de caminar": "f7",
        "Sin síntomas activos y realiza ejercicio ocasional": "f8",
        "Realiza ejercicio regular y está más ágil/'fit' de lo esperado para su edad": "f9",
    }

    codigo = mapa_opciones_a_codigo[opcion_cfs_simpl]

    cfs_simpl, desc_simpl = calcular_cfs_simplificado(codigo)

    st.info(desc_simpl)


st.markdown("---")
st.caption("App desarrollada por Irene Romera / irene.r.s@outlook.com")
st.write("Si esta calculadora te resulta útil …")

button(
    username="ireneromera",
    floating=False,
    text="Invítame a un té",
    emoji="🫖",
    bg_color="#C084FC",
    font_color="#FFFFFF",
)





