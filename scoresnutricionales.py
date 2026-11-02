#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Calculadora de instrumentos nutricionales:
NRS-2002, NUTRIC-PCR, FILNUT y GLIM.

Reglas basadas en los documentos aportados.
"""

from datetime import date
import math
import re

import streamlit as st


# ============================================================
# CONFIGURACIÓN
# ============================================================
st.set_page_config(
    page_title="Calculadora de scores nutricionales",
    layout="centered",
)

st.title("Calculadora de scores nutricionales")
st.subheader("⬅ Selecciona el instrumento e introduce los datos")

SCORES = ["NRS-2002", "NUTRIC-PCR", "FILNUT", "GLIM"]




# ============================================================
# UTILIDADES
# ============================================================
def numero(valor, decimales=2):
    if valor is None:
        return "No disponible"
    return f"{valor:.{decimales}f}".replace(".", ",")


def validar_numeros(**valores):
    errores = []

    for nombre, valor in valores.items():
        if valor is not None and not math.isfinite(valor):
            errores.append(f"{nombre}: introduce un número finito.")

    return errores


def si_no(valor):
    return "Sí" if valor else "No"


def guardar_informe(score, identificador, fecha, resultado):
    st.session_state["informe_nutricional"] = {
        "score": score,
        "id": identificador.strip() or "No indicado",
        "fecha": fecha.strftime("%Y%m%d"),
        **resultado,
    }


def informe_a_texto(informe):
    lineas = [
        "INFORME DE VALORACIÓN NUTRICIONAL",
        "",
        f"Instrumento: {informe['score']}",
        f"ID: {informe['id']}",
        f"Fecha: {informe['fecha']}",
        "",
        f"Resultado: {informe['resultado']}",
        "",
        "DESGLOSE",
    ]

    for fila in informe["filas"]:
        lineas.append(
            " | ".join(
                f"{campo}: {valor}"
                for campo, valor in fila.items()
            )
        )

    if informe.get("notas"):
        lineas.extend(["", "OBSERVACIONES"])

        for nota in informe["notas"]:
            lineas.append(f"- {nota}")

    lineas.extend([
        "",
        "Resultado de apoyo a la valoración clínica. "
        "No sustituye el juicio clínico.",
    ])

    return "\n".join(lineas)


def mostrar_informe(informe):
    st.header(f"Informe: {informe['score']}")

    col1, col2 = st.columns(2)
    col1.write(f"ID: {informe['id']}")
    col2.write(f"Fecha: {informe['fecha']}")

    st.subheader("Resultado")
    st.info(informe["resultado"])

    st.subheader("Desglose")
    st.dataframe(
        informe["filas"],
        hide_index=True,
        use_container_width=True,
    )

    if informe.get("notas"):
        st.subheader("Observaciones")

        for nota in informe["notas"]:
            st.write(f"• {nota}")

    st.caption(
        "Resultado de apoyo a la valoración clínica. "
        "No sustituye el juicio clínico."
    )

    id_archivo = re.sub(
        r"[^A-Za-z0-9_-]+",
        "_",
        informe["id"],
    )[:60]

    st.download_button(
        "Descargar informe en texto",
        data=informe_a_texto(informe).encode("utf-8"),
        file_name=(
            f"{informe['score']}_{id_archivo}_"
            f"{informe['fecha']}.txt"
        ),
        mime="text/plain",
        key="descarga_informe_nutricional",
        use_container_width=True,
    )


# ============================================================
# NRS-2002
# ============================================================
NRS_NUTRICION = [
    (
        "0 — Estado nutricional normal",
        0,
    ),
    (
        "1 — Pérdida >5 % en 3 meses o ingesta "
        "50–75 % de requerimientos en la última semana",
        1,
    ),
    (
        "2 — Pérdida >5 % en 2 meses, o IMC 18,5–20,5 "
        "con deterioro general, o ingesta 25–60 %",
        2,
    ),
    (
        "3 — Pérdida >5 % en 1 mes o >15 % en 3 meses, "
        "o IMC <18,5 con deterioro general, o ingesta 0–25 %",
        3,
    ),
]

NRS_ENFERMEDAD = [
    ("0 — Requerimientos normales", 0),
    (
        "1 — Leve: fractura de cadera, cirrosis, EPOC, "
        "hemodiálisis, diabetes u oncología estable",
        1,
    ),
    (
        "2 — Moderada: cirugía mayor abdominal, ictus, "
        "neumonía grave o neoplasias hematológicas",
        2,
    ),
    (
        "3 — Severa: TCE, trasplante de médula ósea "
        "o paciente crítico en UCI",
        3,
    ),
]


def calcular_nrs(edad, nutricion, enfermedad):
    edad_puntos = int(edad >= 70)
    total = nutricion[1] + enfermedad[1] + edad_puntos

    return {
        "resultado": f"NRS-2002: {total} / 7 puntos.",
        "filas": [
            {
                "Componente": "Estado nutricional",
                "Dato": nutricion[0],
                "Puntos": nutricion[1],
            },
            {
                "Componente": "Severidad de la enfermedad",
                "Dato": enfermedad[0],
                "Puntos": enfermedad[1],
            },
            {
                "Componente": "Edad",
                "Dato": f"{edad} años",
                "Puntos": edad_puntos,
            },
        ],
        "notas": [
            "Se ha utilizado la puntuación completa, sin precribado. "
            "El documento indica que en pacientes que ingresan en UCI "
            "puede omitirse el precribado inicial.",

            "Cuando se cumplan criterios de varios niveles del estado "
            "nutricional, selecciona el de mayor puntuación.",

            "El resumen aportado no incluye un umbral de "
            "interpretación del total NRS-2002; por ello, este módulo "
            "informa la puntuación sin añadir una clasificación "
            "de riesgo no especificada en el documento.",
        ],
    }


def render_nrs(identificador, fecha):
    with st.sidebar.form("form_nrs"):
        st.subheader("NRS-2002")

        edad = st.number_input(
            "Edad (años)",
            min_value=18,
            value=None,
            step=1,
            key="nrs_edad",
        )

        st.caption(
            "Selecciona el nivel más alto aplicable en cada dominio."
        )

        nutricion = st.selectbox(
            "Estado nutricional",
            NRS_NUTRICION,
            format_func=lambda opcion: opcion[0],
            index=None,
            placeholder="Selecciona el estado nutricional",
        )

        enfermedad = st.selectbox(
            "Severidad de la enfermedad",
            NRS_ENFERMEDAD,
            format_func=lambda opcion: opcion[0],
            index=None,
            placeholder="Selecciona la severidad",
        )

        enviar = st.form_submit_button(
            "Calcular NRS-2002",
            use_container_width=True,
        )

    if enviar:
        if edad is None or nutricion is None or enfermedad is None:
            st.error("Completa la edad y los dos dominios del NRS-2002.")
            return

        guardar_informe(
            "NRS-2002",
            identificador,
            fecha,
            calcular_nrs(edad, nutricion, enfermedad),
        )


# ============================================================
# NUTRIC-PCR
# ============================================================
def calcular_nutric(edad, apache, sofa, comorbilidades, dias, pcr):
    puntos_edad = 0 if edad <= 49 else 1 if edad <= 74 else 2

    puntos_apache = (
        0 if apache <= 14
        else 1 if apache <= 19
        else 2 if apache <= 28
        else 3
    )

    puntos_sofa = 0 if sofa <= 5 else 1 if sofa <= 9 else 2
    puntos_comorbilidades = int(comorbilidades >= 2)
    puntos_dias = int(dias >= 1)

    total_sin_pcr = (
        puntos_edad
        + puntos_apache
        + puntos_sofa
        + puntos_comorbilidades
        + puntos_dias
    )

    riesgo_sin_pcr = (
        "Bajo riesgo"
        if total_sin_pcr <= 4
        else "Alto riesgo"
    )

    filas = [
        {"Componente": "Edad", "Dato": f"{edad} años",
         "Puntos": puntos_edad},
        {"Componente": "APACHE II", "Dato": str(apache),
         "Puntos": puntos_apache},
        {"Componente": "SOFA", "Dato": str(sofa),
         "Puntos": puntos_sofa},
        {"Componente": "Comorbilidades", "Dato": str(comorbilidades),
         "Puntos": puntos_comorbilidades},
        {"Componente": "Días previos al ingreso en UCI",
         "Dato": str(dias), "Puntos": puntos_dias},
    ]

    notas = [
        "Se aplican las variantes y los umbrales de la tabla aportada.",
        "Comorbilidades: registra el número utilizado por tu protocolo "
        "para este instrumento.",
    ]

    resultado = (
        f"NUTRIC-1, sin PCR: {total_sin_pcr} / 9 puntos. "
        f"{riesgo_sin_pcr}."
    )

    if pcr is not None:
        puntos_pcr = int(pcr >= 10)
        total_con_pcr = total_sin_pcr + puntos_pcr

        riesgo_con_pcr = (
            "Bajo riesgo"
            if total_con_pcr <= 5
            else "Alto riesgo"
        )

        filas.append({
            "Componente": "PCR",
            "Dato": f"{numero(pcr)} mg/dL",
            "Puntos": puntos_pcr,
        })

        resultado += (
            f"\n\nNUTRIC-2, con PCR: "
            f"{total_con_pcr} / 10 puntos. {riesgo_con_pcr}."
        )

    else:
        notas.append(
            "No se ha calculado NUTRIC-2 porque no se ha introducido PCR."
        )

    return {
        "resultado": resultado,
        "filas": filas,
        "notas": notas,
    }


def render_nutric(identificador, fecha):
    with st.sidebar.form("form_nutric"):
        st.subheader("NUTRIC-PCR")

        edad = st.number_input(
            "Edad (años)", min_value=18, value=None, step=1,
            key="nutric_edad",
        )

        apache = st.number_input(
            "APACHE II", min_value=0, max_value=71,
            value=None, step=1,
        )

        sofa = st.number_input(
            "SOFA", min_value=0, max_value=24,
            value=None, step=1,
        )

        comorbilidades = st.number_input(
            "Número de comorbilidades",
            min_value=0, value=None, step=1,
        )

        dias = st.number_input(
            "Días de hospitalización previos al ingreso en UCI",
            min_value=0, value=None, step=1,
        )

        pcr = st.number_input(
            "PCR (mg/dL) — opcional",
            min_value=0.0, value=None, step=0.1,
            format="%.2f",
            help=(
                "La tabla utiliza mg/dL. "
                "Si el laboratorio informa mg/L, divide entre 10."
            ),
        )

        enviar = st.form_submit_button(
            "Calcular NUTRIC",
            use_container_width=True,
        )

    if enviar:
        if any(
            valor is None
            for valor in [edad, apache, sofa, comorbilidades, dias]
        ):
            st.error(
                "Completa todos los campos salvo la PCR, que es opcional."
            )
            return

        errores = validar_numeros(PCR=pcr)

        if errores:
            st.error(" ".join(errores))
            return

        guardar_informe(
            "NUTRIC-PCR",
            identificador,
            fecha,
            calcular_nutric(
                edad, apache, sofa, comorbilidades, dias, pcr
            ),
        )


# ============================================================
# FILNUT
# ============================================================
def puntos_albumina(valor):
    if valor >= 3.5:
        return 0
    if valor >= 3:
        return 2
    if valor >= 2.5:
        return 4
    return 6


def puntos_prealbumina(valor):
    if valor >= 18:
        return 0
    if valor > 15:
        return 2
    if valor >= 10:
        return 4
    return 6


def puntos_linfocitos(valor):
    if valor >= 1600:
        return 0
    if valor >= 1200:
        return 1
    if valor >= 800:
        return 2
    return 3


def puntos_colesterol(valor):
    if valor >= 180:
        return 0
    if valor >= 140:
        return 1
    if valor >= 100:
        return 2
    return 3


def calcular_filnut(albumina, prealbumina, proteinas, linfocitos, colesterol):
    candidatos = []

    if albumina is not None:
        candidatos.append((
            "Albúmina",
            albumina,
            "g/dL",
            puntos_albumina(albumina),
        ))

    if prealbumina is not None:
        candidatos.append((
            "Prealbúmina",
            prealbumina,
            "mg/dL",
            puntos_prealbumina(prealbumina),
        ))

    if candidatos:
        # En empate se conserva la albúmina si está disponible.
        seleccionado = max(candidatos, key=lambda item: item[3])

    elif proteinas is not None:
        seleccionado = (
            "Proteínas totales",
            proteinas,
            "g/dL",
            0 if proteinas >= 5 else 5,
        )

    else:
        raise ValueError(
            "Introduce albúmina, prealbúmina o proteínas totales."
        )

    nombre, valor, unidad, puntos_proteicos = seleccionado

    puntos_linf = puntos_linfocitos(linfocitos)
    puntos_col = puntos_colesterol(colesterol)

    total = puntos_proteicos + puntos_linf + puntos_col

    riesgo = (
        "Sin riesgo" if total <= 1
        else "Riesgo bajo" if total <= 4
        else "Riesgo medio" if total <= 8
        else "Riesgo alto"
    )

    filas = []

    for etiqueta, dato, unidad_dato, puntos in candidatos:
        filas.append({
            "Parámetro": etiqueta,
            "Dato": f"{numero(dato)} {unidad_dato}",
            "Puntuación del parámetro": str(puntos),
            "Uso": (
                "Seleccionado"
                if etiqueta == nombre
                else "No sumado"
            ),
        })

    if proteinas is not None:
        filas.append({
            "Parámetro": "Proteínas totales",
            "Dato": f"{numero(proteinas)} g/dL",
            "Puntuación del parámetro": str(
                0 if proteinas >= 5 else 5
            ),
            "Uso": (
                "Seleccionado"
                if nombre == "Proteínas totales"
                else "No sumado: hay albúmina o prealbúmina"
            ),
        })

    filas.extend([
        {
            "Parámetro": "Linfocitos",
            "Dato": f"{linfocitos} células/µL",
            "Puntuación del parámetro": str(puntos_linf),
            "Uso": "Sumado",
        },
        {
            "Parámetro": "Colesterol total",
            "Dato": f"{numero(colesterol)} mg/dL",
            "Puntuación del parámetro": str(puntos_col),
            "Uso": "Sumado",
        },
    ])

    return {
        "resultado": f"FILNUT: {total} puntos. {riesgo}.",
        "filas": filas,
        "notas": [
            f"Componente proteico utilizado: {nombre} "
            f"({puntos_proteicos} puntos).",

            "La albúmina y la prealbúmina no se suman entre sí: "
            "se utiliza la de mayor puntuación.",

            "Antes de utilizar clínicamente la calculadora, confirma "
            "esa unidad con el documento original y el laboratorio. "
            "El código aplica directamente los umbrales numéricos "
            "800, 1200 y 1600, sin convertir unidades.",
        ],
    }


def render_filnut(identificador, fecha):
    with st.sidebar.form("form_filnut"):
        st.subheader("FILNUT")

        st.caption(
            "Introduce al menos un parámetro proteico. "
            "Deja vacíos los que no estén disponibles."
        )

        albumina = st.number_input(
            "Albúmina (g/dL)",
            min_value=0.0, value=None, step=0.01, format="%.2f",
        )

        prealbumina = st.number_input(
            "Prealbúmina (mg/dL)",
            min_value=0.0, value=None, step=0.01, format="%.2f",
        )

        proteinas = st.number_input(
            "Proteínas totales (g/dL)",
            min_value=0.0, value=None, step=0.01, format="%.2f",
        )

        st.caption(
            "Se aplican los valores numéricos de la tabla aportada."
        )

        linfocitos = st.number_input(
          "Linfocitos totales (células/µL)",
          min_value=0,
          value=None,
          step=1,
          help="Introduce el recuento absoluto en células/µL.",
        )

        colesterol = st.number_input(
            "Colesterol total (mg/dL)",
            min_value=0.0, value=None, step=1.0, format="%.2f",
        )

        enviar = st.form_submit_button(
            "Calcular FILNUT",
            use_container_width=True,
        )

    if enviar:
        if all(
            valor is None
            for valor in [albumina, prealbumina, proteinas]
        ):
            st.error(
                "Introduce albúmina, prealbúmina o proteínas totales."
            )
            return

        if linfocitos is None or colesterol is None:
            st.error(
                "Introduce linfocitos y colesterol para obtener "
                "una puntuación FILNUT completa."
            )
            return

        errores = validar_numeros(
            Albumina=albumina,
            Prealbumina=prealbumina,
            Proteinas=proteinas,
            Colesterol=colesterol,
        )

        if errores:
            st.error(" ".join(errores))
            return

        guardar_informe(
            "FILNUT",
            identificador,
            fecha,
            calcular_filnut(
                albumina, prealbumina, proteinas,
                linfocitos, colesterol,
            ),
        )


# ============================================================
# GLIM
# ============================================================
MASA_MUSCULAR = [
    "Sin reducción",
    "Reducida: déficit leve-moderado",
    "Reducida: déficit grave",
    "Reducida: gravedad no determinada",
    "No evaluada",
]

RESPUESTAS = ["No", "Sí"]


def calcular_glim(
    edad,
    imc,
    referencia,
    perdida,
    periodo,
    masa,
    ingesta_50,
    ingesta_2_semanas,
    malabsorcion,
    inflamacion_aguda,
    inflamacion_cronica,
):
    referencia_asia = referencia == "Asia"

    if referencia_asia:
        corte_imc = 18.5 if edad < 70 else 20
    else:
        corte_imc = 20 if edad < 70 else 22

    bajo_imc = imc < corte_imc

    periodo_corto = periodo == "Últimos 6 meses"

    perdida_positiva = (
        perdida > 5
        if periodo_corto
        else perdida > 10
    )

    masa_positiva = masa in [
        "Reducida: déficit leve-moderado",
        "Reducida: déficit grave",
        "Reducida: gravedad no determinada",
    ]

    fenotipos = [
        perdida_positiva,
        bajo_imc,
        masa_positiva,
    ]

    etiologia_ingesta = any([
        ingesta_50,
        ingesta_2_semanas,
        malabsorcion,
    ])

    etiologia_inflamacion = any([
        inflamacion_aguda,
        inflamacion_cronica,
    ])

    hay_fenotipo = any(fenotipos)
    hay_etiologia = etiologia_ingesta or etiologia_inflamacion

    cumple_glim = hay_fenotipo and hay_etiologia

    # Gravedad: se utiliza el criterio fenotípico más grave.
    grados = []
    gravedad_incompleta = False

    if perdida_positiva:
        corte_grave = 10 if periodo_corto else 20
        grados.append(2 if perdida > corte_grave else 1)

    if bajo_imc:
        if referencia_asia:
            # El PDF ofrece umbrales diagnósticos asiáticos,
            # pero no una tabla diferenciada de estadificación.
            gravedad_incompleta = True
        else:
            corte_grave_imc = 18.5 if edad < 70 else 20
            grados.append(2 if imc < corte_grave_imc else 1)

    if masa == "Reducida: déficit leve-moderado":
        grados.append(1)
    elif masa == "Reducida: déficit grave":
        grados.append(2)
    elif masa == "Reducida: gravedad no determinada":
        gravedad_incompleta = True
    elif masa == "No evaluada":
        gravedad_incompleta = True

    notas = [
        "GLIM no produce una puntuación total. "
        "Requiere al menos un criterio fenotípico "
        "y un criterio etiológico.",

        "La evaluación se realiza después de un cribado "
        "nutricional, como parte de la valoración clínica.",

        "La masa muscular debe haberse valorado mediante "
        "una técnica validada. No se utilizan aquí puntos "
        "de corte ecográficos adicionales.",
    ]

    if cumple_glim:
        grado_conocido = max(grados, default=0)

        if grado_conocido == 2:
            resultado = (
                "Se cumple la combinación diagnóstica GLIM. "
                "Desnutrición grave — estadio 2."
            )

        elif grado_conocido == 1 and not gravedad_incompleta:
            resultado = (
                "Se cumple la combinación diagnóstica GLIM. "
                "Desnutrición moderada — estadio 1."
            )

        elif grado_conocido == 1:
            resultado = (
                "Se cumple la combinación diagnóstica GLIM. "
                "Al menos estadio 1; gravedad final pendiente "
                "de completar la valoración."
            )

        else:
            resultado = (
                "Se cumple la combinación diagnóstica GLIM. "
                "Gravedad no determinada con los datos disponibles."
            )

    elif not hay_fenotipo and masa == "No evaluada":
        resultado = (
            "No se demuestra la combinación diagnóstica GLIM "
            "con los datos disponibles. Valoración fenotípica "
            "incompleta: masa muscular no evaluada."
        )

    else:
        resultado = (
            "No se cumple la combinación diagnóstica GLIM "
            "con los datos registrados. "
            "Esto no equivale por sí solo a excluir desnutrición."
        )

    if referencia_asia:
        notas.append(
            "Se utilizan los umbrales diagnósticos de IMC para Asia "
            "del PDF. Su tabla de gravedad no aporta umbrales "
            "asiáticos diferenciados; por ello, el IMC no "
            "estadifica automáticamente en esta opción."
        )

    if masa == "No evaluada":
        notas.append(
            "La falta de valoración muscular puede impedir "
            "excluir un criterio fenotípico o completar la gravedad."
        )

    filas = [
        {
            "Tipo": "Fenotípico",
            "Criterio": "Pérdida involuntaria de peso",
            "Dato": f"{numero(perdida)} % — {periodo.lower()}",
            "Cumple": si_no(perdida_positiva),
        },
        {
            "Tipo": "Fenotípico",
            "Criterio": "Bajo IMC",
            "Dato": (
                f"{numero(imc)} kg/m²; "
                f"umbral <{numero(corte_imc)}"
            ),
            "Cumple": si_no(bajo_imc),
        },
        {
            "Tipo": "Fenotípico",
            "Criterio": "Masa muscular reducida",
            "Dato": masa,
            "Cumple": (
                "No evaluable"
                if masa == "No evaluada"
                else si_no(masa_positiva)
            ),
        },
        {
            "Tipo": "Etiológico",
            "Criterio": "Ingesta <50 % durante >1 semana",
            "Dato": si_no(ingesta_50),
            "Cumple": si_no(ingesta_50),
        },
        {
            "Tipo": "Etiológico",
            "Criterio": "Reducción de ingesta durante >2 semanas",
            "Dato": si_no(ingesta_2_semanas),
            "Cumple": si_no(ingesta_2_semanas),
        },
        {
            "Tipo": "Etiológico",
            "Criterio": "Enfermedad digestiva con malasimilación",
            "Dato": si_no(malabsorcion),
            "Cumple": si_no(malabsorcion),
        },
        {
            "Tipo": "Etiológico",
            "Criterio": "Inflamación: enfermedad aguda o cirugía",
            "Dato": si_no(inflamacion_aguda),
            "Cumple": si_no(inflamacion_aguda),
        },
        {
            "Tipo": "Etiológico",
            "Criterio": "Inflamación relacionada con enfermedad crónica",
            "Dato": si_no(inflamacion_cronica),
            "Cumple": si_no(inflamacion_cronica),
        },
    ]

    return {
        "resultado": resultado,
        "filas": filas,
        "notas": notas,
    }


def render_glim(identificador, fecha):
    with st.sidebar.form("form_glim"):
        st.subheader("GLIM")

        edad = st.number_input(
            "Edad (años)",
            min_value=18, value=None, step=1,
            key="glim_edad",
        )

        referencia = st.selectbox(
            "Referencia diagnóstica de IMC",
            ["General", "Asia"],
        )

        imc = st.number_input(
            "IMC (kg/m²)",
            min_value=0.1,
            value=None,
            step=0.1,
            format="%.2f",
        )

        perdida = st.number_input(
            "Pérdida involuntaria de peso (%)",
            min_value=0.0,
            max_value=100.0,
            value=None,
            step=0.1,
            format="%.2f",
            help="Introduce 0 si no existe pérdida involuntaria.",
        )

        periodo = st.selectbox(
            "Periodo de la pérdida de peso",
            ["Últimos 6 meses", "Periodo superior a 6 meses"],
            index=None,
            placeholder="Selecciona el periodo",
        )

        masa = st.selectbox(
            "Valoración de masa muscular",
            MASA_MUSCULAR,
            index=None,
            placeholder="Selecciona la valoración",
        )

        st.subheader("Criterios etiológicos")

        ingesta_50 = st.selectbox(
            "¿Ingesta <50 % de la recomendada durante >1 semana?",
            RESPUESTAS, index=None,
        )

        ingesta_2 = st.selectbox(
            "¿Cualquier reducción de ingesta durante >2 semanas?",
            RESPUESTAS, index=None,
        )

        malabsorcion = st.selectbox(
            "¿Enfermedad digestiva crónica con impacto "
            "en asimilación o absorción?",
            RESPUESTAS, index=None,
        )

        inflamacion_aguda = st.selectbox(
            "¿Inflamación por enfermedad aguda o cirugía?",
            RESPUESTAS, index=None,
        )

        inflamacion_cronica = st.selectbox(
            "¿Inflamación relacionada con enfermedad crónica?",
            RESPUESTAS, index=None,
        )

        enviar = st.form_submit_button(
            "Evaluar GLIM",
            use_container_width=True,
        )

    if enviar:
        obligatorios = [
            edad, imc, perdida, periodo, masa,
            ingesta_50, ingesta_2, malabsorcion,
            inflamacion_aguda, inflamacion_cronica,
        ]

        if any(valor is None for valor in obligatorios):
            st.error(
                "Completa los campos GLIM. "
                "Si no se ha medido la masa muscular, "
                "selecciona «No evaluada»."
            )
            return

        errores = validar_numeros(IMC=imc, Perdida=perdida)

        if errores:
            st.error(" ".join(errores))
            return

        guardar_informe(
            "GLIM",
            identificador,
            fecha,
            calcular_glim(
                edad=edad,
                imc=imc,
                referencia=referencia,
                perdida=perdida,
                periodo=periodo,
                masa=masa,
                ingesta_50=ingesta_50 == "Sí",
                ingesta_2_semanas=ingesta_2 == "Sí",
                malabsorcion=malabsorcion == "Sí",
                inflamacion_aguda=inflamacion_aguda == "Sí",
                inflamacion_cronica=inflamacion_cronica == "Sí",
            ),
        )


# ============================================================
# NAVEGACIÓN
# ============================================================
if "informe_nutricional" not in st.session_state:
    st.session_state["informe_nutricional"] = None


def limpiar_informe():
    st.session_state["informe_nutricional"] = None


with st.sidebar:
    st.markdown(
        """
        <h2 style="text-align:center; color:#800080;">
            Valoración nutricional
        </h2>
        """,
        unsafe_allow_html=True,
    )

    score = st.selectbox(
        "¿Qué instrumento deseas calcular?",
        SCORES,
        key="score_nutricional",
        on_change=limpiar_informe,
    )

    identificador = st.text_input(
        "ID — opcional",
        help="Utiliza preferiblemente un identificador seudonimizado.",
    )

    fecha = st.date_input(
        "Fecha de valoración",
        value=date.today(),
    )

    st.caption(
        "Los cambios se aplican al pulsar el botón de cálculo."
    )


# Se evita mostrar un informe antiguo tras un envío incompleto:
# si se ha pulsado un botón de formulario, se limpia antes
# de ejecutar la validación del módulo correspondiente.
if any(
    valor is True
    for clave, valor in st.session_state.items()
    if clave.startswith("FormSubmitter:")
):
    st.session_state["informe_nutricional"] = None


RENDERIZADORES = {
    "NRS-2002": render_nrs,
    "NUTRIC-PCR": render_nutric,
    "FILNUT": render_filnut,
    "GLIM": render_glim,
}

RENDERIZADORES[score](identificador, fecha)


# ============================================================
# INFORME CENTRAL
# ============================================================
informe = st.session_state["informe_nutricional"]

if informe is not None and informe["score"] == score:
    mostrar_informe(informe)

    st.caption(
        "Se muestra el último informe calculado. "
        "Después de modificar los datos, vuelve a pulsar "
        "el botón de cálculo para actualizarlo."
    )

else:
    st.info(
        "Introduce los datos en la barra lateral "
        "y pulsa el botón de cálculo."
    )


# ============================================================
# PIE
# ============================================================
st.markdown("---")
st.caption("App desarrollada por Irene Romera / irene.r.s@outlook.com")
