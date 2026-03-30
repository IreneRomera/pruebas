#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 19:23:59 2026

@author: Prunebelly
"""

import streamlit as st
from datetime import datetime
from streamlit_extras.buy_me_a_coffee import button

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
        self.kcal_requeridas = None
        self.prote_requeridas = None
        self.vol_ne_ml_dia = None
        self.vol_ne_ml_h = None
        self.prote_ne = None
        self.prote_extra = None

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

    def calcular_ne(self, objetivo_kcal_kg_dia, objetivo_prot_kg_dia,
                    estres_alto, kcal_por_ml, prote_gramos_100ml):
        """
        estres_alto: True si z == 1, False si z == 2
        """
        if self.imc is None or self.pesoajustado is None or self.pesoideal is None:
            raise ValueError("Primero hay que calcular IMC y pesos.")

        peso_base = self.pesokg

        # factor estrés
        factor_estres = 0.7 if estres_alto else 1.0

        # --- Necesidades calóricas ---
        if self.imc < 30:
            kcal = int(objetivo_kcal_kg_dia * peso_base * factor_estres)
        elif 30 <= self.imc <= 35:
            kcal = int(objetivo_kcal_kg_dia * self.pesoajustado * factor_estres)
        else:  # IMC > 35
            kcal = int(objetivo_kcal_kg_dia * self.pesoajustado * factor_estres)

        self.kcal_requeridas = kcal

        # --- Necesidades proteicas ---
        if self.imc < 30:
            prote = int(objetivo_prot_kg_dia * peso_base * factor_estres)
        elif 30 <= self.imc <= 35:
            prote = int(objetivo_prot_kg_dia * self.pesoajustado * factor_estres)
        else:  # IMC > 35
            prote = int(objetivo_prot_kg_dia * self.pesoideal * factor_estres)

        self.prote_requeridas = prote

        # --- Dosis de NE ---
        vol_ne = self.kcal_requeridas / kcal_por_ml          # mL/día
        self.vol_ne_ml_dia = int(vol_ne)
        self.vol_ne_ml_h = round(vol_ne / 24, 1)

        self.prote_ne = int((vol_ne / 100.0) * prote_gramos_100ml)
        self.prote_extra = max(self.prote_requeridas - self.prote_ne, 0)


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

st.sidebar.markdown("---")
st.sidebar.subheader("Objetivos de nutrición enteral")

objetivo_kcal = st.sidebar.number_input(
    "Objetivo calórico (kcal/kg/día)",
    min_value=0.0, max_value=80.0, value=25.0, step=0.5
)

objetivo_prot = st.sidebar.number_input(
    "Objetivo proteico (g/kg/día)",
    min_value=0.0, max_value=5.0, value=1.3, step=0.1
)

estres_opcion = st.sidebar.radio(
    "Situación de estrés metabólico elevado / hiperagudo / empeoramiento clínico",
    options=["No", "Sí"]
)
estres_alto = (estres_opcion == "Sí")

kcal_por_ml = st.sidebar.number_input(
    "kcal/mL de la NE a utilizar",
    min_value=0.1, max_value=5.0, value=1.0, step=0.1
)

prote_100ml = st.sidebar.number_input(
    "g de proteínas por 100 mL de NE",
    min_value=0.0, max_value=30.0, value=4.0, step=0.1
)



if st.sidebar.button("Calcular dosis de nutrición enteral"):
    # Comprobamos que hay datos razonables
    if tallacm <= 0 or pesokg <= 0:
        st.error("Introduce primero un peso y una talla válidos.")
    else:
        ID = f"PAC-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        paciente = Paciente(ID, edad, genero, pesokg, tallacm)
        paciente.calcular_imc()
        paciente.calcular_pesos()
        paciente.calcular_ne(
            objetivo_kcal_kg_dia=objetivo_kcal,
            objetivo_prot_kg_dia=objetivo_prot,
            estres_alto=estres_alto,
            kcal_por_ml=kcal_por_ml,
            prote_gramos_100ml=prote_100ml,
        )

        st.subheader("Dosis de nutrición enteral")

        st.write(f"IMC: **{paciente.imc}**")
        st.write(f"Kcal requeridas: **{paciente.kcal_requeridas} kcal/día**")
        st.write(f"Proteínas requeridas: **{paciente.prote_requeridas} g/día**")

        st.markdown("---")
        st.write(f"Volumen de NE: **{paciente.vol_ne_ml_dia} mL/día**")
        st.write(f"Velocidad de perfusión: **{paciente.vol_ne_ml_h} mL/h**")
        st.write(f"Proteínas aportadas por la NE: **{paciente.prote_ne} g/día**")
        st.write(f"Proteínas extra necesarias: **{paciente.prote_extra} g/día**")


st.markdown("---")
st.caption("App desarrollada por Irene Romera / irene.r.s@outlook.com 😊")
st.write("Si esta calculadora te resulta útil …")

button(
    username="ireneromera",      # tu usuario de buymeacoffee.com
    floating=False,                  # que no flote, aparece en el flujo normal
    text="Invítame a un té",
    emoji="🍵",
    bg_color="#FFDD00",
    font_color="#000000"
)
