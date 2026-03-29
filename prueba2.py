#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 17:57:35 2026

@author: Prunebelly
"""

import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Calculadora de sueroterapia y electrolitos")

st.title("Calculadora de sueroterapia y reposición de electrolitos")
st.subheader("⬅ Usa la barra lateral para introducir datos y elegir el cálculo")

# ------------------------------
# Clase Paciente (datos básicos)
# ------------------------------
class Paciente:
    def __init__(self, ID, edad, genero, pesokg, tallacm):
        self.ID = ID
        self.edad = edad
        self.genero = genero        # 'H' o 'M'
        self.pesokg = pesokg
        self.tallacm = tallacm

        self.imc = None
        self.pesoideal = None
        self.pesoajustado = None

    def calcular_imc(self):
        if self.tallacm and self.pesokg:
            imc = self.pesokg / ((self.tallacm / 100) ** 2)
            self.imc = round(imc, 2)

    def calcular_pesos(self):
        if self.tallacm and self.pesokg:
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
                
# ------------------------------
# Barra lateral: datos del paciente
# ------------------------------
st.sidebar.header("Datos del paciente")

edad = st.sidebar.number_input("Edad (años)", min_value=0, max_value=110, step=1)

genero_opcion = st.sidebar.radio(
    "Género",
    options=["H - Hombre", "M - Mujer"]
)
genero = genero_opcion[0]  # 'H' o 'M'

pesokg = st.sidebar.number_input("Peso (kg)", min_value=0.0, max_value=250.0, step=0.1)
tallacm = st.sidebar.number_input("Talla (cm)", min_value=0.0, max_value=250.0, step=0.1)

# Creamos el objeto paciente
ID = f"PAC-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
paciente = Paciente(ID, edad, genero, pesokg, tallacm)
paciente.calcular_imc()
paciente.calcular_pesos()

st.sidebar.markdown("---")

# ------------------------------
# Elegir qué cálculo hacer
# ------------------------------
calculo = st.sidebar.selectbox(
    "¿Qué cálculo deseas realizar?",
    [
        "Necesidades de sueroterapia",
        "Necesidades de glucosa",
        "Ajuste del aporte de sodio",
        "Ajuste del aporte de potasio",
        "Reposición de sodio",
        "Reposición de potasio",
        "Reposición de calcio",
        "Reposición de magnesio",
        "Reposición de fosfato",
        "Reposición de bicarbonato (acidosis metabólica)",
    ]
)

# ------------------------------
# 1) Necesidades de sueroterapia
# ------------------------------
if calculo == "Necesidades de sueroterapia":
    st.sidebar.subheader("Opciones de sueroterapia")

    situacion = st.sidebar.radio(
        "Situación clínica",
        options=[
            "Sin fiebre ni taquipnea",
            "Con fiebre",
            "Taquipneico"
        ]
    )

    boton_sueros = st.sidebar.button("Calcular sueroterapia")

    if boton_sueros:
        if pesokg <= 0:
            st.error("Introduce primero un peso válido.")
        else:
            # Intervalo de volumen horario (mL/día)
            vol_dia_min = 25 * pesokg
            vol_dia_max = 30 * pesokg

            # Ajuste por situación clínica
            if situacion == "Con fiebre":
                factor = 1.12
            elif situacion == "Taquipneico":
                factor = 1.5
            else:
                factor = 1.0

            vol_total_min_aj = vol_dia_min * factor
            vol_total_max_aj = vol_dia_max * factor
            
            # velocidad hora (mL/h) 
            vel_hora_min = vol_dia_min / 24
            vel_hora_max = vol_dia_max / 24


            st.subheader("Necesidades de sueroterapia")
            st.write(f"Peso del paciente: **{pesokg} kg**")
            st.write(f"Situación clínica: **{situacion}**")
            st.markdown("---")

            st.write(
                f"Volumen recomendado: **{int(vol_total_min_aj)}–{int(vol_total_max_aj)} mL/día**"
            )
            st.write(
                f"Velocidad de perfusión: **{vel_hora_min:.1f}–{vel_hora_max:.1f} mL/h**"
            )
            
# ------------------------------
# 2) Necesidades de glucosa
# ------------------------------
if calculo == "Necesidades de glucosa":
    st.sidebar.subheader("Aporte de glucosa")

    aporte_glu_kg = st.sidebar.number_input(
        "Aporte de glucosa deseado (g/kg/día)",
        min_value=0.0, max_value=15.0, value=2.0, step=0.5,
        help="Introduce el objetivo de glucosa en gramos por kg de peso y día."
    )

    tipo_suero = st.sidebar.selectbox(
        "Tipo de suero glucosado",
        [
            "Glucosalino 3.3%",
            "Glucosado 5%",
            "Glucosado 10%",
            "Glucosado 30%",
            "Glucosado 33%",
        ]
    )

    boton_glu = st.sidebar.button("Calcular sueroterapia glucosada")

    if boton_glu:
        if pesokg <= 0:
            st.error("Introduce primero un peso válido.")
        elif aporte_glu_kg <= 0:
            st.error("Introduce un aporte de glucosa mayor que 0.")
        else:
            # gramos totales de glucosa/día
            glu_total = pesokg * aporte_glu_kg  # g/día

            # concentración de cada suero en g/100 mL
            if tipo_suero == "Glucosalino 3.3%":
                conc_g_100ml = 3.3
            elif tipo_suero == "Glucosado 5%":
                conc_g_100ml = 5.0
            elif tipo_suero == "Glucosado 10%":
                conc_g_100ml = 10.0
            elif tipo_suero == "Glucosado 30%":
                conc_g_100ml = 30.0
            elif tipo_suero == "Glucosado 33%":
                conc_g_100ml = 33.0
            else:
                conc_g_100ml = 5.0  # por si acaso

            # Volumen de suero necesario (mL/día)
            vol_necesario_ml = (glu_total / conc_g_100ml) * 100.0
            vel_ml_h = vol_necesario_ml / 24.0

            st.subheader("Necesidades de glucosa")
            st.write(f"Peso del paciente: **{pesokg} kg**")
            st.write(f"Aporte deseado: **{aporte_glu_kg} g/kg/día**")
            st.write(f"Glucosa total objetivo: **{glu_total:.1f} g/día**")
            st.markdown("---")
            st.write(f"Tipo de suero elegido: **{tipo_suero}**")
            st.write(f"Concentración: **{conc_g_100ml} g / 100 mL**")
            st.markdown("---")
            st.write(f"Volumen de suero necesario: **{vol_necesario_ml:.0f} mL/día**")
            st.write(f"Velocidad aproximada: **{vel_ml_h:.1f} mL/h**")







