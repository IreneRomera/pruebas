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
                value=None,
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
        

def interpretar_pesi(puntuacion):
    if puntuacion <= 65:
        return "Clase I", "Riesgo bajo", "La puntuación sugiere bajo riesgo."
    elif 66 <= puntuacion <= 85:
        return "Clase II", "Riesgo bajo", "La puntuación sugiere bajo riesgo."
    elif 86 <= puntuacion <= 105:
        return "Clase III", "Riesgo elevado", "La puntuación sugiere riesgo intermedio."
    elif 106 <= puntuacion <= 125:
        return "Clase IV", "Riesgo elevado", "La puntuación sugiere riesgo elevado."
    else:
        return "Clase V", "Riesgo elevado", "La puntuación sugiere riesgo muy elevado."


def render_pesi():
    st.header("PESI")
    st.caption("Pulmonary Embolism Severity Index para estratificación pronóstica en TEP agudo.")

    st.info(
        "El PESI original utiliza edad, sexo, comorbilidades y variables clínicas para clasificar el riesgo en cinco clases pronósticas.",
        icon="🩺"
    )

    with st.container(border=True):
        st.markdown("### Datos clínicos")

        with st.form("form_pesi"):
            c0, c1 = st.columns([1, 1], gap="large")

            with c0:
                edad = st.number_input(
                    "Edad (años)",
                    min_value=0,
                    max_value=120,
                    value=None,
                    placeholder="Introduce la edad",
                    step=1
                )

                sexo = st.selectbox(
                    "Sexo",
                    ["Mujer", "Hombre"],
                    index=None,
                    placeholder="Selecciona una opción"
                )

            with c1:
                st.caption("Antecedentes y situación clínica")

            c2, c3 = st.columns(2, gap="large")

            with c2:
                pesi1 = st.radio("Antecedentes de cáncer", ["No", "Sí"], horizontal=True)
                pesi2 = st.radio("Antecedentes de insuficiencia cardiaca", ["No", "Sí"], horizontal=True)
                pesi3 = st.radio("Antecedentes de enfermedad pulmonar crónica", ["No", "Sí"], horizontal=True)
                pesi4 = st.radio("Frecuencia cardiaca ≥ 110 lpm", ["No", "Sí"], horizontal=True)
                pesi5 = st.radio("Presión arterial sistólica < 100 mmHg", ["No", "Sí"], horizontal=True)

            with c3:
                pesi6 = st.radio("Frecuencia respiratoria ≥ 30 rpm", ["No", "Sí"], horizontal=True)
                pesi7 = st.radio("Saturación de oxígeno < 90 %", ["No", "Sí"], horizontal=True)
                pesi8 = st.radio("Temperatura < 36 ºC", ["No", "Sí"], horizontal=True)
                pesi9 = st.radio("Alteración del estado de consciencia", ["No", "Sí"], horizontal=True)

            submitted = st.form_submit_button("Calcular PESI", use_container_width=True)

    if submitted:
        if edad is None:
            st.error("Introduce la edad del paciente.", icon="⚠️")
            return

        if sexo is None:
            st.error("Selecciona el sexo del paciente.", icon="⚠️")
            return

        desglose = {
            "Edad": edad,
            "Sexo masculino": 10 if sexo == "Hombre" else 0,
            "Cáncer": 30 if pesi1 == "Sí" else 0,
            "Insuficiencia cardiaca": 10 if pesi2 == "Sí" else 0,
            "Enfermedad pulmonar crónica": 10 if pesi3 == "Sí" else 0,
            "FC ≥ 110 lpm": 20 if pesi4 == "Sí" else 0,
            "PAs < 100 mmHg": 30 if pesi5 == "Sí" else 0,
            "FR ≥ 30 rpm": 20 if pesi6 == "Sí" else 0,
            "SatO2 < 90 %": 20 if pesi7 == "Sí" else 0,
            "Temperatura < 36 ºC": 20 if pesi8 == "Sí" else 0,
            "Alteración del estado de consciencia": 60 if pesi9 == "Sí" else 0,
        }

        puntuacion = sum(desglose.values())
        clase, riesgo, recomendacion = interpretar_pesi(puntuacion)

        st.markdown("### Resultado")

        r1, r2, r3 = st.columns(3, gap="large")

        with r1:
            st.metric("Puntuación total", int(puntuacion))

        with r2:
            st.metric("Clase PESI", clase)

        with r3:
            st.metric("Estrato", riesgo)

        if puntuacion <= 85:
            st.success(f"**{clase}**. {riesgo}. {recomendacion}", icon="🟢")
        elif 86 <= puntuacion <= 105:
            st.warning(f"**{clase}**. {riesgo}. {recomendacion}", icon="🟡")
        else:
            st.error(f"**{clase}**. {riesgo}. {recomendacion}", icon="🔴")

        with st.expander("Ver desglose de la puntuación"):
            for criterio, valor in desglose.items():
                st.write(f"- {criterio}: **{valor}** puntos")

        st.caption(
            "El PESI es una herramienta pronóstica y debe integrarse con la evaluación hemodinámica, la función ventricular derecha y el juicio clínico."
        )


