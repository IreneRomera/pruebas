#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 18:48:37 2026

@author: Prunebelly
"""

import streamlit as st
from datetime import datetime
from streamlit_extras.buy_me_a_coffee import button

st.set_page_config(page_title="Calculadora de perfusiones endovenosas de medicación")

st.title("Calculadora de velocidad y dosis de medicaciones en perfusión endovenosa")
st.subheader("⬅ Usa la barra lateral para introducir datos y elegir el cálculo")

# ------------------------------
# Estado de sesión
# ------------------------------
if "categoria" not in st.session_state:
    st.session_state.categoria = None
    
    
# ------------------------------
# Funciones auxiliares
# ------------------------------
def mostrar_peso_sidebar():
    peso = st.sidebar.number_input(
        "Peso del paciente (kg)",
        min_value=20.0,
        max_value=150.0,
        value=65.0,
        step=0.1,
        format="%.1f"
    )
    return peso

# ------------------------------
# Funciones de cálculo/render
# ------------------------------

import streamlit as st

# Config general de fármacos para el módulo de velocidades
FARMACOS_CONFIG = {
    "Noradrenalina base (simple)": {
        "unidad_dosis": "mcg/kg/min",
        "unidad_dilucion": "mcg/mL",
        "dilucion_normalizada": 160.0,
        "tipo": "nora_simple",
        "info_seguridad": """
- Dosis terapéutica habitual: 0,05 mcg/kg/min y aumentar según respuesta.
- Dosis máxima recomendada: 1 mcg/kg/min.
- Preferente vía central (riesgo de necrosis ante extravasación).
"""
    },
    "Noradrenalina base (doble)": {
        "unidad_dosis": "mcg/kg/min",
        "unidad_dilucion": "mcg/mL",
        "dilucion_normalizada": 320.0,
        "tipo": "nora_doble",
        "info_seguridad": """
- Dosis terapéutica habitual: 0,05 mcg/kg/min y aumentar según respuesta.
- Dosis máxima recomendada: 1 mcg/kg/min.
- Preferente vía central (riesgo de necrosis ante extravasación).
"""
    },
    "Dobutamina": {
        "unidad_dosis": "mcg/kg/min",
        "unidad_dilucion": "mg/mL",
        "dilucion_normalizada": 5.0,
        "tipo": "dobutamina",
        "info_seguridad": """
- Dosis terapéutica: 2,5–15 mcg/kg/min.
- Dosis máxima: hasta 40 mcg/kg/min.
- Preferente vía central; extravasación puede producir necrosis (considerar fentolamina)."""
    },
    "Dopamina": {
        "unidad_dosis": "mcg/kg/min",
        "unidad_dilucion": "mg/mL",
        "dilucion_normalizada": 4.0,
        "tipo": "dopamina",
        "info_seguridad": """
- Dosis habitual: 2–50 mcg/kg/min.
- Preferente vía central; extravasación puede producir necrosis (considerar fentolamina)."""
    },
    "Propofol": {
        "unidad_dosis": "mg/kg/h",
        "unidad_dilucion": "mg/mL",
        "dilucion_normalizada": 20.0,
        "tipo": "propofol",
        "info_seguridad": """
- Emulsión lipídica, vigilar dosis acumuladas y riesgo de síndrome de perfusión de propofol."""
    },
    "Midazolam": {
        "unidad_dosis": "mg/kg/h",
        "unidad_dilucion": "mg/mL",
        "dilucion_normalizada": 1.0,
        "tipo": "midazolam",
        "info_seguridad": """
- Vigilar sedación y función respiratoria; considerar ajuste en insuficiencia hepática/renal."""
    },
    "Ketamina": {
        "unidad_dosis": "mg/kg/h",
        "unidad_dilucion": "mg/mL",
        "dilucion_normalizada": 1.0,  # rango habitual 1–2 mg/mL
        "tipo": "ketamina",
        "info_seguridad": """
- Dilución habitual 1–2 mg/mL.
- Monitorizar efectos neuropsiquiátricos y hemodinámicos."""
    },
    "Morfina": {
        "unidad_dosis": "mg/h",
        "unidad_dilucion": "mg/mL",
        "dilucion_normalizada": 0.2,  # rango habitual 0,2–0,4 mg/mL
        "tipo": "morfina",
        "info_seguridad": """
