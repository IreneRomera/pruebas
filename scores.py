import streamlit as st
from datetime import datetime
from streamlit_extras.buy_me_a_coffee import button

st.set_page_config(page_title="Calculadora de SCOREs")

st.title("Calculadora de diferentes SCOREs en el paciente agudo hospitalizado")
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
score_elegido = st.sidebar.selectbox(
    "¿Qué SCORE deseas calcular?",
    [
        "Clinical Frailty Scale (CFS)",
        "NEWS-2",
        # aquí irás añadiendo más scores en el futuro
    ],
)


# ------------------------------
# Clinical Frailty Scale (CFS)
# ------------------------------
if score_elegido == "Clinical Frailty Scale (CFS)":
    st.sidebar.subheader("Preguntas para CFS (respecto a las últimas 2 semanas)")

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
