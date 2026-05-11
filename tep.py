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

if "categoria" not in st.session_state:
    st.session_state.categoria = None

st.title("Calculadoras para el manejo integral del tromboembolismo pulmonar (TEP)")

st.subheader("⬅ Usa la barra lateral para elegir el cálculo")


# ------------------------------
# Funciones de cálculo de escalas
# ------------------------------

def interpretar_wells(puntuacion):
    if puntuacion <= 2:
        return "TEP improbable", "Se aconseja revalorar el contexto clínico."
    elif 3 <= puntuacion <= 6:
        return "TEP poco probable", "Considerar escala Years y dímero-D para ayudar a descartar TEP según el contexto clínico."
    else:
        return "TEP muy probable", "Considerar diagnóstico por imagen."

def render_wells():
    st.header("Escala de Wells para TEP")
    st.caption("Estimación de probabilidad clínica pretest en pacientes con sospecha de tromboembolismo pulmonar.")

    st.info(
        "Versión mostrada: modelo de tres niveles de riesgo para TEP. "
        "Interpretación: 2 puntos o menos = TEP improbable; entre 3 y 6 puntos = TEP poco probable; más de 6 puntos = TEP muy probable.",
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
            if puntuacion <= 2:
                st.success(f"**{categoria}**. {recomendacion}", icon="🟢")
            elif 3 <= puntuacion <= 6:
                st.warning(f"**{categoria}**. {recomendacion}", icon="🟡")
            else:
                st.error(f"**{categoria}**. {recomendacion}", icon="🔴")

        with st.expander("Ver desglose de la puntuación"):
            for criterio, valor in desglose.items():
                st.write(f"- {criterio}: **{valor}** puntos")

        st.caption(
            "Esta calculadora es un apoyo a la decisión clínica y debe interpretarse en el contexto clínico completo."
        )
        
        
        
def interpretar_years(contyears, ddimero):
    if contyears >= 1:
        punto_corte = 500
        if ddimero < punto_corte:
            decision = "Se descarta el tromboembolismo pulmonar."
            estado = "descartado"
        else:
            decision = "Se recomienda realizar angio-TC."
            estado = "angio_tc"
    else:
        punto_corte = 1000
        if ddimero < punto_corte:
            decision = "Se descarta el tromboembolismo pulmonar."
            estado = "descartado"
        else:
            decision = "Se recomienda realizar angio-TC."
            estado = "angio_tc"

    return punto_corte, decision, estado


def render_years():
    st.header("Escala YEARS + Dímero-D")
    st.caption("Algoritmo diagnóstico simplificado para sospecha de TEP con punto de corte variable de Dímero-D.")

    st.info(
        "Regla YEARS: si no hay criterios YEARS, puede usarse un punto de corte de Dímero-D de 1000 ng/mL FEU; "
        "si existe 1 o más criterios YEARS, el punto de corte es 500 ng/mL FEU.",
        icon="🩺"
    )

    with st.container(border=True):
        st.markdown("### Datos clínicos")

        with st.form("form_years"):
            ddimero = st.number_input(
                "Dímero-D (ng/mL, FEU)",
                min_value=0.0,
                value=500,
                placeholder="Introduce el valor del Dímero-D",
                step=10.0,
                format="%.0f",
                help="Si tu laboratorio informa en DDU, recuerda que aproximadamente DDU = FEU / 2."
            )

            c1, c2, c3 = st.columns(3, gap="large")

            with c1:
                years1 = st.radio(
                    "Signos o síntomas de TVP",
                    ["No", "Sí"],
                    horizontal=True
                )

            with c2:
                years2 = st.radio(
                    "El TEP es la principal sospecha diagnóstica",
                    ["No", "Sí"],
                    horizontal=True
                )

            with c3:
                years3 = st.radio(
                    "Hemoptisis",
                    ["No", "Sí"],
                    horizontal=True
                )

            submitted = st.form_submit_button("Calcular YEARS + Dímero-D", use_container_width=True)

    if submitted:
        if ddimero is None:
            st.error("Introduce un valor de Dímero-D para poder calcular el resultado.", icon="⚠️")
            return

        desglose = {
            "Signos o síntomas de TVP": 1 if years1 == "Sí" else 0,
            "TEP como principal sospecha diagnóstica": 1 if years2 == "Sí" else 0,
            "Hemoptisis": 1 if years3 == "Sí" else 0,
        }

        contyears = sum(desglose.values())
        punto_corte, decision, estado = interpretar_years(contyears, ddimero)

        st.markdown("### Resultado")

        r1, r2, r3 = st.columns(3, gap="large")

        with r1:
            st.metric("Criterios YEARS", contyears)

        with r2:
            st.metric("Dímero-D", f"{ddimero:.0f} ng/mL")

        with r3:
            st.metric("Punto de corte aplicado", f"{punto_corte} ng/mL")

        if estado == "descartado":
            st.success(f"**Resultado:** {decision}", icon="✅")
        else:
            st.warning(f"**Resultado:** {decision}", icon="📌")

        if contyears == 0:
            st.caption(
                "No hay criterios YEARS positivos, por lo que se aplica un umbral de Dímero-D de 1000 ng/mL FEU."
            )
        else:
            st.caption(
                "Hay 1 o más criterios YEARS positivos, por lo que se aplica un umbral de Dímero-D de 500 ng/mL FEU."
            )

        with st.expander("Ver desglose de criterios YEARS"):
            for criterio, valor in desglose.items():
                st.write(f"- {criterio}: **{valor}**")

        st.caption(
            "Esta calculadora es una ayuda a la toma de decisiones y debe interpretarse junto con el contexto clínico completo."
        )     
        
        
        

# ------------------------------
# Barra lateral: botones de categoría
# ------------------------------

st.sidebar.markdown(
    """
    <h2 style='text-align: center; color: #800080;'>
        ¿Qué deseas calcular?
    </h2>
    """,
    unsafe_allow_html=True,
)

if st.sidebar.button("Escalas de probabilidad clínica", use_container_width=True):
    st.session_state.categoria = "probabilidad"

if st.sidebar.button("Escalas de riesgo y pronóstico", use_container_width=True):
    st.session_state.categoria = "riesgo"

if st.sidebar.button("Tratamiento", use_container_width=True):
    st.session_state.categoria = "tratamiento"


# ------------------------------
# Contenido principal según categoría
# ------------------------------

if st.session_state.categoria == "probabilidad":
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
        st.info("Selecciona una escala de probabilidad clínica en la barra lateral.")



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

