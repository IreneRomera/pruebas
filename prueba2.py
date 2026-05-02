#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 17:57:35 2026

@author: Prunebelly
"""

import streamlit as st
from datetime import datetime
from streamlit_extras.buy_me_a_coffee import button

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
        "Necesidades de sodio",
        "Necesidades de potasio",
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


# ------------------------------
# 3) Necesidades de sodio
# ------------------------------
if calculo == "Necesidades de sodio":
    st.sidebar.subheader("Aporte de sodio en 24 h")

    suero_tipo = st.sidebar.selectbox(
        "Tipo de suero principal",
        [
            "NaCl 0.9%",
            "Glucosalino 0.33%",
            "NaCl 0.45%",
            "Ringer lactato",
            "Plasmalyte",
            "No recibe suero"
        ]
    )

    suero_vol = st.sidebar.number_input(
        "Volumen de suero en 24 h (mL)",
        min_value=0.0, max_value=10000.0, value=0.0, step=50.0
    )

    nutri_vol = st.sidebar.number_input(
        "Volumen de nutrición artificial (NE/NPT) en 24 h (mL)",
        min_value=0.0, max_value=10000.0, value=0.0, step=50.0
    )

    nutri_tipo = st.sidebar.number_input(
        "Concentración de sodio de la nutrición (mmol/100 mL)",
        min_value=0.0, max_value=100.0, value=0.0, step=1.0
    )

    extra_na = st.sidebar.number_input(
        "Aporte extra de sodio (mmol/24 h)",
        min_value=0.0, max_value=1000.0, value=0.0, step=5.0
    )

    boton_na = st.sidebar.button("Calcular balance de sodio")

    if boton_na:
        if pesokg <= 0:
            st.error("Introduce primero un peso válido.")
        else:
            # mmol de sodio según tipo de suero (por litro)
            if suero_tipo == "NaCl 0.9%":
                na_suero_mmol_l = 154.0
            elif suero_tipo == "Glucosalino 0.33%":
                na_suero_mmol_l = 51.0
            elif suero_tipo == "NaCl 0.45%":
                na_suero_mmol_l = 77.0
            elif suero_tipo == "Ringer lactato":
                na_suero_mmol_l = 130.0
            elif suero_tipo == "Plasmalyte":
                na_suero_mmol_l = 140.0
            else:  # No recibe suero
                na_suero_mmol_l = 0.0

            aporte_suero = na_suero_mmol_l * (suero_vol / 1000.0)
            aporte_nutricion = nutri_vol * (nutri_tipo / 100.0)
            aporte_total = aporte_suero + aporte_nutricion + extra_na

            requerimiento_est = pesokg  # aprox. mmol/24h ~ peso

            st.subheader("Ajuste del aporte de sodio")
            st.write(f"Peso del paciente: **{pesokg} kg**")
            st.markdown("---")
            st.write(f"Aporte desde suero: **{aporte_suero:.1f} mmol/24h**")
            st.write(f"Aporte desde nutrición: **{aporte_nutricion:.1f} mmol/24h**")
            st.write(f"Aporte extra: **{extra_na:.1f} mmol/24h**")
            st.markdown("---")
            st.write(f"Aporte total estimado: **{aporte_total:.1f} mmol/24h**")
            st.write(f"Requerimiento estimado (≈peso): **{requerimiento_est:.1f} mmol/24h**")
            st.markdown("---")

            balance = aporte_total - requerimiento_est
            if balance > 0:
                st.warning(f"Balance positivo de sodio: **+{balance:.1f} mmol/24h** (posible exceso).")
            elif balance < 0:
                st.info(f"Balance negativo de sodio: **{balance:.1f} mmol/24h** (posible déficit).")
            else:
                st.success("El aporte de sodio está muy próximo al requerimiento estimado.")
                
                
# ------------------------------
# 4) Necesidades de potasio
# ------------------------------
if calculo == "Necesidades de potasio":
    st.sidebar.subheader("Requerimiento ajustado de potasio")

    diuresis_ml = st.sidebar.number_input(
        "Diuresis en 24 h (mL)",
        min_value=0.0, max_value=10000.0, value=0.0, step=50.0
    )

    kcal_dia = st.sidebar.number_input(
        "Aporte calórico actual (kcal/día)",
        min_value=0.0, max_value=6000.0, value=0.0, step=50.0
    )

    boton_k = st.sidebar.button("Calcular requerimiento de potasio")

    if boton_k:
        if pesokg <= 0:
            st.error("Introduce primero un peso válido.")
        else:
            # Tu fórmula original:
            # diu = 30*(g/1000)
            # potasi = diu + (kcd/100)
            perdidas_urinarias = 30 * (diuresis_ml / 1000.0)    # mmol por diuresis
            aporte_por_kcal = kcal_dia / 100.0                  # mmol por aporte calórico

            requerimiento_k = perdidas_urinarias + aporte_por_kcal

            st.subheader("Ajuste del aporte de potasio")
            st.write(f"Diuresis: **{diuresis_ml:.0f} mL/24h**")
            st.write(f"Aporte calórico: **{kcal_dia:.0f} kcal/día**")
            st.markdown("---")
            st.write(f"Pérdidas urinarias estimadas: **{perdidas_urinarias:.1f} mEq/24h**")
            st.write(f"Requerimiento por aporte calórico: **{aporte_por_kcal:.1f} mEq/24h**")
            st.markdown("---")
            st.write(f"Requerimiento ajustado de potasio: **{requerimiento_k:.1f} mEq/24h**")

# ------------------------------
# 5) Reposición de sodio
# ------------------------------
if calculo == "Reposición de sodio":
    st.sidebar.subheader("Reposición de sodio")

    natremia_actual = st.sidebar.number_input(
        "Natremia actual (mEq/L)",
        min_value=90.0, max_value=170.0, value=125.0, step=0.5
    )

    natremia_objetivo = st.sidebar.number_input(
        "Natremia objetivo (mEq/L)",
        min_value=90.0, max_value=170.0, value=135.0, step=0.5
    )

    tiempo_horas = st.sidebar.number_input(
        "Tiempo deseado para la corrección (horas)",
        min_value=1.0, max_value=96.0, value=36.0, step=1.0
    )

    solucion_na = st.sidebar.selectbox(
        "Solución de Na+ para la reposición",
        [
            "NaCl 0.9%",
            "NaCl 3%",
            "NaCl 5%",
            "Ringer lactato"
        ]
    )

    boton_hipo = st.sidebar.button("Calcular reposición de sodio")

    if boton_hipo:
        if pesokg <= 0:
            st.error("Introduce primero un peso válido.")
        else:
            # --- 1. Agua corporal total (ACT) según TUS FÓRMULAS ---
            if edad < 16:
                act = 0.6 * pesokg
            else:
                if genero == "H":
                    act = 2.447 - (0.09516 * edad) + (0.1074 * tallacm) + (0.3362 * pesokg)
                else:  # genero == "M"
                    act = -2.097 + (0.1069 * tallacm) + (0.2466 * pesokg)
                    
                    
            # --- 2. Déficit de sodio total (mEq) ---
            delta_na = natremia_objetivo - natremia_actual  # mEq/L
            deficit_na = act * delta_na                     # mEq totales

            # --- 3. Ritmo de corrección previsto ---
            ritmo_na_dia = (delta_na / tiempo_horas) * 24.0  # mEq/L/día

            # --- 4. Concentración de Na+ de cada solución (mEq/L) ---
            if solucion_na == "NaCl 0.9%":
                conc_na = 154.0
            elif solucion_na == "NaCl 3%":
                conc_na = 513.0
            elif solucion_na == "NaCl 5%":
                conc_na = 855.0
            elif solucion_na == "Ringer lactato":
                conc_na = 130.0
            else:
                conc_na = 154.0

            # --- 5. Volumen/velocidad aproximada ---
            # Déficit a repartir en 'tiempo_horas'
            # mEq/h que queremos aportar:
            mEq_por_hora = deficit_na / tiempo_horas

            # Volumen de solución necesario por hora (mL/h):
            # mEq/h / (mEq/L) = L/h  -> *1000 = mL/h
            vel_ml_h = (mEq_por_hora / conc_na) * 1000.0

            st.subheader("Reposición de sodio")
            st.write(f"Peso del paciente: **{pesokg} kg**")
            st.write(f"ACT estimada: **{act:.1f} L**")
            st.markdown("---")
            st.write(f"Natremia actual: **{natremia_actual:.1f} mEq/L**")
            st.write(f"Natremia objetivo: **{natremia_objetivo:.1f} mEq/L**")
            st.write(f"Diferencia a corregir: **{delta_na:.1f} mEq/L**")
            st.markdown("---")
            st.write(f"Déficit total de sodio estimado: **{deficit_na:.1f} mEq**")
            st.write(f"Tiempo de corrección: **{tiempo_horas:.0f} h**")
            st.write(f"Ritmo aproximado de corrección: **{ritmo_na_dia:.1f} mEq/L/día**")
            if ritmo_na_dia > 12:
                st.error("Ritmo de corrección > 12 mEq/L/día: MUY elevado, alto riesgo de mielinólisis.")
            elif ritmo_na_dia > 8:
                st.warning("Ritmo de corrección 8–12 mEq/L/día: elevado, valora prolongar el tiempo de corrección.")
            else:
                st.info("Ritmo de corrección dentro de rangos habitualmente recomendados (< 8 mEq/L/día).")

            st.markdown("---")
            st.write(f"Solución elegida: **{solucion_na}** (≈{conc_na} mEq/L de Na+)")
            st.write(f"Velocidad aproximada de reposición: **{vel_ml_h:.1f} mL/h**")

            st.caption(
                "Nota: cálculo orientativo. Ajustar siempre según natremias seriadas, "
                "situación clínica y recomendaciones de tu protocolo local."
            )

# ------------------------------
# 6) Reposición de potasio
# ------------------------------
if calculo == "Reposición de potasio":
    st.sidebar.subheader("Reposición de potasio")

    k_actual = st.sidebar.number_input(
        "Potasemia actual (mEq/L)",
        min_value=1.0, max_value=7.0, value=3.0, step=0.1
    )

    k_objetivo = st.sidebar.number_input(
        "Potasemia objetivo (mEq/L)",
        min_value=1.0, max_value=7.0, value=4.0, step=0.1
    )

    sintomas_k = st.sidebar.radio(
        "¿Tiene síntomas de hipopotasemia?",
        options=["No", "Sí"]
    )

    boton_k_repo = st.sidebar.button("Calcular reposición de potasio")

    if boton_k_repo:
        if pesokg <= 0 or tallacm <= 0:
            st.error("Introduce primero un peso y una talla válidos.")
        else:
            # Aseguramos que tenemos peso ideal calculado
            paciente.calcular_pesos()
            if paciente.pesoideal is None:
                st.error("No se pudo calcular el peso ideal; revisa los datos de talla y género.")
            else:
                dif_k = k_objetivo - k_actual          # mEq/L
                deficit_k = dif_k * paciente.pesoideal * 0.5 # mEq totales aproximados con factor corrección

                st.subheader("Reposición de potasio")
                st.write(f"Potasemia actual: **{k_actual:.1f} mEq/L**")
                st.write(f"Potasemia objetivo: **{k_objetivo:.1f} mEq/L**")
                st.write(f"Diferencia a corregir: **{dif_k:.1f} mEq/L**")
                st.markdown("---")
                st.write(f"Déficit estimado de potasio: **{deficit_k:.1f} mEq**")

                st.markdown("---")
                if deficit_k <= 0:
                    st.info("No se estima déficit positivo de potasio con estos valores.")
                else:
                    if sintomas_k == "Sí":
                        st.warning(
                            "Paciente sintomático: considerar reposición IV más rápida "
                            "según protocolo local."
                        )
                    else:
                        st.info(
                            "Paciente asintomático: considerar reposición fraccionada "
                            "en varias dosis según protocolo local."
                        )

                st.caption(
                    "Cálculo orientativo usando déficit = (K objetivo − K actual) × peso ideal. "
                    "Ajustar siempre según EKG, función renal y guías locales."
                )


# ------------------------------
# 7) Reposición de calcio (hipocalcemia)
# ------------------------------
if calculo == "Reposición de calcio":
    st.sidebar.subheader("Reposición de calcio")

    modo_calcio = st.sidebar.radio(
        "¿Cómo quieres valorar la hipocalcemia?",
        options=[
            "Según calcio iónico",
            "Según calcio corregido por albúmina"
        ]
    )

    if modo_calcio == "Según calcio iónico":
        cal_ionico = st.sidebar.number_input(
            "Calcio iónico (mmol/L)",
            min_value=0.2, max_value=1.6, value=1.05, step=0.01
        )

        boton_calcio = st.sidebar.button("Calcular reposición según calcio iónico")

        if boton_calcio:
            st.subheader("Reposición de calcio según calcio iónico")

            st.write(f"Calcio iónico: **{cal_ionico:.2f} mmol/L**")

            if 1.00 <= cal_ionico <= 1.12:
                st.warning(
                    "Hipocalcemia leve/moderada.\n\n"
                    "Se recomienda reposición con **2 g de gluconato cálcico 10% (bolo IV)** "
                    "a administrar en aproximadamente **2 horas**."
                )
            elif cal_ionico < 1.00:
                st.error(
                    "Hipocalcemia moderada-severa.\n\n"
                    "Se recomienda reposición con **4 g de gluconato cálcico 10% (bolo IV)** "
                    "a administrar en aproximadamente **4 horas**."
                )
            else:
                st.info("El calcio iónico no está bajo según los rangos indicados.")

            st.caption(
                "Esquema basado en tu protocolo: ajustar siempre a la situación clínica, "
                "ECG y función renal, siguiendo las guías locales."
            )

    else:  # Según calcio corregido por albúmina
        cal_corregido = st.sidebar.number_input(
            "Calcio corregido por albúmina (mmol/L)",
            min_value=0.5, max_value=3.0, value=2.2, step=0.1
        )

        sintomas = st.sidebar.radio(
            "¿Tiene síntomas de hipocalcemia?",
            options=["No", "Sí"]
        )

        boton_calcio2 = st.sidebar.button("Calcular reposición según calcio corregido")

        if boton_calcio2:
            st.subheader("Reposición de calcio según calcio corregido")

            st.write(f"Calcio corregido: **{cal_corregido:.2f} mmol/L**")
            st.write(f"Síntomas de hipocalcemia: **{sintomas}**")
            st.markdown("---")

            if cal_corregido <= 2.2 and cal_corregido >= 1.9 and sintomas == "No":
                st.info(
                    "Hipocalcemia leve, paciente asintomático.\n\n"
                    "Se recomienda tratamiento con **carbonato cálcico oral +/- vitamina D** "
                    "según tolerancia y protocolo local."
                )
            elif cal_corregido < 1.9 or sintomas == "Sí":
                st.error(
                    "Hipocalcemia significativa o paciente sintomático.\n\n"
                    "Se recomienda:\n"
                    "- **Gluconato cálcico 10% IV** 10–20 mL en 100 mL de SG 5% durante 10 minutos (bolo).\n"
                    "- seguido de **Gluconato cálcico 10%** (100 mL = 10 ampollas) en 1 L de NaCl 0.9% "
                    "o SG 5% a **50–100 mL/h**."
                )
            else:
                st.info("El calcio corregido no está bajo según los rangos indicados.")

            st.caption(
                "Esquema basado en tu algoritmo original. Valorar siempre clínica, ECG "
                "y riesgo de extravasación, y seguir las recomendaciones de tu unidad."
            )
            
            
# ------------------------------
# 8) Reposición de magnesio (hipomagnesemia)
# ------------------------------
if calculo == "Reposición de magnesio":
    st.sidebar.subheader("Reposición de magnesio")

    mg_actual = st.sidebar.number_input(
        "Magnesemia actual (mg/dL)",
        min_value=0.2, max_value=3.0, value=1.3, step=0.01
    )

    boton_mg = st.sidebar.button("Calcular reposición de magnesio")

    if boton_mg:
        if pesokg <= 0:
            st.error("Introduce primero un peso válido.")
        else:
            # Parámetros de tu algoritmo original
            necemag1 = pesokg          # mmol (aprox) para día 1
            necemag2 = 0.5 * pesokg    # mmol (aprox) para día 2

            gmagdia1 = necemag1 / 8    # g de MgSO4 (1 g = 8 mEq)
            gmagdia2 = necemag2 / 8

            l = necemag1 / 4           # mEq cada 6h día 1
            m = necemag2 / 4           # mEq cada 6h día 2
            n = gmagdia1 / 4           # g cada 6h día 1
            o = gmagdia2 / 4           # g cada 6h día 2

            st.subheader("Reposición de magnesio (hipomagnesemia)")
            st.write(f"Magnesemia actual: **{mg_actual:.2f} mg/dL**")
            st.write(f"Peso del paciente: **{pesokg:.1f} kg**")
            st.markdown("---")

            if 1.4 <= mg_actual <= 1.7:
                # Hipomagnesemia leve
                st.info(
                    "Hipomagnesemia leve.\n\n"
                    "Se recomienda reposición con **1–2 dosis IV de 1–2 g** "
                    "de sulfato de magnesio (8–16 mEq) o, si es posible, "
                    "reposiciones orales (por ejemplo, óxido de magnesio 400 mg 1–2 comp/día)."
                )

            elif 1.2 <= mg_actual < 1.4:
                # Moderada
                st.warning(
                    "Hipomagnesemia moderada.\n\n"
                    "Se recomienda reposición **vía endovenosa de 1–2 g (8–16 mEq)** "
                    "de sulfato de magnesio **cada 4 horas**, evitando la vía oral."
                )

            elif mg_actual < 1.2:
                # Severa: usamos tus fórmulas peso‑dependientes
                st.error(
                    "Hipomagnesemia severa.\n\n"
                    f"**Día 1:**\n"
                    f"- Reposición IV con aproximadamente **{n:.1f} g** de sulfato de magnesio "
                    f"cada 6 h (≈ **{l:.1f} mEq** cada 6 h).\n\n"
                    f"**Día 2:**\n"
                    f"- Reposición IV con aproximadamente **{o:.1f} g** de sulfato de magnesio "
                    f"cada 6 h (≈ **{m:.1f} mEq** cada 6 h).\n\n"
                    "No se recomienda reposición oral en este contexto."
                )
            else:
                st.success("La magnesemia no se encuentra en rango de hipomagnesemia con este umbral.")

            st.caption(
                "Esquema basado en tu algoritmo original (1 g MgSO₄ ≈ 8 mEq). "
                "Ajustar siempre a función renal, diuresis y protocolos locales."
            )

# ------------------------------
# 9) Reposición de fosfato (hipofosfatemia)
# ------------------------------
if calculo == "Reposición de fosfato":
    st.sidebar.subheader("Reposición de fosfato")

    sintomas_fosf = st.sidebar.radio(
        "¿Tiene síntomas de hipofosfatemia?",
        options=["No", "Sí"]
    )

    fosfato_serico = st.sidebar.number_input(
        "Fosfato sérico (mg/dL)",
        min_value=0.1, max_value=10.0, value=2.0, step=0.1
    )

    boton_fosf = st.sidebar.button("Calcular reposición de fosfato")

    if boton_fosf:
        if pesokg <= 0:
            st.error("Introduce primero un peso válido.")
        else:
            # Aseguramos IMC y pesos
            paciente.calcular_imc()
            paciente.calcular_pesos()

            if paciente.imc is None:
                st.error("No se pudo calcular el IMC; revisa talla/peso.")
            else:
                st.subheader("Reposición de fosfato (hipofosfatemia)")
                st.write(f"IMC: **{paciente.imc:.1f} kg/m²**")
                st.write(f"Fosfato sérico: **{fosfato_serico:.2f} mg/dL**")
                st.write(f"Síntomas: **{sintomas_fosf}**")
                st.markdown("---")

                # Cálculos según tu algoritmo
                if paciente.imc < 30:
                    # Peso normal: usamos peso real
                    base = pesokg
                else:
                    # Obeso: usamos peso ajustado
                    if paciente.pesoajustado is None:
                        st.error("No se pudo calcular el peso ajustado.")
                        base = pesokg
                    else:
                        base = paciente.pesoajustado

                # Rangos de reposición basados en tu código:
                # i1=0.08*b; i2=0.16*b; i3=0.32*b; s3=0.64*b
                r1_min = 0.08 * base
                r1_max = 0.16 * base
                r2_min = 0.16 * base
                r2_max = 0.32 * base
                r3_min = 0.32 * base
                r3_max = 0.64 * base

                mensaje = ""

                if sintomas_fosf == "Sí":
                    # Sintomático: ir directamente a rango más alto
                    mensaje = f"Se recomienda reposición con **{r3_min:.1f}–{r3_max:.1f} mmol** de fosfato."
                else:
                    # Asintomático: según fosfato sérico
                    if fosfato_serico <= 2.7 and fosfato_serico >= 2.3:
                        mensaje = f"Se recomienda reposición con **{r1_min:.1f}–{r1_max:.1f} mmol** de fosfato."
                    elif 1.5 <= fosfato_serico < 2.3:
                        mensaje = f"Se recomienda reposición con **{r2_min:.1f}–{r2_max:.1f} mmol** de fosfato."
                    elif fosfato_serico < 1.5:
                        mensaje = f"Se recomienda reposición con **{r3_min:.1f}–{r3_max:.1f} mmol** de fosfato."
                    else:
                        mensaje = "El fosfato sérico no está en rango de hipofosfatemia según este esquema."

                if "mmol" in mensaje:
                    if paciente.imc < 30:
                        st.info("Paciente con IMC < 30: se usa el peso real para el cálculo.")
                    else:
                        st.info("Paciente con IMC ≥ 30: se usa el peso ajustado para el cálculo.")

                    st.warning(mensaje)
                else:
                    st.success(mensaje)

                st.caption(
                    "Esquema basado en tu algoritmo original. Ajustar siempre según función renal, "
                    "riesgo de precipitación de sales de calcio y protocolo local."
                )


# ------------------------------
# 10) Reposición de bicarbonato (acidosis metabólica)
# ------------------------------
if calculo == "Reposición de bicarbonato (acidosis metabólica)":
    st.sidebar.subheader("Reposición de bicarbonato")

    bic_actual = st.sidebar.number_input(
        "Bicarbonato sérico actual (mmol/L)",
        min_value=0.0, max_value=40.0, value=16.0, step=0.5
    )

    sodio_serico = st.sidebar.number_input(
        "Sodio sérico (mmol/L o mEq/L)",
        min_value=100.0, max_value=180.0, value=140.0, step=1.0
    )

    cloro_serico = st.sidebar.number_input(
        "Cloro sérico (mmol/L o mEq/L)",
        min_value=70.0, max_value=140.0, value=100.0, step=1.0
    )

    boton_bic = st.sidebar.button("Calcular reposición de bicarbonato")

    if boton_bic:
        if pesokg <= 0:
            st.error("Introduce primero un peso válido.")
        else:
            st.subheader("Reposición de bicarbonato (acidosis metabólica)")
            st.write(f"Peso del paciente: **{pesokg:.1f} kg**")
            st.write(f"Bicarbonato actual: **{bic_actual:.1f} mmol/L**")
            st.markdown("---")

            # 1) Déficit de bicarbonato
            # Tu fórmula: deficitbic = 0.4 * peso * (24 - HCO3)
            deficit_bic = 0.4 * pesokg * (24.0 - bic_actual)

            if deficit_bic <= 0:
                st.success("No se estima déficit de bicarbonato con estos valores (HCO₃⁻ ≥ 24).")
            else:
                st.write(f"Déficit estimado de bicarbonato: **{deficit_bic:.1f} mmol**")
                dosis_1h = deficit_bic / 2.0
                dosis_restante = deficit_bic - dosis_1h

                st.markdown("---")
                st.info(
                    f"Recomendación (según tu esquema):\n\n"
                    f"- Reponer aproximadamente **{dosis_1h:.1f} mmol** en **1 hora**.\n"
                    f"- Reponer los **{dosis_restante:.1f} mmol** restantes en las siguientes **4–6 horas**.\n"
                )

            # 2) Anión gap y delta gap
            anion_gap = sodio_serico - (cloro_serico + bic_actual)
            delta_gap = (anion_gap - 12.0) / (24.0 - bic_actual) if (24.0 - bic_actual) != 0 else None

            st.markdown("---")
            st.write(f"Anión gap: **{anion_gap:.1f} mEq/L**")

            if delta_gap is not None:
                st.write(f"Delta gap: **{delta_gap:.2f}**")
            else:
                st.write("Delta gap no calculable (24 − HCO₃⁻ = 0).")

            st.caption(
                "Déficit de bicarbonato calculado como 0.4 × peso × (24 − HCO₃⁻), siguiendo tu algoritmo. "
                "Interpretar anión gap y delta gap junto con la clínica y gases arteriales. Un delta gap alto (>2) sugiere alcalosis metabólica concomitante o acidosis respiratoria crónica, y un delta gap bajo (<1) sugiere además una acidosis metabólica hiperclorémica."
            )

st.markdown("---")
st.caption("App desarrollada por Irene Romera / irene.r.s@outlook.com 😊")
st.write("Si esta calculadora te resulta útil …")

button(
    username="ireneromera",      # tu usuario de buymeacoffee.com
    floating=False,                  # que no flote, aparece en el flujo normal
    text="Invítame a un té",
    emoji="🫖",
    bg_color="#C084FC",
    font_color="#FFFFFF"
)








