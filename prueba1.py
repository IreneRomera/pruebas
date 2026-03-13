import streamlit as st
from datetime import datetime

class Paciente:
    def __init__(self, ID, edad, genero, pesokg, tallacm):
        self.ID = ID
        self.edad = edad
        self.genero = genero
        self.pesokg = pesokg
        self.tallacm = tallacm
        self.imc = None
        self.pesoideal = None
        self.pesoajustado = None
    
    def calcular_imc(self):
        imc = self.pesokg / ((self.tallacm / 100) ** 2)
        self.imc = round(imc, 2)

    def calcular_pesos(self):
        pesoidealH = round(50 + (0.75 * (self.tallacm - 152.4)), 2)
        pesoidealM = round(45.4 + (0.67 * (self.tallacm - 152.4)), 2)
        pesoajustadoH = round(pesoidealH + ((self.pesokg - pesoidealH) * 0.25), 2)
        pesoajustadoM = round(pesoidealM + ((self.pesokg - pesoidealM) * 0.25), 2)

        if self.genero == 'H':
            self.pesoideal = pesoidealH
            self.pesoajustado = pesoajustadoH
        elif self.genero == 'M':
            self.pesoideal = pesoidealM
            self.pesoajustado = pesoajustadoM

st.title("Calculadora de soporte nutricional")
st.subheader("<--Despligue para introducir los datos")

st.sidebar.header("Datos del paciente")

edad = st.sidebar.number_input("Edad", min_value=0, max_value=120, step=1)

genero_opcion = st.sidebar.radio(
    "Género",
    options=["H - Hombre", "M - Mujer"]
)
genero = genero_opcion[0]

pesokg = st.sidebar.number_input("Peso (kg)", min_value=0.0, max_value=400.0, step=0.1)
tallacm = st.sidebar.number_input("Talla (cm)", min_value=0.0, max_value=250.0, step=0.1)

if st.sidebar.button("Calcular IMC y pesos"):
    ID = f"PAC-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    paciente = Paciente(ID, edad, genero, pesokg, tallacm)
    paciente.calcular_imc()
    paciente.calcular_pesos()

    st.subheader("Resultados antropométricos del paciente")
    st.write(f"IMC: **{paciente.imc}**")
    st.write(f"Peso ideal: **{paciente.pesoideal} kg**")
    st.write(f"Peso ajustado: **{paciente.pesoajustado} kg**")
    