def interpretar_pesi_simp(puntuacion):
    if puntuacion == 0:
        return (
            "sPESI = 0",
            "Riesgo bajo",
            "Mortalidad estimada a 30 días aproximadamente del 1,1%. Puede apoyar la consideración de manejo ambulatorio en pacientes seleccionados."
        )
    else:
        return (
            f"sPESI = {puntuacion}",
            "Riesgo elevado",
            "sPESI ≥ 1. Mortalidad a 30 días más elevada; valorar manejo hospitalario y estratificación adicional según el contexto clínico."
        )


def render_pesi_simp():
    st.header("PESI simplificado")
    st.caption("Simplified Pulmonary Embolism Severity Index (sPESI) para estratificación pronóstica en TEP agudo.")

    st.info(
        "El sPESI asigna 1 punto a cada criterio presente. "
        "Interpretación: 0 puntos = bajo riesgo; 1 o más puntos = riesgo elevado.",
        icon="🩺"
    )

    with st.container(border=True):
        st.markdown("### Datos clínicos")

        with st.form("form_pesi_simp"):
            c1, c2 = st.columns(2, gap="large")

            with c1:
                edad = st.number_input(
                    "Edad (años)",
                    min_value=0,
                    max_value=120,
                    value=None,
                    placeholder="Introduce la edad",
                    step=1
                )

                ps1 = st.radio(
                    "Antecedentes de cáncer",
                    ["No", "Sí"],
                    horizontal=True
                )

                ps2 = st.radio(
                    "Antecedentes de enfermedad cardiopulmonar crónica",
                    ["No", "Sí"],
                    help="Incluye insuficiencia cardiaca crónica y/o enfermedad pulmonar crónica.",
                    horizontal=True
                )

                ps3 = st.radio(
                    "Frecuencia cardiaca ≥ 110 lpm",
                    ["No", "Sí"],
                    horizontal=True
                )

            with c2:
                ps4 = st.radio(
                    "Presión arterial sistólica < 100 mmHg",
                    ["No", "Sí"],
                    horizontal=True
                )

                ps5 = st.radio(
                    "Saturación de oxígeno < 90 %",
                    ["No", "Sí"],
                    horizontal=True
                )

            submitted = st.form_submit_button("Calcular sPESI", use_container_width=True)

    if submitted:
        if edad is None:
            st.error("Introduce la edad del paciente.", icon="⚠️")
            return

        desglose = {
            "Edad > 80 años": 1 if edad > 80 else 0,
            "Cáncer": 1 if ps1 == "Sí" else 0,
            "Enfermedad cardiopulmonar crónica": 1 if ps2 == "Sí" else 0,
            "FC ≥ 110 lpm": 1 if ps3 == "Sí" else 0,
            "PAs < 100 mmHg": 1 if ps4 == "Sí" else 0,
            "SatO₂ < 90 %": 1 if ps5 == "Sí" else 0,
        }

        puntuacion = sum(desglose.values())
        categoria, riesgo, recomendacion = interpretar_pesi_simp(puntuacion)

        st.markdown("### Resultado")

        r1, r2, r3 = st.columns(3, gap="large")

        with r1:
            st.metric("Puntuación total", puntuacion)

        with r2:
            st.metric("Categoría", categoria)

        with r3:
            st.metric("Estrato", riesgo)

        if puntuacion == 0:
            st.success(f"**{categoria}**. {recomendacion}", icon="🟢")
        else:
            st.error(f"**{categoria}**. {recomendacion}", icon="🔴")

        with st.expander("Ver desglose de la puntuación"):
            for criterio, valor in desglose.items():
                st.write(f"- {criterio}: **{valor}** punto(s)")

        st.caption(
            "El sPESI es una herramienta pronóstica tras el diagnóstico de TEP y debe integrarse con la estabilidad hemodinámica, biomarcadores, imagen y juicio clínico."
        )

