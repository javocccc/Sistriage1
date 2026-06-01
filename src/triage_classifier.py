"""
triage_classifier.py
Módulo M2 — Clasificación y modificadores automáticos
SisTriage · ERS v1.1

Responsabilidad: Recibir el score MEWS y los parámetros crudos, aplicar modificadores
de nivel mínimo (RN-03, RN-04) y override clínico (RF-09), retornar nivel de prioridad final.

Requisitos: RF-03 · RF-04 · RF-09 · RN-03 · RN-04 · CA-2 · CA-3
"""

# Jerarquía de niveles para comparaciones
NIVEL_ORDEN = {"Verde": 1, "Amarillo": 2, "Naranja": 3, "Rojo": 4}
NIVEL_TIEMPO = {
    "Verde":    "Puede esperar (> 2 h)",
    "Amarillo": "Atender en < 30 min",
    "Naranja":  "Atender en < 10 min",
    "Rojo":     "Atención inmediata",
}


def _nivel_por_score(score: int) -> str:
    """Determina el nivel de prioridad según score MEWS. (RF-03)"""
    if score <= 1:
        return "Verde"
    elif score <= 3:
        return "Amarillo"
    elif score <= 5:
        return "Naranja"
    else:
        return "Rojo"


def apply_modifiers(nivel_base: str, avpu: str, spo2: int) -> tuple[str, str | None]:
    """
    Aplica modificadores de nivel mínimo. (RF-04, RN-03, RN-04)

    Retorna:
        (nivel_final, descripcion_modificador | None)
    """
    nivel = nivel_base
    modificador = None

    # RN-03: AVPU=U → nivel mínimo Naranja
    if avpu.upper() == "U" and NIVEL_ORDEN[nivel] < NIVEL_ORDEN["Naranja"]:
        nivel = "Naranja"
        modificador = "AVPU=Inconsciente → nivel mínimo Naranja"

    # RN-04: SpO₂ < 85% → nivel mínimo Rojo (puede sobreescribir el anterior)
    if spo2 < 85 and NIVEL_ORDEN[nivel] < NIVEL_ORDEN["Rojo"]:
        nivel = "Rojo"
        modificador = "SpO₂ < 85% → nivel mínimo Rojo"

    return nivel, modificador


def apply_clinical_override(nivel_calculado: str, override_nivel: str,
                             override_justificacion: str | None) -> dict:
    """
    Aplica priorización clínica manual (RF-09).

    Reglas:
    - Solo se puede asignar un nivel igual o superior al calculado.
    - La justificación es obligatoria (mínimo 20 caracteres).

    Retorna:
        dict con 'exito', 'nivel', 'mensaje_error'
    """
    if not override_justificacion or len(override_justificacion.strip()) < 20:
        return {
            "exito": False,
            "nivel": nivel_calculado,
            "mensaje_error": "La justificación clínica es obligatoria y debe tener al menos 20 caracteres.",
        }

    if NIVEL_ORDEN.get(override_nivel, 0) < NIVEL_ORDEN.get(nivel_calculado, 0):
        return {
            "exito": False,
            "nivel": nivel_calculado,
            "mensaje_error": f"El override no puede asignar un nivel inferior al calculado ({nivel_calculado}).",
        }

    return {
        "exito": True,
        "nivel": override_nivel,
        "mensaje_error": None,
    }


def classify(score_total: int, avpu: str, spo2: int,
             override_nivel: str | None = None,
             override_justificacion: str | None = None) -> dict:
    """
    Clasifica al paciente y aplica todos los modificadores.

    Parámetros:
        score_total           : Score MEWS calculado por M1
        avpu                  : Nivel de conciencia (A/V/P/U)
        spo2                  : Saturación O₂ (%)
        override_nivel        : Nivel manual del médico (RF-09), o None
        override_justificacion: Justificación obligatoria del override, o None

    Retorna:
        dict con nivel, tiempo_espera, modificador_aplicado, es_override.
    """
    nivel_base = _nivel_por_score(score_total)
    nivel, modificador = apply_modifiers(nivel_base, avpu, spo2)
    es_override = False

    if override_nivel is not None:
        resultado_override = apply_clinical_override(nivel, override_nivel, override_justificacion)
        if resultado_override["exito"]:
            nivel = resultado_override["nivel"]
            es_override = True
            modificador = f"Override clínico → {nivel} (justificación registrada)"
        else:
            return {
                "nivel": nivel,
                "tiempo_espera": NIVEL_TIEMPO[nivel],
                "modificador_aplicado": modificador,
                "es_override": False,
                "error": resultado_override["mensaje_error"],
            }

    return {
        "nivel":               nivel,
        "tiempo_espera":       NIVEL_TIEMPO[nivel],
        "modificador_aplicado": modificador,
        "es_override":         es_override,
        "error":               None,
    }
