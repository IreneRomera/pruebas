#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 19:47:31 2026

@author: Prunebelly
"""

import streamlit as st
from datetime import datetime
from streamlit_extras.buy_me_a_coffee import button

st.set_page_config(
    page_title="Calculadoras para el manejo integral del tromboembolismo pulmonar (TEP)",
    layout="wide"
)
st.title("Calculadoras para el manejo integral del tromboembolismo pulmonar (TEP)")

st.subheader("⬅ Usa la barra lateral para introducir datos y elegir el cálculo")

# ------------------------------
# Funciones de cálculo de escalas
# ------------------------------

def interpretar_wells(puntuacion):
    if puntuacion <= 4:
        return "TEP improbable", "Considerar Dímero-D para ayudar a descartar TEP según el contexto clínico."
    else:
        return "TEP probable", "Considerar diagnóstico por imagen según el contexto clínico."


def render_wells():
    st.header("Escala de Wells para TEP")
    st.caption("Estimación de probabilidad clínica pretest en pacientes con sospecha de tromboembolismo pulmonar.")

    st.info(
        "Versión mostrada: modelo dicotómico de Wells para TEP. "
        "Interpretación: 4 puntos o menos = TEP improbable; más de 4 puntos = TEP probable.",
        icon="🩺"
    )

    with st.container(border=True):
        st.markdown("### Criterios clínicos")

        with st.form("form_wells"):
            c1, c2 = st.columns(2, gap="large")

            with c1:
                we1 = st.radio(
                    "Signos o síntomas clínicos de TVP",
                    ["No", "Sí"],
                    help="Incluye signos clínicos compatibles con trombosis venosa profunda.",
                    horizontal=True
                )

                we2 = st.radio(
                    "El TEP es el diagnóstico más probable",
                    ["No", "Sí"],
                    help="Equivale a que no existe una alternativa diagnóstica más probable.",
                    horizontal=True
                )

                we3 = st.radio(
                    "Inmovilización ≥ 3 días o cirugía en las últimas 4 semanas",
                    ["No", "Sí"],
                    horizontal=True
                )

                we4 = st.radio(
                    "Antecedente personal de TVP o TEP",
                    ["No", "Sí"],
                    horizontal=True
                )

            with c2:
                we5 = st.radio(
                    "Frecuencia cardiaca > 100 lpm",
                    ["No", "Sí"],
                    horizontal=True
                )

                we6 = st.radio(
                    "Hemoptisis",
                    ["No", "Sí"],
                    horizontal=True
                )

                we7 = st.radio(
                    "Cáncer activo o tratamiento paliativo",
                    ["No", "Sí"],
                    help="Puedes adaptar este texto después según el criterio exacto que quieras usar.",
                    horizontal=True
                )

            submitted = st.form_submit_button("Calcular Wells", use_container_width=True)

    if submitted:
        puntuacion = 0

        desglose = {
            "Signos o síntomas de TVP": 3 if we1 == "Sí" else 0,
            "TEP como diagnóstico principal": 3 if we2 == "Sí" else 0,
            "Inmovilización o cirugía reciente": 1.5 if we3 == "Sí" else 0,
            "Antecedente de TVP o TEP": 1.5 if we4 == "Sí" else 0,
            "FC > 100 lpm": 1.5 if we5 == "Sí" else 0,
            "Hemoptisis": 1 if we6 == "Sí" else 0,
            "Cáncer activo o paliativo": 1 if we7 == "Sí" else 0,
        }

        puntuacion = sum(desglose.values())
        categoria, recomendacion = interpretar_wells(puntuacion)

        st.markdown("### Resultado")

        r1, r2 = st.columns([1, 2], gap="large")

        with r1:
            st.metric("Puntuación total", puntuacion)

        with r2:
            if puntuacion <= 4:
                st.warning(f"**{categoria}**. {recomendacion}", icon="🟡")
            else:
                st.error(f"**{categoria}**. {recomendacion}", icon="🔴")

        with st.expander("Ver desglose de la puntuación"):
            for criterio, valor in desglose.items():
                st.write(f"- {criterio}: **{valor}** puntos")

        st.caption(
            "Esta calculadora es un apoyo a la decisión clínica y debe interpretarse en el contexto clínico completo."
        )
        
        
# ------------------------------
# Barra lateral: elegir cálculo
# ------------------------------

st.sidebar.markdown(
    """
    <h2 style='text-align: center; color: #800080;'>
        ¿Qué deseas calcular?
    </h2>
    """,
    unsafe_allow_html=True,
)

calculo = st.sidebar.selectbox(
    "Categoría",
    [
        "Escalas de probabilidad clínica (diagnóstico y toma de decisiones)",
        "Escalas de riesgo y pronóstico",
        "Tratamiento",
    ],
    index=None,
    placeholder="Elige una categoría"
)

# ------------------------------
# Escalas de probabilidad clínica
# ------------------------------
if calculo == "Escalas de probabilidad clínica (diagnóstico y toma de decisiones)":
    subcategoria = st.sidebar.selectbox(
        "Selecciona una escala",
        [
            "Escala de Wells",
            "Escala YEARS + Dímero-D",
        ],
        index=None,
        placeholder="Elige una escala"
    )

    if subcategoria == "Escala de Wells":
        render_wells()
    elif subcategoria == "Escala YEARS + Dímero-D":
        render_years()
    else:
        st.info("Selecciona una escala en la barra lateral para comenzar.")



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