- Dilución habitual 0,2–0,4 mg/mL.
- Monitorizar depresión respiratoria y sedación."""
    },
    "Fentanilo": {
        "unidad_dosis": "mcg/kg/h",
        "unidad_dilucion": "mcg/mL",
        "dilucion_normalizada": 15.0,
        "tipo": "fentanilo",
        "info_seguridad": """
- Perfusión continua: ajustar según respuesta clínica y función respiratoria."""
    },
    "Remifentanilo": {
        "unidad_dosis": "mcg/kg/min",
        "unidad_dilucion": "mcg/mL",
        "dilucion_normalizada": 40.0,
        "tipo": "remifentanilo",
        "info_seguridad": """
- Dosis terapéutica: 0,008–0,05 mcg/kg/min (sedación) hasta 0,2 mcg/kg/min (anestesia).
- Semi-vida muy corta; ajustar finamente según respuesta."""
    },
    "Dexmedetomidina": {
        "unidad_dosis": "mcg/kg/h",
        "unidad_dilucion": "mcg/mL",
        "dilucion_normalizada": 4.0,
        "tipo": "dexmedetomidina",
        "info_seguridad": """
- Dosis terapéutica: 0,2–1,4 mcg/kg/h.
- Monitorizar FC y TA (riesgo de bradicardia/hipotensión)."""
    },
    "Atracurio": {
        "unidad_dosis": "mcg/kg/min",
        "unidad_dilucion": "mg/mL",
        "dilucion_normalizada": 5.0,
        "tipo": "atracurio",
        "info_seguridad": """
- Bloqueante neuromuscular; requiere monitorización del bloqueo y ajuste según respuesta."""
    },
    "Cisatracurio": {
        "unidad_dosis": "mcg/kg/min",
        "unidad_dilucion": "mg/mL",
        "dilucion_normalizada": 2.0,
        "tipo": "cisatracurio",
        "info_seguridad": """
- Dosis terapéutica: 0,5–5 mcg/kg/min; máximo 10,2 mcg/kg/min.
- Perfusión inicial 3 mcg/kg/min, luego 1–2 mcg/kg/min."""
    },
    "Rocuronio": {
        "unidad_dosis": "mg/kg/h",
        "unidad_dilucion": "mg/mL",
        "dilucion_normalizada": 10.0,
        "tipo": "rocuronio",
        "info_seguridad": """
- Bloqueante neuromuscular; administrar con monitorización de bloqueo y soporte ventilatorio."""
    },
    "Urapidil": {
        "unidad_dosis": "mg/h",
        "unidad_dilucion": "mg/mL",
        "dilucion_normalizada": 2.0,
        "tipo": "urapidil",
        "info_seguridad": """
- Vasodilatador periférico; vigilar TA y riesgo de hipotensión."""
    },
    "Furosemida": {
        "unidad_dosis": "mg/h",
        "unidad_dilucion": "mg/mL",
        "dilucion_normalizada": 10.0,
        "tipo": "furosemida",
        "info_seguridad": """
- Dosis habitual: 5–40 mg/h.
- Velocidades >4 mg/min aumentan riesgo de ototoxicidad; administrar lentamente."""
    },
    "Isoprenalina": {
        "unidad_dosis": "mcg/kg/min",
        "unidad_dilucion": "mcg/mL",
        "dilucion_normalizada": 40.0,
        "tipo": "isoprenalina",
        "info_seguridad": """
- Dosis inicial: 0,02–0,04 mcg/kg/min; dosis máxima recomendada: 0,15 mcg/kg/min."""
    },
    "Esmolol": {
        "unidad_dosis": "mcg/kg/min",
        "unidad_dilucion": "mg/mL",
        "dilucion_normalizada": 10.0,
        "tipo": "esmolol",
        "info_seguridad": """
- Recomendada dosis de carga 0,5–1 mg/kg en bolo.
- Perfusión según respuesta; monitorizar TA y FC."""
    },
    "Nitroglicerina": {
        "unidad_dosis": "mg/h",
        "unidad_dilucion": "mcg/mL",
        "dilucion_normalizada": 200.0,  # rango habitual 200–1000 mcg/mL
        "tipo": "nitroglicerina",
        "info_seguridad": """
