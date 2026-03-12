import math

def spline_potassium(x7):
    term1 = 0.08121 * max(x7 - 3.2, 0)**3
    term2 = -0.1421 * max(x7 - 4.1, 0)**3
    term3 = 0.06091 * max(x7 - 5.3, 0)**3
    return term1 + term2 + term3

def riesgo_af(x1, x2, x3, x4, x5, x6, x7, x8, x9, x10):
    a = -6.2252
    b1 = 0.0522
    b2 = 0.3076
    b3 = 0.3133
    b4 = 0.5901
    b5 = 0.4159
    b6 = -0.2674
    b8 = 0.8920
    b9 = 0.3967
    b10 = -0.3571

    linear_combination = (
        a + b1*x1 + b2*x2 + b3*x3 + b4*x4 + b5*x5 + b6*x6 +
        spline_potassium(x7) +
        b8*x8 + b9*x9 + b10*x10
    )

    P = math.exp(linear_combination) / (1 + math.exp(linear_combination))
    return P

print("Introduce los valores para calcular el riesgo de fibrilación auricular:")

x1 = float(input("Edad (años): "))
x2 = float(input("Obesidad - índice de masa corporal > 30 (1 = sí, 0 = no): "))
x3 = float(input("Estado inmunocomprometido (1 = sí, 0 = no): "))
x4 = float(input("Uso de vasopresores o inotrópicos (1 = sí, 0 = no): "))
x5 = float(input("Insuficiencia renal (1 = sí, 0 = no): "))
x6 = float(input("Potasio sérico (valor más alto de últimas 24h), mmol/L: "))
x7 = float(input("Potasio sérico' (para spline), mmol/L: "))
x8 = float(input("Fracción más alta de oxígeno inspirado (entre 0 y 1): "))

# Validación simple para inflamación
while True:
    try:
        x9 = int(input(
            "Inflamación (0 = baja, 1 = moderada, 2 = severa) "
            "\n(0 si PCR < 70 y Leucocitosis < 15; 1 si PCR 70-150 o leucocitosis 15-30; 2 si PCR ≥150 o leucocitosis ≥30): "))
        if x9 in (0, 1, 2):
            break
        else:
            print("Por favor ingresa 0, 1 o 2 para inflamación.")
    except ValueError:
        print("Entrada inválida. Debe ser un número entero 0, 1 o 2.")

x10 = float(input("Tiempo desde admisión a UCI, días: "))

probabilidad = riesgo_af(x1, x2, x3, x4, x5, x6, x7, x8, x9, x10)

print(f"\nEl riesgo estimado de desarrollar fibrilación auricular en 24 horas es {probabilidad:.2%}")
