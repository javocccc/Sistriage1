"""
mews_calculator.py
Módulo M1 — Cálculo del score MEWS
SisTriage · ERS v1.1

Responsabilidad: Calcular el score MEWS total a partir de los 6 parámetros fisiológicos
puntuados, aplicar el modificador por edad extrema, y retornar el desglose por variable.

Requisitos: RF-02 · RT-01 · RT-02 · CA-1
Error aceptable en el cálculo: 0
"""


def pts_fr(fr: int) -> int:
    """Puntos por Frecuencia Respiratoria (rpm)."""
    if fr < 9:
        return 2
    elif fr <= 14:
        return 0
    elif fr <= 20:
        return 1
    elif fr <= 29:
        return 2
    else:  # >= 30
        return 3


def pts_fc(fc: int) -> int:
    """Puntos por Frecuencia Cardíaca (bpm)."""
    if fc < 40:
        return 2
    elif fc <= 50:
        return 1
    elif fc <= 100:
        return 0
    elif fc <= 110:
        return 1
    elif fc <= 129:
        return 2
    else:  # >= 130
        return 3


def pts_pas(pas: int) -> int:
    """Puntos por Presión Arterial Sistólica (mmHg)."""
    if pas < 70:
        return 3
    elif pas <= 80:
        return 2
    elif pas <= 100:
        return 1
    elif pas <= 199:
        return 0
    else:  # >= 200
        return 2


def pts_temperatura(temp: float) -> int:
    """Puntos por Temperatura (°C)."""
    if temp < 35.0:
        return 2
    elif temp <= 38.4:
        return 0
    else:  # >= 38.5
        return 2


def pts_avpu(avpu: str) -> int:
    """Puntos por nivel de conciencia AVPU."""
    tabla = {"A": 0, "V": 1, "P": 2, "U": 3}
    return tabla.get(avpu.upper(), 0)


def pts_spo2(spo2: int) -> int:
    """Puntos por Saturación de O₂ (%)."""
    if spo2 >= 94:
        return 0
    elif spo2 >= 90:
        return 1
    elif spo2 >= 85:
        return 2
    else:  # < 85
        return 3


def modificador_edad(edad: int) -> int:
    """Modificador +1 si edad < 2 o edad >= 75. (RF-02)"""
    return 1 if (edad < 2 or edad >= 75) else 0


def calculate_mews(fr: int, fc: int, pas: int, temperatura: float,
                   avpu: str, spo2: int, edad: int) -> dict:
    """
    Calcula el score MEWS completo con desglose por variable.

    Parámetros:
        fr          : Frecuencia Respiratoria (rpm), rango válido 1-60
        fc          : Frecuencia Cardíaca (bpm), rango válido 20-200
        pas         : Presión Arterial Sistólica (mmHg), rango válido 40-250
        temperatura : Temperatura (°C), rango válido 30.0-42.0
        avpu        : Nivel de conciencia (A/V/P/U)
        spo2        : Saturación O₂ (%), rango válido 50-100
        edad        : Edad en años (0-120)

    Retorna:
        dict con score_total y desglose por variable.
    """
    p_fr   = pts_fr(fr)
    p_fc   = pts_fc(fc)
    p_pas  = pts_pas(pas)
    p_temp = pts_temperatura(temperatura)
    p_avpu = pts_avpu(avpu)
    p_spo2 = pts_spo2(spo2)
    p_edad = modificador_edad(edad)

    score = p_fr + p_fc + p_pas + p_temp + p_avpu + p_spo2 + p_edad

    return {
        "score_total":      score,
        "pts_fr":           p_fr,
        "pts_fc":           p_fc,
        "pts_pas":          p_pas,
        "pts_temperatura":  p_temp,
        "pts_avpu":         p_avpu,
        "pts_spo2":         p_spo2,
        "modificador_edad": p_edad,
    }