- Respuesta efectiva suele alcanzarse con 3–6 mg/h (50–100 mcg/min).
- Dosis máxima recomendada: 10 mg/h (170 mcg/min).
- Evitar PVC por retención del fármaco; usar materiales no-PVC."""
    },
    "Salbutamol": {
        "unidad_dosis": "mcg/kg/h",
        "unidad_dilucion": "mcg/mL",
        "dilucion_normalizada": 20.0,
        "tipo": "salbutamol",
        "info_seguridad": """
- Ajustar dosis en función de respuesta clínica y efectos secundarios (taquicardia, temblor)."""
    },
    "Nimodipino": {
        "unidad_dosis": "mcg/kg/h",
        "unidad_dilucion": "mcg/mL",
        "dilucion_normalizada": 200.0,
        "tipo": "nimodipino",
        "info_seguridad": """
- Inicio habitual 15 mcg/kg/h durante 2 h, luego 30 mcg/kg/h si bien tolerado.
- En <70 kg o inestabilidad hemodinámica, no superar 7,5 mcg/kg/h."""
    },
    "Flumazenilo": {
        "unidad_dosis": "mg/h",
        "unidad_dilucion": "mg/mL",
        "dilucion_normalizada": 0.04,
        "tipo": "flumazenilo",
        "info_seguridad": """
- Dosis máxima recomendada 0,4 mg/h; dosis tóxica hasta 2 mg/h.
- Vigilar convulsiones en pacientes con uso crónico de benzodiacepinas."""
    },
    "Landiolol": {
        "unidad_dosis": "mcg/kg/min",
        "unidad_dilucion": "mg/mL",
        "dilucion_normalizada": 6.0,
        "tipo": "landiolol",
        "info_seguridad": """