def interpretar_bova(puntuacion):
    if puntuacion <= 2:
        return (
            "Estadio I",
            "Riesgo bajo",
            "4,4% de riesgo de complicaciones relacionadas con TEP y 3,1% de mortalidad a 30 días."
        )
    elif 3 <= puntuacion <= 4:
        return (
            "Estadio II",
            "Riesgo intermedio",
            "18% de riesgo de complicaciones relacionadas con TEP y 6,8% de mortalidad a 30 días."
        )
    else:
        return (
            "Estadio III",
            "Riesgo alto",
            "42% de riesgo de complicaciones relacionadas con TEP y 10,5% de mortalidad a 30 días."
        )


def render_bova():
    st.header("BOVA score")
    st.caption("Estratificación pronóstica en pacientes normotensos con TEP agudo.")

    st.info(
        "El BOVA score se aplica en pacientes con TEP agudo hemodinámicamente estables o normotensos y estima el riesgo de complicaciones a 30 días.",
        icon="🩺"
    )

    with st.container(border=True):
        st.markdown("### Datos clínicos")

        with st.form("form_bova"):
            c1, c2 = st.columns(2, gap="large")

            with c1:
                bova1 = st.radio(
                    "Presión arterial sistólica entre 90 y 100 mmHg",
                    ["No", "Sí"],
                    horizontal=True
                )

                bova2 = st.radio(
                    "Elevación de troponinas",
                    ["No", "Sí"],
                    horizontal=True
                )

            with c2:
                bova3 = st.radio(
                    "Disfunción del ventrículo derecho",
                    ["No", "Sí"],
                    help="Basada en ecocardiografía o pruebas de imagen según disponibilidad.",
                    horizontal=True
                )

                bova4 = st.radio(
                    "Frecuencia cardiaca ≥ 110 lpm",
                    ["No", "Sí"],
                    horizontal=True
                )

            submitted = st.form_submit_button("Calcular BOVA", use_container_width=True)

    if submitted:
        desglose = {
            "PAs 90–100 mmHg": 2 if bova1 == "Sí" else 0,
            "Troponinas elevadas": 2 if bova2 == "Sí" else 0,
            "Disfunción del ventrículo derecho": 2 if bova3 == "Sí" else 0,
            "FC ≥ 110 lpm": 1 if bova4 == "Sí" else 0,
        }

        puntuacion = sum(desglose.values())
        estadio, riesgo, recomendacion = interpretar_bova(puntuacion)

        st.markdown("### Resultado")

        r1, r2, r3 = st.columns(3, gap="large")

        with r1:
            st.metric("Puntuación total", puntuacion)

        with r2:
            st.metric("Estadio BOVA", estadio)

        with r3:
            st.metric("Estrato", riesgo)

        if puntuacion <= 2:
            st.success(f"**{estadio}**. {riesgo}. {recomendacion}", icon="🟢")
        elif 3 <= puntuacion <= 4:
            st.warning(f"**{estadio}**. {riesgo}. {recomendacion}", icon="🟡")
        else:
            st.error(f"**{estadio}**. {riesgo}. {recomendacion}", icon="🔴")

        with st.expander("Ver desglose de la puntuación"):
            for criterio, valor in desglose.items():
                st.write(f"- {criterio}: **{valor}** punto(s)")

        st.caption(
            "El BOVA score complementa la estratificación pronóstica y debe interpretarse junto con biomarcadores, imagen, estabilidad hemodinámica y juicio clínico."
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


elif st.session_state.categoria == "riesgo":
    subcategoria = st.sidebar.selectbox(
        "Selecciona una escala",
        [
            "PESI",
            "PESI simplificado",
            "BOVA score"
        ],
        index=None,
        placeholder="Elige una escala"
    )

    if subcategoria == "PESI":
        render_pesi()
    elif subcategoria == "PESI simplificado":
        render_pesi_simp()
    elif subcategoria == "BOVA score":
        render_bova()
    else:
        st.info("Selecciona una escala de pronóstico y riesgo en la barra lateral.")


def interpretar_bova(puntuacion):
    if puntuacion <= 2:
        return (
            "Estadio I",
            "Riesgo bajo",
            "4,4% de riesgo de complicaciones relacionadas con TEP y 3,1% de mortalidad a 30 días."
        )
    elif 3 <= puntuacion <= 4:
        return (
            "Estadio II",
            "Riesgo intermedio",
            "18% de riesgo de complicaciones relacionadas con TEP y 6,8% de mortalidad a 30 días."
        )
    else:
        return (
            "Estadio III",
            "Riesgo alto",
            "42% de riesgo de complicaciones relacionadas con TEP y 10,5% de mortalidad a 30 días."
        )


def render_bova():
    st.header("BOVA score")
    st.caption("Estratificación pronóstica en pacientes normotensos con TEP agudo.")

    st.info(
        "El BOVA score se aplica en pacientes con TEP agudo hemodinámicamente estables o normotensos y estima el riesgo de complicaciones a 30 días.",
        icon="🩺"
    )

    with st.container(border=True):
        st.markdown("### Datos clínicos")

        with st.form("form_bova"):
            c1, c2 = st.columns(2, gap="large")

            with c1:
                bova1 = st.radio(
                    "Presión arterial sistólica entre 90 y 100 mmHg",
                    ["No", "Sí"],
                    horizontal=True
                )

                bova2 = st.radio(
                    "Elevación de troponinas",
                    ["No", "Sí"],
                    horizontal=True
                )

            with c2:
                bova3 = st.radio(
                    "Disfunción del ventrículo derecho",
                    ["No", "Sí"],
                    help="Basada en ecocardiografía o pruebas de imagen según disponibilidad.",
                    horizontal=True
                )

                bova4 = st.radio(
                    "Frecuencia cardiaca ≥ 110 lpm",
                    ["No", "Sí"],
                    horizontal=True
                )

            submitted = st.form_submit_button("Calcular BOVA", use_container_width=True)

    if submitted:
        desglose = {
            "PAs 90–100 mmHg": 2 if bova1 == "Sí" else 0,
            "Troponinas elevadas": 2 if bova2 == "Sí" else 0,
            "Disfunción del ventrículo derecho": 2 if bova3 == "Sí" else 0,
            "FC ≥ 110 lpm": 1 if bova4 == "Sí" else 0,
        }

        puntuacion = sum(desglose.values())
        estadio, riesgo, recomendacion = interpretar_bova(puntuacion)

        st.markdown("### Resultado")

        r1, r2, r3 = st.columns(3, gap="large")

        with r1:
            st.metric("Puntuación total", puntuacion)

        with r2:
            st.metric("Estadio BOVA", estadio)

        with r3:
            st.metric("Estrato", riesgo)

        if puntuacion <= 2:
            st.success(f"**{estadio}**. {riesgo}. {recomendacion}", icon="🟢")
        elif 3 <= puntuacion <= 4:
            st.warning(f"**{estadio}**. {riesgo}. {recomendacion}", icon="🟡")
        else:
            st.error(f"**{estadio}**. {riesgo}. {recomendacion}", icon="🔴")

        with st.expander("Ver desglose de la puntuación"):
            for criterio, valor in desglose.items():
                st.write(f"- {criterio}: **{valor}** punto(s)")

        st.caption(
            "El BOVA score complementa la estratificación pronóstica y debe interpretarse junto con biomarcadores, imagen, estabilidad hemodinámica y juicio clínico."
        )








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

