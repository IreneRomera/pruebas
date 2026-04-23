
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 19:10:18 2026

@author: Prunebelly
"""

import streamlit as st
from datetime import datetime
from streamlit_extras.buy_me_a_coffee import button

st.set_page_config(page_title="Calculadora de ESCALAS")

st.title("Calculadora de diferentes escalas de aplicación en el paciente agudo hospitalizado")
st.subheader("⬅ Usa la barra lateral para introducir datos y elegir el cálculo")


# ------------------------------
# Clase Paciente (datos básicos)
# ------------------------------
class Paciente:
    def __init__(self, ID, edad, genero):
        self.ID = ID
        self.edad = edad
        self.genero = genero        # 'H' o 'M'


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
        contador += 1
    elif c4 == 2:
        contador += 2
    elif c4 == 3:
        contador += 3
    elif c4 == 4:
        contador += 4
    elif c4 == 5:
        contador += 5

    # Traducción a categoría CFS
    if contador == 1:
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


def calcular_news2(
    soporte_O2,
    fr,
    tipo_IR,
    spo2,
    pas,
    fc,
    temp,
    alteracion_consciencia,
):
    """
    Implementa tu NEWS-2 original pero en versión limpia.
    Devuelve (news2, mensaje_riesgo).
    """
    score = 0

    # a) Soporte O2
    if soporte_O2 == "Sí":
        score += 2

    # b) Frecuencia respiratoria
    if 12 <= fr <= 20:
        score += 0
    elif 21 <= fr <= 24:
        score += 2
    elif fr > 24:
        score += 3
    elif 9 <= fr < 12:
        score += 1
    elif fr < 9:
        score += 3

    # c + d) Tipo de IR y SpO2 (tu lógica original)
    if tipo_IR == "Hipoxémica":
        if spo2 > 95:
            score += 0
        elif 94 <= spo2 <= 95:
            score += 1
        elif 92 <= spo2 <= 93:
            score += 2
        elif spo2 < 92:
            score += 3
    else:  # Hipercápnica
        if spo2 > 96:
            score += 3
        elif 95 <= spo2 <= 96:
            score += 2
        elif 93 <= spo2 <= 94:
            score += 1
        elif 88 <= spo2 <= 92:
            score += 0
        elif 86 <= spo2 <= 87:
            score += 1
        elif 84 <= spo2 <= 85:
            score += 2
        elif spo2 < 84:
            score += 3

    # e) PAS
    if pas > 219:
        score += 3
    elif 111 <= pas <= 219:
        score += 0
    elif 101 <= pas <= 110:
        score += 1
    elif 91 <= pas <= 100:
        score += 2
    elif pas < 91:
        score += 3

    # f) FC
    if fc > 130:
        score += 3
    elif 111 <= fc <= 130:
        score += 2
    elif 91 <= fc <= 110:
        score += 1
    elif 51 <= fc <= 90:
        score += 0
    elif 41 <= fc <= 50:
        score += 1
    elif fc < 41:
        score += 3

    # g) Temperatura
    if temp > 39:
        score += 2
    elif 38.1 <= temp <= 39:
        score += 1
    elif 36.1 <= temp <= 38:
        score += 0
    elif 35.1 <= temp <= 36:
        score += 1
    elif temp < 35.1:
        score += 3

    # h) Nivel de consciencia
    if alteracion_consciencia == "Sí":
        score += 3

    # Mensaje de riesgo (según tus textos)
    if score >= 7:
        msg = (
            "Situación de alto riesgo. Se recomienda una valoración emergente "
            "por el equipo de Medicina Intensiva."
        )
    elif 5 <= score <= 6:
        msg = (
            "Situación de riesgo intermedio. Se recomienda una valoración urgente "
            "por el equipo médico de planta."
        )
    else:
        msg = (
            "Situación de bajo riesgo. Se recomienda mantener la vigilancia "
            "por el equipo de enfermería de planta."
        )

    return score, msg


def calcular_qsofa(alteracion_consciencia, pam_menor_100, fr_mayor_22):
    """
    Calcula qSOFA según los 3 criterios:
    - Alteración del nivel de consciencia
    - PAM ≤ 100 mmHg  
    - FR ≥ 22 rpm
    Devuelve (score, interpretacion)
    """
    score = 0
    
    if alteracion_consciencia == "Sí":
        score += 1
    if pam_menor_100 == "Sí":
        score += 1
    if fr_mayor_22 == "Sí":
        score += 1
    
    if score == 1:
        interpretacion = (
            "Se recomienda repetir el qSOFA frecuentemente y continuar evaluando al paciente."
        )
    elif score >= 2:
        interpretacion = (
            "Se recomienda vigilar la aparición de disfunción orgánica y establecer las "
            "medidas diagnósticas y terapéuticas necesarias. Existe mayor riesgo de mortalidad "
            "hospitalaria o prolongada estancia en pacientes con sospecha de infección."
        )
    else:
        interpretacion = "qSOFA negativo. Continuar con vigilancia rutinaria."
    
    return score, interpretacion


def calcular_sofa(
    gcs,
    tipo_relacion,          # "SaO2/FiO2" o "PaO2/FiO2"
    relacion,
    hemodinamica,          # 1-5
    creatinina,            # 1-5
    bilirrubina,           # 1-5
    plaquetas              # 1-5
):
    """
    Calcula el SOFA total y devuelve:
    - score total
    - texto sobre la mortalidad esperada
    """
    score = 0

    # A) GCS
    if gcs == 15:
        score += 0
    elif gcs in (13, 14):
        score += 1
    elif 10 <= gcs < 13:
        score += 2
    elif 6 <= gcs < 10:
        score += 3
    elif gcs < 6:
        score += 4

    # B) SaFi o PaFi
    if tipo_relacion == "SaO₂/FiO₂":
        # Usamos los mismos puntos que tu código original
        if relacion > 512:
            score += 0
        elif 357 <= relacion <= 512:
            score += 1
        elif 214 <= relacion < 357:
            score += 2
        elif 89 <= relacion < 214:
            score += 3
        elif relacion < 89:
            score += 4
    else:  # PaO2/FiO2
        if relacion >= 400:
            score += 0
        elif 300 <= relacion < 400:
            score += 1
        elif 200 <= relacion < 300:
            score += 2
        elif 100 <= relacion < 200:
            score += 3
        elif relacion < 100:
            score += 4

    # C) Hemodinámica (1-5 tal como en tu código)
    if hemodinamica == 1:
        score += 0
    elif hemodinamica == 2:
        score += 1
    elif hemodinamica == 3:
        score += 2
    elif hemodinamica == 4:
        score += 3
    elif hemodinamica == 5:
        score += 4

    # D) Creatinina
    if creatinina == 1:
        score += 0
    elif creatinina == 2:
        score += 1
    elif creatinina == 3:
        score += 2
    elif creatinina == 4:
        score += 3
    elif creatinina == 5:
        score += 4

    # E) Bilirrubina
    if bilirrubina == 1:
        score += 0
    elif bilirrubina == 2:
        score += 1
    elif bilirrubina == 3:
        score += 2
    elif bilirrubina == 4:
        score += 3
    elif bilirrubina == 5:
        score += 4

    # F) Plaquetas
    if plaquetas == 1:
        score += 0
    elif plaquetas == 2:
        score += 1
    elif plaquetas == 3:
        score += 2
    elif plaquetas == 4:
        score += 3
    elif plaquetas == 5:
        score += 4

    # Estimación de mortalidad aproximada
    if score <= 4:
        mortalidad = "Mortalidad esperada aproximada 5–10%."
    elif 5 <= score <= 5:
        mortalidad = "Mortalidad esperada aproximada al menos 10–20%."
    elif 6 <= score <= 8:
        mortalidad = "Mortalidad esperada aproximada 20–33%."
    elif 9 <= score <= 11:
        mortalidad = "Mortalidad esperada aproximada 40–50%."
    elif 12 <= score <= 14:
        mortalidad = "Mortalidad esperada aproximada 60–75%."
    else:  # >= 15
        mortalidad = "La mortalidad esperada es superior al 90%."

    return score, (
        "El aumento del SOFA score en las últimas 48 h supone un aumento de mortalidad "
        "de al menos el 50%. " + mortalidad
    )

def contar_disfuncion_leve(
    gcs,
    tipo_relacion,
    relacion,
    hemodinamica,
    creatinina,
    bilirrubina,
    plaquetas,
):
    """
    Reproduce tu lógica original de 'disfunción leve':
    - cuenta órganos con puntuación 2 (c, d, e, f)
    - +1 si PaFi entre 200-300 (equivalente a score 2 respiratorio)
    - +1 si GCS 12-14 (equivalente a score 1-2 neurológico, tú usabas >=12 y <15)
    """
    contador = 0

    # c, d, e, f = 2
    for valor in [hemodinamica, creatinina, bilirrubina, plaquetas]:
        if valor == 2:
            contador += 1

    # Respiratorio
    if tipo_relacion == "PaO₂/FiO₂":
        if 200 < relacion <= 300:
            contador += 1
    else:
        # No tenías definición explícita de disfunción leve con SaFi;
        # si quieres podríamos añadir un criterio equivalente más adelante.
        pass

    # Neurológico
    if 10 <= gcs < 12:
        contador += 1

    return contador


def contar_disfuncion_grave(
    gcs,
    tipo_relacion,
    relacion,
    hemodinamica,
    creatinina,
    bilirrubina,
    plaquetas,
):
    """
    Tu lógica de 'disfunción grave':
    - cuenta órganos con puntuación 3 (c, d, e, f)
    - +1 si PaFi entre 100-200
    - +1 si GCS entre 6-9
    """
    contador = 0

    for valor in [hemodinamica, creatinina, bilirrubina, plaquetas]:
        if valor == 3:
            contador += 1

    if tipo_relacion == "PaO₂/FiO₂":
        if 100 <= relacion <= 200:
            contador += 1

    if 6 <= gcs < 10:
        contador += 1

    return contador


def contar_fallo_organico(
    gcs,
    tipo_relacion,
    relacion,
    hemodinamica,
    creatinina,
    bilirrubina,
    plaquetas,
):
    """
    Tu lógica de 'fallo':
    - cuenta órganos con puntuación 4 o 5 (c, d, e, f)
    - +1 si PaFi < 100
    - +1 si GCS < 6
    """
    contador = 0

    for valor in [hemodinamica, creatinina, bilirrubina, plaquetas]:
        if valor in (4, 5):
            contador += 1

    if tipo_relacion == "PaO₂/FiO₂":
        if relacion < 100:
            contador += 1

    if gcs < 6:
        contador += 1

    return contador








# ------------------------------
# Barra lateral: datos del paciente
# ------------------------------

st.sidebar.header("Datos del paciente")

edad = st.sidebar.number_input("Edad (años)", min_value=0, max_value=110, step=1)

genero_opcion = st.sidebar.radio(
    "Género",
    options=["H - Hombre", "M - Mujer"],
)
genero = genero_opcion[0]  # 'H' o 'M'


ID = f"PAC-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
paciente = Paciente(ID, edad, genero)

st.sidebar.markdown("---")




# ------------------------------
# Elegir SCORE
# ------------------------------
st.sidebar.markdown(
    """
    <h2 style='text-align: center; color: #003366;'>
        ¿Qué ESCALA deseas calcular?
    </h2>
    """,
    unsafe_allow_html=True,
)

score_elegido = st.sidebar.selectbox(
    "",
    [
        "Clinical Frailty Scale (CFS)",
        "Clinical Frailty Scale (CFS) flowchart",
        "NEWS-2",
        "qSOFA",  
        "SOFA score",
    ],
)


# ------------------------------
# Clinical Frailty Scale (CFS)
# ------------------------------
if score_elegido == "Clinical Frailty Scale (CFS)":
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
            "Problemas de salud bien controlados y ejercicio más allá de caminar",
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
        "Problemas de salud bien controlados y ejercicio más allá de caminar": "f7",
        "Sin síntomas activos y realiza ejercicio ocasional": "f8",
        "Realiza ejercicio regular y está más ágil/'fit' de lo esperado para su edad": "f9",
    }

    codigo = mapa_opciones_a_codigo[opcion_cfs_simpl]

    cfs_simpl, desc_simpl = calcular_cfs_simplificado(codigo)

    st.info(desc_simpl)


# ------------------------------
# NEWS-2
# ------------------------------
if score_elegido == "NEWS-2":
    st.sidebar.subheader("Parámetros para NEWS-2")

    soporte_O2 = st.sidebar.radio(
        "¿Precisa soporte con O₂?",
        options=["No", "Sí"],
    )

    fr = st.sidebar.number_input(
        "Frecuencia respiratoria (rpm)",
        min_value=0,
        max_value=80,
        value=16,
        step=1,
    )

    tipo_IR = st.sidebar.radio(
        "Tipo de insuficiencia respiratoria",
        options=["Hipoxémica", "Hipercápnica"],
    )

    spo2 = st.sidebar.number_input(
        "SpO₂ (%)",
        min_value=50,
        max_value=100,
        value=96,
        step=1,
    )

    pas = st.sidebar.number_input(
        "Presión arterial sistólica (mmHg)",
        min_value=40,
        max_value=260,
        value=120,
        step=1,
    )

    fc = st.sidebar.number_input(
        "Frecuencia cardiaca (lpm)",
        min_value=20,
        max_value=220,
        value=80,
        step=1,
    )

    temp = st.sidebar.number_input(
        "Temperatura (ºC)",
        min_value=30.0,
        max_value=43.0,
        value=36.5,
        step=0.1,
    )

    alteracion_consciencia = st.sidebar.radio(
        "¿Hay disminución del nivel de consciencia?",
        options=["No", "Sí"],
    )

    boton_news = st.sidebar.button("Calcular NEWS-2")

    if boton_news:
        news2, mensaje = calcular_news2(
            soporte_O2,
            fr,
            tipo_IR,
            spo2,
            pas,
            fc,
            temp,
            alteracion_consciencia,
        )

        st.subheader("NEWS-2")
        st.write(f"La puntuación NEWS-2 es de  **{news2} puntos**")
        st.info(mensaje)


# ------------------------------
# qSOFA 
# ------------------------------
if score_elegido == "qSOFA":
    st.sidebar.subheader("Parámetros para qSOFA")
    
    alteracion_consciencia_qsofa = st.sidebar.radio(
        "¿Existe alteración del nivel de consciencia?",
        options=["No", "Sí"],
    )
    
    pam_menor_100 = st.sidebar.radio(
        "¿La PAM es ≤ 100 mmHg?",
        options=["No", "Sí"],
    )
    
    fr_mayor_22 = st.sidebar.radio(
        "¿La FR es ≥ 22 rpm?",
        options=["No", "Sí"],
    )
    
    boton_qsofa = st.sidebar.button("Calcular qSOFA")
    
    if boton_qsofa:
        qsofa_score, interpretacion = calcular_qsofa(
            alteracion_consciencia_qsofa,
            pam_menor_100,
            fr_mayor_22
        )
        
        st.subheader("qSOFA")
        
        # Información previa (siempre visible al calcular)
        with st.expander("ℹ️ Información sobre qSOFA", expanded=True):
            st.info("""
            **El qSOFA tiene una sensibilidad baja para el diagnóstico de sepsis** en 
            comparación para otras escalas, por lo que **no se recomienda como herramienta 
            única de cribado de sepsis** en el paciente hospitalizado. 
            
            No obstante, se considera una **buena herramienta para detectar el deterioro 
            clínico general** de los pacientes y como predictor de mortalidad y/o estancia 
            prolongada en UCI en pacientes con una infección sospechada o confirmada. 
            
            **Un qSOFA positivo debe activar una evaluación clínica inmediata** y la 
            búsqueda de una posible disfunción orgánica.
            """)
        
        # Resultado
        st.success(f"**El qSOFA score es de {qsofa_score} puntos**")
        st.info(interpretacion)


# ------------------------------
# SOFA score
# ------------------------------
if score_elegido == "SOFA score":
    st.sidebar.subheader("Parámetros para SOFA")

    # GCS
    gcs = st.sidebar.number_input(
        "Glasgow Coma Scale (GCS)",
        min_value=3,
        max_value=15,
        value=15,
        step=1,
    )

    # Relación SaFi / PaFi
    tipo_relacion = st.sidebar.radio(
        "¿Qué relación desea utilizar?",
        options=["SaO₂/FiO₂", "PaO₂/FiO₂"],
    )

    if tipo_relacion == "SaO₂/FiO₂":
        spo2 = st.sidebar.number_input(
            "SpO₂ (%)",
            min_value=50,
            max_value=100,
            value=96,
            step=1,
        )
        fio2 = st.sidebar.number_input(
            "FiO₂ (%)",
            min_value=21,
            max_value=100,
            value=21,
            step=1,
        )
        relacion = spo2 / (fio2 / 100.0)
    else:
        pao2 = st.sidebar.number_input(
            "PaO₂ (mmHg)",
            min_value=30,
            max_value=600,
            value=80,
            step=1,
        )
        fio2 = st.sidebar.number_input(
            "FiO₂ (%)",
            min_value=21,
            max_value=100,
            value=21,
            step=1,
        )
        relacion = pao2 / (fio2 / 100.0)

    # C) Situación hemodinámica
    hemodinamica_opcion = st.sidebar.selectbox(
        "Situación hemodinámica del paciente",
        options=[
            "1) Ausencia de hipotensión",
            "2) PAM < 70 mmHg",
            "3) DPM < 5 o DBT",
            "4) DPM > 5 o NAD < 0.1 o ADR < 0.1",
            "5) DPM > 15 o NAD > 0.1 o ADR > 0.1",
        ],
    )
    hemodinamica = int(hemodinamica_opcion.split(")")[0])

    # D) Creatinina
    creatinina_opcion = st.sidebar.selectbox(
        "Creatinina sérica",
        options=[
            "1) < 1.2 mg/dL (< 110 µmol/L)",
            "2) 1.2 - 1.9 mg/dL (110-170 µmol/L)",
            "3) 2 - 3.4 mg/dL (171-299 µmol/L)",
            "4) 3.5 - 4.9 mg/dL (300-439 µmol/L) o diuresis < 500 mL/día",
            "5) > 5 mg/dL (> 440 µmol/L) o diuresis < 200 mL/día",
        ],
    )
    creatinina = int(creatinina_opcion.split(")")[0])

    # E) Bilirrubina
    bilirrubina_opcion = st.sidebar.selectbox(
        "Bilirrubina sérica",
        options=[
            "1) < 1.2 mg/dL (< 20 µmol/L)",
            "2) 1.2 - 1.9 mg/dL (20-32 µmol/L)",
            "3) 2 - 5.9 mg/dL (32-101 µmol/L)",
            "4) 6 - 11.9 mg/dL (102-204 µmol/L)",
            "5) > 12 mg/dL (> 205 µmol/L)",
        ],
    )
    bilirrubina = int(bilirrubina_opcion.split(")")[0])

    # F) Plaquetas
    plaquetas_opcion = st.sidebar.selectbox(
        "Plaquetas (x10³/mcL)",
        options=[
            "1) ≥ 150",
            "2) 150 - 100",
            "3) 99 - 50",
            "4) 49 - 20",
            "5) < 20",
        ],
    )
    plaquetas = int(plaquetas_opcion.split(")")[0])

    boton_sofa = st.sidebar.button("Calcular SOFA")

    if boton_sofa:
        score_sofa, texto_sofa = calcular_sofa(
            gcs,
            tipo_relacion,
            relacion,
            hemodinamica,
            creatinina,
            bilirrubina,
            plaquetas,
        )

        st.subheader("SOFA score")

        with st.expander("ℹ️ Información sobre SOFA", expanded=True):
            st.info(
                "El SOFA (Sequential Organ Failure Assessment) evalúa la disfunción de 6 órganos "
                "(respiratorio, coagulación, hepático, cardiovascular, neurológico y renal). "
                "Se utiliza para cuantificar la gravedad y como predictor de mortalidad."
            )

        st.success(f"**El SOFA score es de {score_sofa} puntos**")
        st.info(texto_sofa)

        # --- Disfunción leve, grave y fallo orgánico ---
        n_leve = contar_disfuncion_leve(
            gcs,
            tipo_relacion,
            relacion,
            hemodinamica,
            creatinina,
            bilirrubina,
            plaquetas,
        )
        n_grave = contar_disfuncion_grave(
            gcs,
            tipo_relacion,
            relacion,
            hemodinamica,
            creatinina,
            bilirrubina,
            plaquetas,
        )
        n_fallo = contar_fallo_organico(
            gcs,
            tipo_relacion,
            relacion,
            hemodinamica,
            creatinina,
            bilirrubina,
            plaquetas,
        )

        st.markdown("### Disfunción / fallo de órganos")

        st.write(
            f"Existe **disfunción leve** de `{n_leve}` órganos, "
            f"**disfunción grave** de `{n_grave}` órganos y "
            f"**fallo** de `{n_fallo}` órganos."
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


        