- Dosis inicial: 10–40 mcg/kg/min; dosis máxima diaria: 57,6 mcg/kg/día.
- Puede usarse dosis de carga 100 mcg/kg/min durante 1 min."""
    },
}

def calcular_velocidad(farmaco_key: str, peso: float, dilucion: float, dosis: float) -> float:
    """Devuelve la velocidad en mL/h para un fármaco dado."""
    tipo = FARMACOS_CONFIG[farmaco_key]["tipo"]

    if tipo in ("nora_simple", "nora_doble", "remifentanilo", "atracurio",
                "cisatracurio", "isoprenalina", "landiolol", "esmolol"):
        # mayoría en mcg/kg/min con dilución en mcg/mL o mg/mL con factor 1000
        if FARMACOS_CONFIG[farmaco_key]["unidad_dilucion"] == "mcg/mL":
            vel = (dosis * peso * 60) / dilucion
        else:
            # dilución expresada en mg/mL, dosis en mcg/kg/min → convertir
            vel = (dosis * peso * 60) / (dilucion * 1000.0)

    elif tipo in ("dobutamina", "dopamina"):
        # mcg/kg/min, dilución en mg/mL (5 y 4 mg/mL)
        vel = (dosis * peso * 60) / (dilucion * 1000.0)

    elif tipo in ("propofol", "midazolam", "ketamina", "rocuronio"):
        # mg/kg/h, dilución mg/mL
        vel = (dosis * peso) / dilucion

    elif tipo in ("morfina", "urapidil", "furosemida", "flumazenilo", "nitroglicerina"):
        # mg/h, dilución mg/mL o mcg/mL con conversión adecuada
        if FARMACOS_CONFIG[farmaco_key]["unidad_dilucion"] == "mg/mL":
            vel = dosis / dilucion
        else:
            # nitroglicerina: dilución en mcg/mL, dosis en mg/h
            vel = dosis / (dilucion / 1000.0)

    elif tipo in ("fentanilo", "salbutamol", "nimodipino", "dexmedetomidina"):
        # mcg/kg/h, dilución en mcg/mL
        vel = (dosis * peso) / dilucion

    else:
        vel = float("nan")

    return vel

FARMACOS_LISTA = sorted(FARMACOS_CONFIG.keys())

def render_modulo_velocidades(peso: float):
    st.header("Cálculo de velocidad de perfusión (mL/h)")
    st.write(f"Peso del paciente: **{peso:.1f} kg**")

    farmaco = st.sidebar.selectbox(
        "Selecciona una medicación",
        FARMACOS_LISTA,
        index=None,
        placeholder="Elige una medicación"
    )

    if not farmaco:
        st.info("Selecciona un fármaco en la barra lateral para iniciar el cálculo.")
        return

    config = FARMACOS_CONFIG[farmaco]
    unidad_dosis = config["unidad_dosis"]
    unidad_dilucion = config["unidad_dilucion"]
    dilu_default = config["dilucion_normalizada"]

    st.subheader(farmaco)

    # Entrada de dilución con valor normalizado por defecto pero editable
    dilucion = st.number_input(
        f"Dilución ({unidad_dilucion})",
        min_value=0.0001,
        value=float(dilu_default),
        step=max(dilu_default / 100.0, 0.01),
        format="%.4f",
        help=f"Dilución normalizada habitual: {dilu_default} {unidad_dilucion}. "
             "Puedes modificarla si utilizas otra preparación."
    )

    # Entrada de dosis
    dosis = st.number_input(
        f"Dosis deseada ({unidad_dosis})",
        min_value=0.0,
        value=0.0,
        step=0.01,
        format="%.4f"
    )

    if st.button("Calcular velocidad de perfusión", key=f"calc_vel_{farmaco}"):
        vel_mlh = calcular_velocidad(farmaco, peso, dilucion, dosis)

        if not vel_mlh or vel_mlh != vel_mlh:
            st.error("No se ha podido calcular la velocidad con los parámetros introducidos.")
            return

        st.success(f"Velocidad requerida: **{vel_mlh:.2f} mL/h**")

        # Bloque de información de seguridad
        st.markdown("### Límites de seguridad y consideraciones")
        st.info(config["info_seguridad"])

        # Ejemplos de chequeo de dosis frente a máximos para algunos fármacos
        tipo = config["tipo"]

        if tipo in ("nora_simple", "nora_doble") and dosis > 1.0:
            st.error(
                "La dosis introducida supera la dosis máxima recomendada de 1 mcg/kg/min "
                "para noradrenalina base."
            )

        if tipo == "dobutamina" and dosis > 40.0:
            st.error(
                "La dosis de dobutamina supera 40 mcg/kg/min, por encima del máximo recomendado."
            )

        if tipo == "cisatracurio" and dosis > 10.2:
            st.error(
                "La dosis de cisatracurio supera 10,2 mcg/kg/min, máximo recomendado."
            )

        if tipo == "isoprenalina" and dosis > 0.15:
            st.error(
                "La dosis de isoprenalina supera 0,15 mcg/kg/min, máximo recomendado."
            )

        if tipo == "nitroglicerina" and dosis > 10.0:
            st.error(
                "La dosis de nitroglicerina supera 10 mg/h (≈170 mcg/min), máximo recomendado."
            )

        if tipo == "flumazenilo" and dosis > 0.4:
            st.warning(
                "La dosis de flumazenilo supera 0,4 mg/h; recuerda que dosis tóxicas se sitúan "
                "en torno a 2 mg/h."
            )

        if tipo == "dexmedetomidina" and dosis > 1.4:
            st.warning(
                "La dosis de dexmedetomidina supera 1,4 mcg/kg/h, por encima del rango terapéutico."
            )

        if tipo == "landiolol" and dosis > 40.0:
            st.warning(
                "La dosis de landiolol supera 40 mcg/kg/min, revisar que se mantiene dentro de las "
                "recomendaciones de dosis máxima diaria."
            )

def calcular_dosis(farmaco_key: str, peso: float, dilucion: float, velocidad_mlh: float) -> float:
    """
    Devuelve la dosis (en las unidades correspondientes) para un fármaco dado,
    a partir de la velocidad (mL/h) y la dilución.
    """
    tipo = FARMACOS_CONFIG[farmaco_key]["tipo"]

    # mcg/kg/min con dilución en mcg/mL o mg/mL*1000
    if tipo in ("nora_simple", "nora_doble", "remifentanilo",
                "atracurio", "cisatracurio", "isoprenalina",
                "landiolol", "esmolol"):
        if FARMACOS_CONFIG[farmaco_key]["unidad_dilucion"] == "mcg/mL":
            # dospvc = (vel * dilu) / (peso * 60)
            dosis = (velocidad_mlh * dilucion) / (peso * 60.0)
        else:
            # dilución en mg/mL → mcg/mL = mg/mL * 1000
            dosis = (velocidad_mlh * (dilucion * 1000.0)) / (peso * 60.0)

    elif tipo in ("dobutamina", "dopamina"):
        # mcg/kg/min, dilución mg/mL
        dosis = (velocidad_mlh * (dilucion * 1000.0)) / (peso * 60.0)

    elif tipo in ("propofol", "midazolam", "ketamina", "rocuronio"):
        # mg/kg/h, dilución mg/mL
        # dospvc = (vel * dilu) / peso
        dosis = (velocidad_mlh * dilucion) / peso

    elif tipo in ("morfina", "urapidil", "furosemida", "flumazenilo"):
        # mg/h, dilución mg/mL
        # dospvc = vel * dilu
        dosis = velocidad_mlh * dilucion

    elif tipo == "nitroglicerina":
        # mg/h, dilución en mcg/mL
        # dospvc = vel * (dilu/1000)
        dosis = velocidad_mlh * (dilucion / 1000.0)

    elif tipo in ("fentanilo", "salbutamol", "nimodipino", "dexmedetomidina"):
        # mcg/kg/h, dilución mcg/mL
        # dospvc = (vel * dilu) / peso
        dosis = (velocidad_mlh * dilucion) / peso

    else:
        dosis = float("nan")

    return dosis



def render_modulo_dosis(peso: float):
    st.header("Cálculo de dosis a partir de la velocidad de perfusión")
    st.write(f"Peso del paciente: **{peso:.1f} kg**")

    farmaco = st.sidebar.selectbox(
        "Selecciona una medicación",
        FARMACOS_LISTA,
        index=None,
        placeholder="Elige una medicación"
    )

    if not farmaco:
        st.info("Selecciona un fármaco en la barra lateral para calcular la dosis.")
        return

    config = FARMACOS_CONFIG[farmaco]
    unidad_dosis = config["unidad_dosis"]
    unidad_dilucion = config["unidad_dilucion"]
    dilu_default = config["dilucion_normalizada"]
    tipo = config["tipo"]

    st.subheader(farmaco)

    # Dilución: valor normalizado por defecto pero editable
    dilucion = st.number_input(
        f"Dilución ({unidad_dilucion})",
        min_value=0.0001,
        value=float(dilu_default),
        step=max(dilu_default / 100.0, 0.01),
        format="%.4f",
        help=(
            f"Dilución normalizada habitual: {dilu_default} {unidad_dilucion}. "
            "Modifícala si tu preparación difiere."
        ),
        key=f"dilucion_{tipo}"
    )

    # Velocidad de perfusión en mL/h
    velocidad_mlh = st.number_input(
        "Velocidad de la perfusión (mL/h)",
        min_value=0.0,
        value=0.0,
        step=0.1,
        format="%.2f",
        key=f"velocidad_{tipo}"
    )

    if st.button("Calcular dosis", key=f"calc_dosis_{tipo}"):
        dosis = calcular_dosis(farmaco, peso, dilucion, velocidad_mlh)

        if not dosis or dosis != dosis:
            st.error("No se ha podido calcular la dosis con los parámetros introducidos.")
            return

        # Redondeo especial para algunos fármacos donde en consola ya redondeabas
        if tipo in ("isoprenalina", "esmolol", "landiolol", "nimodipino", "flumazenilo"):
            dosis_mostrar = round(dosis, 0)
        else:
            dosis_mostrar = dosis

        st.success(
            f"Dosis calculada: **{dosis_mostrar:.4f} {unidad_dosis}**"
        )

        st.markdown("### Límites de seguridad y consideraciones")
        st.info(config["info_seguridad"])

        # Avisos si nos salimos de los rangos del PDF
        if tipo in ("nora_simple", "nora_doble"):
            # 0,05–1 mcg/kg/min
            if dosis < 0.05:
                st.warning(
                    "La dosis calculada está por debajo de 0,05 mcg/kg/min, "
                    "por debajo del rango terapéutico habitual."
                )
            elif dosis > 1.0:
                st.error(
                    "La dosis calculada supera 1 mcg/kg/min, máxima recomendada "
                    "para noradrenalina base."
                )

        if tipo == "dobutamina":
            # 2,5–15 mcg/kg/min, máx 40
            if dosis < 2.5:
                st.warning("La dosis de dobutamina está por debajo de 2,5 mcg/kg/min.")
            elif dosis > 40.0:
                st.error("La dosis de dobutamina supera 40 mcg/kg/min, máximo recomendado.")

        if tipo == "dopamina":
            # rango 2–50 mcg/kg/min
            if dosis < 2.0:
                st.warning("La dosis de dopamina está por debajo de 2 mcg/kg/min.")
            elif dosis > 50.0:
                st.error("La dosis de dopamina supera 50 mcg/kg/min, por encima del rango usual.")

        if tipo == "cisatracurio":
            # 0,5–5 mcg/kg/min, máx 10,2
            if dosis < 0.5:
                st.warning("La dosis de cisatracurio está por debajo de 0,5 mcg/kg/min.")
            elif dosis > 10.2:
                st.error("La dosis de cisatracurio supera 10,2 mcg/kg/min, máximo recomendado.")

        if tipo == "isoprenalina":
            # máx 0,15 mcg/kg/min
            if dosis > 0.15:
                st.error("La dosis de isoprenalina supera 0,15 mcg/kg/min, máximo recomendado.")

        if tipo == "nitroglicerina":
            # eficaz 3–6 mg/h, máx 10 mg/h
            if dosis < 3.0:
                st.warning("La dosis de nitroglicerina está por debajo de 3 mg/h.")
            elif dosis > 10.0:
                st.error(
                    "La dosis de nitroglicerina supera 10 mg/h (~170 mcg/min), "
                    "máximo recomendado."
                )

        if tipo == "flumazenilo":
            # máx 0,4 mg/h, tóxica hasta 2 mg/h
            if dosis > 0.4:
                st.warning(
                    "La dosis de flumazenilo supera 0,4 mg/h; recuerda que dosis tóxicas "
                    "se sitúan en torno a 2 mg/h."
                )

        if tipo == "dexmedetomidina":
            # 0,2–1,4 mcg/kg/h
            if dosis < 0.2:
                st.warning("La dosis de dexmedetomidina está por debajo de 0,2 mcg/kg/h.")
            elif dosis > 1.4:
                st.warning(
                    "La dosis de dexmedetomidina supera 1,4 mcg/kg/h, por encima "
                    "del rango terapéutico."
                )

        if tipo == "nimodipino":
            # 15–30 mcg/kg/h, con límite 7,5 en <70kg o inestabilidad
            st.info(
                "Recuerda: inicio habitual a 15 mcg/kg/h durante 2 h, luego 30 mcg/kg/h "
                "si bien tolerado; en <70 kg o inestabilidad hemodinámica, no superar "
                "7,5 mcg/kg/h."
            )

        if tipo == "landiolol":
            # inicial 10–40 mcg/kg/min, máxima diaria 57,6 mcg/kg/día
            if dosis > 40.0:
                st.warning(
                    "La dosis de landiolol supera 40 mcg/kg/min; revisa que se mantiene "
                    "dentro de la dosis máxima diaria recomendada."
                )
                
                





# ------------------------------
# Barra lateral
# ------------------------------
peso = mostrar_peso_sidebar()

st.sidebar.markdown(
    """
    <h2 style='text-align: center; color: #800080;'>
        ¿Qué deseas calcular?
    </h2>
    """,
    unsafe_allow_html=True,
)

if st.sidebar.button("La velocidad de una perfusión continua", use_container_width=True):
    st.session_state.categoria = "velocidad"

if st.sidebar.button("La dosis de una perfusión continua", use_container_width=True):
    st.session_state.categoria = "dosis"
    
if st.sidebar.button("Hacer un cálculo manual a partir de una dilución", use_container_width=True):
    st.session_state.categoria = "manual"


# ------------------------------
# Contenido principal según categoría
# ------------------------------

if st.session_state.categoria == "velocidad":
    render_modulo_velocidades(peso)

elif st.session_state.categoria == "dosis":
    render_modulo_dosis(peso)


else:
    st.info("Elige en la barra lateral si quieres calcular velocidad o dosis.")


# ------------------------------
# Pie de página
# ------------------------------

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
