"""
main.py
SisTriage — Demo CLI interactiva
Sistema Web de Triaje de Urgencias Hospitalarias

Ejecutar: python main.py
No requiere dependencias externas (solo Python 3.10+)
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from mews_calculator import calculate_mews
from triage_classifier import classify
from validator import validate_inputs

# ── Colores ANSI ──────────────────────────────────────────────────────────────
RESET  = "\033[0m"
BOLD   = "\033[1m"
RED    = "\033[91m"
ORANGE = "\033[93m"   # amarillo brillante simula naranja en terminal
YELLOW = "\033[33m"
GREEN  = "\033[92m"
CYAN   = "\033[96m"
GRAY   = "\033[90m"
WHITE  = "\033[97m"

NIVEL_COLOR = {
    "Verde":    GREEN,
    "Amarillo": YELLOW,
    "Naranja":  ORANGE,
    "Rojo":     RED,
}

NIVEL_EMOJI = {
    "Verde":    "🟢",
    "Amarillo": "🟡",
    "Naranja":  "🟠",
    "Rojo":     "🔴",
}

# ── Dataset de prueba rápida ──────────────────────────────────────────────────
DATASET_DEMO = [
    {"nombre": "Paciente A (normal)",        "fr": 14, "fc": 80,  "pas": 120, "temperatura": 37.0, "avpu": "A", "spo2": 98, "edad": 35, "eva": 1},
    {"nombre": "Paciente B (muy urgente)",   "fr": 22, "fc": 105, "pas": 95,  "temperatura": 38.0, "avpu": "A", "spo2": 92, "edad": 68, "eva": 5},
    {"nombre": "Paciente C (anciano +1)",    "fr": 18, "fc": 90,  "pas": 130, "temperatura": 37.2, "avpu": "A", "spo2": 96, "edad": 82, "eva": 2},
    {"nombre": "Paciente D (crítico)",       "fr": 32, "fc": 135, "pas": 68,  "temperatura": 39.0, "avpu": "V", "spo2": 88, "edad": 45, "eva": 8},
    {"nombre": "Paciente E (AVPU=U→Naranja)","fr": 14, "fc": 80,  "pas": 120, "temperatura": 37.0, "avpu": "U", "spo2": 96, "edad": 40, "eva": 0},
    {"nombre": "Paciente F (SpO₂<85%→Rojo)","fr": 14, "fc": 80,  "pas": 120, "temperatura": 37.0, "avpu": "A", "spo2": 80, "edad": 30, "eva": 3},
]


def linea(char="─", n=60):
    print(GRAY + char * n + RESET)


def banner():
    print()
    linea("═")
    print(f"{BOLD}{CYAN}  🏥  SisTriage — Sistema de Triaje de Urgencias{RESET}")
    print(f"{GRAY}      Algoritmo MEWS · Demo CLI v1.1{RESET}")
    linea("═")
    print()


def mostrar_resultado(nombre, params, resultado_m1, resultado_m2):
    nivel = resultado_m2["nivel"]
    color = NIVEL_COLOR[nivel]
    emoji = NIVEL_EMOJI[nivel]
    score = resultado_m1["score_total"]

    print(f"\n{BOLD}  Paciente:{RESET} {nombre}")
    linea()
    print(f"  {BOLD}Score MEWS:{RESET} {BOLD}{score}{RESET}  →  "
          f"{color}{BOLD}{emoji} {nivel.upper()}{RESET}  "
          f"{GRAY}({resultado_m2['tiempo_espera']}){RESET}")

    if resultado_m2["modificador_aplicado"]:
        print(f"  {ORANGE}⚠  Modificador: {resultado_m2['modificador_aplicado']}{RESET}")

    print(f"\n  {GRAY}Desglose por variable:{RESET}")
    campos = [
        ("FR",   resultado_m1["pts_fr"]),
        ("FC",   resultado_m1["pts_fc"]),
        ("PAS",  resultado_m1["pts_pas"]),
        ("T°",   resultado_m1["pts_temperatura"]),
        ("AVPU", resultado_m1["pts_avpu"]),
        ("SpO₂", resultado_m1["pts_spo2"]),
        ("Edad", resultado_m1["modificador_edad"]),
    ]
    for var, pts in campos:
        barra = "█" * pts if pts > 0 else "·"
        c = RED if pts >= 3 else (ORANGE if pts == 2 else (YELLOW if pts == 1 else GRAY))
        print(f"    {var:<6} {c}{barra:>3} pts{RESET}")
    linea()


def flujo_paciente(params: dict, nombre: str = "Ingresado"):
    """Valida, calcula y clasifica un paciente. Retorna True si exitoso."""
    # Validar
    validacion = validate_inputs(params)
    if not validacion["valido"]:
        print(f"\n  {RED}✗ Error de validación:{RESET}")
        for e in validacion["errores"]:
            print(f"    Campo {BOLD}{e['campo']}{RESET}: {e['mensaje']}")
        return False

    # Calcular
    resultado_m1 = calculate_mews(
        fr=int(params["fr"]),
        fc=int(params["fc"]),
        pas=int(params["pas"]),
        temperatura=float(params["temperatura"]),
        avpu=str(params["avpu"]),
        spo2=int(params["spo2"]),
        edad=int(params["edad"]),
    )

    # Clasificar
    resultado_m2 = classify(
        score_total=resultado_m1["score_total"],
        avpu=str(params["avpu"]),
        spo2=int(params["spo2"]),
    )

    mostrar_resultado(nombre, params, resultado_m1, resultado_m2)
    return True


def modo_demo():
    """Ejecuta el dataset de demostración completo."""
    print(f"\n{BOLD}  ► Modo Demo — Dataset de 6 pacientes{RESET}")
    print(f"  {GRAY}Ejecutando los 6 casos del dataset de prueba...{RESET}\n")
    for p in DATASET_DEMO:
        params = {k: v for k, v in p.items() if k != "nombre"}
        flujo_paciente(params, p["nombre"])
        input(f"  {GRAY}[Enter para continuar...]  {RESET}")


def modo_interactivo():
    """Permite ingresar un paciente manualmente."""
    print(f"\n{BOLD}  ► Modo Interactivo — Ingresar paciente{RESET}")
    print(f"  {GRAY}Ingrese los parámetros fisiológicos (Enter para cancelar):{RESET}\n")

    campos = [
        ("nombre",      "Nombre del paciente",        str,   None,  None),
        ("fr",          "Frecuencia Respiratoria (rpm) [1-60]", int,   1,    60),
        ("fc",          "Frecuencia Cardíaca (bpm) [20-200]",   int,   20,   200),
        ("pas",         "Presión Arterial Sistólica (mmHg) [40-250]", int, 40, 250),
        ("temperatura", "Temperatura (°C) [30.0-42.0]",  float, 30.0, 42.0),
        ("avpu",        "Nivel conciencia AVPU [A/V/P/U]", str,  None,  None),
        ("spo2",        "Saturación O₂ % [50-100]",    int,   50,   100),
        ("edad",        "Edad (años) [0-120]",          int,   0,    120),
        ("eva",         "Escala de dolor EVA [0-10]",   int,   0,    10),
    ]

    datos = {}
    for key, label, tipo, minv, maxv in campos:
        while True:
            try:
                raw = input(f"  {CYAN}{label}{RESET}: ").strip()
                if not raw:
                    print(f"  {GRAY}Cancelado.{RESET}")
                    return
                val = tipo(raw)
                if key == "avpu" and val.upper() not in ["A", "V", "P", "U"]:
                    print(f"  {RED}  Valor inválido. Use A, V, P o U.{RESET}")
                    continue
                if minv is not None and maxv is not None:
                    if not (minv <= val <= maxv):
                        print(f"  {RED}  Fuera de rango ({minv}–{maxv}).{RESET}")
                        continue
                datos[key] = val
                break
            except ValueError:
                print(f"  {RED}  Tipo incorrecto. Esperado: {tipo.__name__}.{RESET}")

    nombre = datos.pop("nombre")
    flujo_paciente(datos, nombre)


def modo_pruebas():
    """Ejecuta las pruebas unitarias via pytest."""
    print(f"\n{BOLD}  ► Ejecutando pruebas unitarias (pytest)...{RESET}\n")
    import subprocess
    result = subprocess.run(
        ["python", "-m", "pytest", "tests/", "-v", "--tb=short"],
        capture_output=False
    )
    if result.returncode == 0:
        print(f"\n  {GREEN}{BOLD}✓ Todas las pruebas pasaron.{RESET}")
    else:
        print(f"\n  {RED}{BOLD}✗ Algunas pruebas fallaron. Revisar output arriba.{RESET}")


def modo_validacion_error():
    """Demuestra validación con datos inválidos."""
    print(f"\n{BOLD}  ► Demo de Validación — Casos de Error{RESET}\n")

    casos = [
        ("CE-01 Campo vacío (PAS=None)",
         {"fr": 14, "fc": 80, "pas": None, "temperatura": 37.0,
          "avpu": "A", "spo2": 98, "edad": 35, "eva": 2}),
        ("CE-02 FC fuera de rango (FC=250)",
         {"fr": 14, "fc": 250, "pas": 120, "temperatura": 37.0,
          "avpu": "A", "spo2": 98, "edad": 35, "eva": 2}),
        ("CE-03 Múltiples errores (FC=250, T°=28.0, EVA=15)",
         {"fr": 14, "fc": 250, "pas": 120, "temperatura": 28.0,
          "avpu": "A", "spo2": 98, "edad": 35, "eva": 15}),
    ]

    for nombre, params in casos:
        print(f"  {BOLD}{nombre}{RESET}")
        flujo_paciente(params, nombre)
        print()


def menu_principal():
    banner()
    opciones = [
        ("1", "Demo automática  — 6 pacientes del dataset"),
        ("2", "Modo interactivo — ingresar paciente manualmente"),
        ("3", "Demo validación  — casos de error (CE-01, CE-02)"),
        ("4", "Pruebas unitarias— ejecutar pytest"),
        ("5", "Salir"),
    ]
    while True:
        print(f"\n{BOLD}  Menú principal:{RESET}")
        for key, desc in opciones:
            print(f"  {CYAN}[{key}]{RESET} {desc}")
        print()
        opcion = input(f"  {BOLD}Seleccione una opción:{RESET} ").strip()

        if opcion == "1":
            modo_demo()
        elif opcion == "2":
            modo_interactivo()
        elif opcion == "3":
            modo_validacion_error()
        elif opcion == "4":
            modo_pruebas()
        elif opcion == "5":
            print(f"\n  {GRAY}Hasta luego.{RESET}\n")
            sys.exit(0)
        else:
            print(f"  {RED}Opción inválida.{RESET}")


if __name__ == "__main__":
    # Si se pasa argumento --demo, corre sin interacción
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        banner()
        print(f"  {BOLD}► Ejecutando demo automática (modo no interactivo)...{RESET}\n")
        for p in DATASET_DEMO:
            params = {k: v for k, v in p.items() if k != "nombre"}
            flujo_paciente(params, p["nombre"])
        print(f"\n  {GREEN}{BOLD}✓ Demo completada. {len(DATASET_DEMO)} pacientes procesados.{RESET}\n")
    else:
        menu_principal()
