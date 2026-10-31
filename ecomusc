#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 17:38:17 2026

@author: Prunebelly
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Calculadora e informe de ecografía muscular.
"""


from streamlit_extras.buy_me_a_coffee import button
from datetime import date, datetime
from io import BytesIO
from statistics import mean
from xml.sax.saxutils import escape
import math
import re

import pandas as pd
import streamlit as st

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


# ------------------------------
# Configuración general
# ------------------------------
st.set_page_config(
    page_title="Calculadora de ecografía muscular",
    layout="centered",
)

st.title("Calculadora de ecografía muscular")
st.subheader("⬅ Introduce los datos en la barra lateral y genera el informe")


# ------------------------------
# Funciones auxiliares
# ------------------------------
def formato_numero(valor, decimales=2):
    """Formato numérico para pantalla y PDF."""
    if valor is None:
        return "No calculable"

    return f"{valor:.{decimales}f}".replace(".", ",")


def calcular_resultados(mediciones, area_previa):
    """Calcula las medias, el cociente y el delta sin redondear."""
    media_y = mean(m["eje_y"] for m in mediciones)
    media_relajacion = mean(m["relajacion"] for m in mediciones)
    media_contraccion = mean(m["contraccion"] for m in mediciones)

    cociente = (
        media_relajacion/ media_contraccion
        if media_relajacion > 0
        else None
    )

    delta = (
        (media_relajacion - area_previa) / area_previa
        if area_previa is not None and area_previa > 0
        else None
    )

    return {
        "media_y": media_y,
        "media_relajacion": media_relajacion,
        "media_contraccion": media_contraccion,
        "cociente": cociente,
        "delta": delta,
    }


def crear_filas_mediciones(informe):
    """Tabla común para pantalla y PDF."""
    mediciones = informe["mediciones"]
    resultados = informe["resultados"]

    filas = []

    variables = [
        ("Eje Y (cm)", "eje_y", "media_y"),
        (
            "Área en relajación (cm²)",
            "relajacion",
            "media_relajacion",
        ),
        (
            "Área en contracción (cm²)",
            "contraccion",
            "media_contraccion",
        ),
    ]

    for etiqueta, campo, campo_media in variables:
        filas.append([
            etiqueta,
            *[
                formato_numero(m[campo])
                for m in mediciones
            ],
            formato_numero(resultados[campo_media]),
        ])

    return filas


def generar_pdf(informe):
    """Devuelve el informe PDF como bytes."""
    buffer = BytesIO()

    documento = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=1.6 * cm,
        leftMargin=1.6 * cm,
        topMargin=1.6 * cm,
        bottomMargin=1.6 * cm,
    )

    estilos = getSampleStyleSheet()
    elementos = []

    def texto(contenido, estilo="BodyText"):
        elementos.append(
            Paragraph(escape(str(contenido)), estilos[estilo])
        )
        elementos.append(Spacer(1, 0.15 * cm))

    def tabla(datos, anchos, encabezado=False):
        tabla_pdf = Table(
            datos,
            colWidths=anchos,
            repeatRows=1 if encabezado else 0,
            hAlign="LEFT",
        )

        instrucciones = [
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.lightgrey),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ]

        if encabezado:
            instrucciones.extend([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#800080")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ALIGN", (1, 0), (-1, -1), "CENTER"),
            ])

        tabla_pdf.setStyle(TableStyle(instrucciones))
        elementos.append(tabla_pdf)
        elementos.append(Spacer(1, 0.4 * cm))

    resultados = informe["resultados"]

    texto("Informe de ecografía muscular", "Title")

    texto(f"ID: {informe['id']}")
    texto(f"Fecha de exploración: {informe['fecha'].strftime('%Y%m%d')}")
    texto(
        f"Localización: {formato_numero(informe['localizacion'])} cm "
        f"en el lado {informe['lado'].lower()}."
    )

    texto("Mediciones y medias", "Heading2")

    tabla(
        [
            ["Variable", "Medición 1", "Medición 2", "Medición 3", "Media"],
            *crear_filas_mediciones(informe),
        ],
        [6.0 * cm, 2.5 * cm, 2.5 * cm, 2.5 * cm, 2.3 * cm],
        encabezado=True,
    )

    texto("Cociente de áreas", "Heading2")
    texto(
        "Media del área en contracción / media del área en relajación: "
        f"{formato_numero(resultados['cociente'], 4)}."
    )

    texto("Características adicionales", "Heading2")
    texto(
        f"Grosor del tendón: "
        f"{formato_numero(informe['grosor_tendon'])} mm."
    )
    texto(f"Ecogenicidad: {informe['ecogenicidad']}.")
    texto(f"Edema: {informe['edema']}.")

    texto("Evolución del área", "Heading2")

    area_previa_texto = (
        f"{formato_numero(informe['area_previa'])} cm²"
        if informe["area_previa"] is not None
        else "No introducida"
    )

    texto(f"Área previa: {area_previa_texto}.")
    texto(
        "Área actual, media en relajación: "
        f"{formato_numero(resultados['media_relajacion'])} cm²."
    )

    if resultados["delta"] is not None:
        texto(f"Delta del área: {formato_numero(resultados['delta'], 4)}.")
        texto(
            "Variación porcentual: "
            f"{formato_numero(resultados['delta'] * 100)} %."
        )
    else:
        texto(
            "Delta del área: no calculable. "
            "Se necesita un área previa mayor que cero."
        )

    texto(
        "Fórmula: (media del área en relajación - área previa) / área previa."
    )

    elementos.append(Spacer(1, 0.4 * cm))

    texto(
        "Informe descriptivo de los datos introducidos. "
        "No incorpora interpretación clínica automática."
    )
    texto(f"Generado el {informe['generado_el']}.")

    documento.build(elementos)
    return buffer.getvalue()


def mostrar_informe(informe):
    """Presenta en pantalla el informe generado."""
    resultados = informe["resultados"]

    st.header("Informe de ecografía muscular")

    col1, col2 = st.columns(2)

    col1.write(f"ID: {informe['id']}")
    col2.write(
        f"Fecha: {informe['fecha'].strftime('%Y%m%d')}"
    )

    st.write(
        f"Localización: {formato_numero(informe['localizacion'])} cm "
        f"en el lado {informe['lado'].lower()}."
    )

    st.subheader("Mediciones y medias")

    tabla_mediciones = pd.DataFrame(
        crear_filas_mediciones(informe),
        columns=[
            "Variable",
            "Medición 1",
            "Medición 2",
            "Medición 3",
            "Media",
        ],
    )

    st.dataframe(
        tabla_mediciones,
        hide_index=True,
        use_container_width=True,
    )

    st.subheader("Cociente de áreas")

    st.metric(
        "Contracción / relajación",
        formato_numero(resultados["cociente"], 4),
    )

    if resultados["cociente"] is None:
        st.warning(
            "No se puede calcular el cociente porque "
            "la media del área en relajación es cero."
        )

    st.subheader("Características adicionales")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Grosor del tendón",
        f"{formato_numero(informe['grosor_tendon'])} mm",
    )
    col2.metric("Ecogenicidad", informe["ecogenicidad"])
    col3.metric("Edema", informe["edema"])

    st.subheader("Evolución del área")

    col1, col2 = st.columns(2)

    col1.metric(
        "Área previa",
        (
            f"{formato_numero(informe['area_previa'])} cm²"
            if informe["area_previa"] is not None
            else "No introducida"
        ),
    )

    col2.metric(
        "Área actual: media en relajación",
        f"{formato_numero(resultados['media_relajacion'])} cm²",
    )

    if resultados["delta"] is not None:
        col1, col2 = st.columns(2)

        col1.metric(
            "Delta del área",
            formato_numero(resultados["delta"], 4),
        )

        col2.metric(
            "Variación porcentual",
            f"{formato_numero(resultados['delta'] * 100)} %",
        )
    else:
        st.info(
            "Delta del área no calculable: introduce un área previa "
            "mayor que cero si deseas calcular la evolución."
        )

    st.caption(
        "Delta = (media del área en relajación − área previa) / área previa."
    )

    st.caption(
        "Informe descriptivo, sin interpretación clínica automática."
    )


# ------------------------------
# Estado de sesión
# ------------------------------
if "informe_eco" not in st.session_state:
    st.session_state.informe_eco = None

if "pdf_eco" not in st.session_state:
    st.session_state.pdf_eco = None


# ------------------------------
# Barra lateral: entrada de datos
# ------------------------------
with st.sidebar:
    st.markdown(
        """
        <h2 style="text-align: center; color: #800080;">
            Datos de la exploración
        </h2>
        """,
        unsafe_allow_html=True,
    )

    st.caption(
        "Los cambios se aplican al pulsar «Generar informe»."
    )

    with st.form("formulario_eco"):
        identificador = st.text_input(
            "ID",
            help="Utiliza preferiblemente un identificador seudonimizado.",
        )

        fecha = st.date_input(
            "Fecha de exploración",
            value=date.today(),
        )

        st.caption(
            "La fecha se mostrará en el informe como AAAAMMDD "
            "(año, mes y día)."
        )

        st.subheader("Localización")

        localizacion = st.number_input(
            "Localización (cm)",
            min_value=0.0,
            value=None,
            step=0.1,
            format="%.2f",
            key="eco_localizacion",
        )

        lado = st.selectbox(
            "Lado",
            ["Derecho", "Izquierdo"],
            index=None,
            placeholder="Selecciona el lado",
        )

        mediciones = []

        for numero in range(1, 4):
            st.subheader(f"Medición {numero}")

            eje_y = st.number_input(
                "Eje Y (cm)",
                min_value=0.0,
                value=None,
                step=0.01,
                format="%.3f",
                key=f"eco_eje_y_{numero}",
            )

            relajacion = st.number_input(
                "Área en relajación (cm²)",
                min_value=0.0,
                value=None,
                step=0.01,
                format="%.3f",
                key=f"eco_relajacion_{numero}",
            )

            contraccion = st.number_input(
                "Área en contracción (cm²)",
                min_value=0.0,
                value=None,
                step=0.01,
                format="%.3f",
                key=f"eco_contraccion_{numero}",
            )

            mediciones.append({
                "eje_y": eje_y,
                "relajacion": relajacion,
                "contraccion": contraccion,
            })

        st.subheader("Características adicionales")

        grosor_tendon = st.number_input(
            "Grosor del tendón (mm)",
            min_value=0.0,
            value=None,
            step=0.01,
            format="%.3f",
        )

        ecogenicidad = st.selectbox(
            "Ecogenicidad",
            [
                "Categoría 1",
                "Categoría 2",
                "Categoría 3",
                "Categoría 4",
            ],
            index=None,
            placeholder="Selecciona una categoría",
        )

        edema = st.selectbox(
            "Edema",
            ["Sí", "No"],
            index=None,
            placeholder="Selecciona una opción",
        )

        st.subheader("Seguimiento")

        area_previa = st.number_input(
            "Área previa (cm²)",
            min_value=0.0,
            value=None,
            step=0.01,
            format="%.3f",
            help=(
                "Opcional. Déjalo vacío si no hay medición previa. "
                "El delta requiere un valor mayor que cero."
            ),
        )

        generar = st.form_submit_button(
            "Generar informe",
            use_container_width=True,
        )


# ------------------------------
# Validación y generación
# ------------------------------
if generar:
    errores = []

    if not identificador.strip():
        errores.append("Introduce el ID.")

    if localizacion is None:
        errores.append("Introduce la localización.")

    if lado is None:
        errores.append("Selecciona el lado.")

    nombres_campos = {
        "eje_y": "eje Y",
        "relajacion": "área en relajación",
        "contraccion": "área en contracción",
    }

    for numero, medicion in enumerate(mediciones, start=1):
        for campo, valor in medicion.items():
            if valor is None:
                errores.append(
                    f"Completa {nombres_campos[campo]} "
                    f"de la medición {numero}."
                )

    if grosor_tendon is None:
        errores.append("Introduce el grosor del tendón.")

    if ecogenicidad is None:
        errores.append("Selecciona la ecogenicidad.")

    if edema is None:
        errores.append("Indica si hay edema.")

    valores_numericos = [
        localizacion,
        grosor_tendon,
        area_previa,
        *[
            valor
            for medicion in mediciones
            for valor in medicion.values()
        ],
    ]

    if any(
        valor is not None and not math.isfinite(valor)
        for valor in valores_numericos
    ):
        errores.append("Todos los valores numéricos deben ser finitos.")

    if errores:
        # Evita presentar un informe anterior tras un envío incorrecto.
        st.session_state.informe_eco = None
        st.session_state.pdf_eco = None

        for error in errores:
            st.error(error)

    else:
        resultados = calcular_resultados(
            mediciones,
            area_previa,
        )

        informe = {
            "id": identificador.strip(),
            "fecha": fecha,
            "localizacion": localizacion,
            "lado": lado,
            "mediciones": mediciones,
            "grosor_tendon": grosor_tendon,
            "ecogenicidad": ecogenicidad,
            "edema": edema,
            "area_previa": area_previa,
            "resultados": resultados,
            "generado_el": datetime.now().strftime("%d/%m/%Y %H:%M"),
        }

        st.session_state.informe_eco = informe
        st.session_state.pdf_eco = None

        try:
            st.session_state.pdf_eco = generar_pdf(informe)
        except Exception:
            st.error(
                "El informe se ha calculado, pero no se ha podido "
                "generar el PDF. Revisa la instalación de ReportLab."
            )


# ------------------------------
# Zona central y descarga
# ------------------------------
if st.session_state.informe_eco is not None:
    informe = st.session_state.informe_eco

    mostrar_informe(informe)

    st.caption(
        "Se muestra el último informe generado. "
        "Si modificas los datos laterales, pulsa «Generar informe» "
        "para actualizarlo y renovar el PDF."
    )

    if st.session_state.pdf_eco is not None:
        id_archivo = re.sub(
            r"[^A-Za-z0-9_-]+",
            "_",
            informe["id"],
        )[:60] or "sin_id"

        fecha_archivo = informe["fecha"].strftime("%Y%m%d")

        st.download_button(
            label="Descargar informe en PDF",
            data=st.session_state.pdf_eco,
            file_name=f"informe_eco_{id_archivo}_{fecha_archivo}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

else:
    st.info(
        "Completa los datos en la barra lateral "
        "y pulsa «Generar informe»."
    )


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
