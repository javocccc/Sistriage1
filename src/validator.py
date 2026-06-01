"""
validator.py
Módulo M3 — Validación de parámetros de entrada
SisTriage · ERS v1.1

Responsabilidad: Verificar que los 8 parámetros fisiológicos estén presentes,
sean del tipo correcto y estén dentro del rango válido. (RF-01, RN-01, RN-02)

Requisitos: RF-01 · RN-01 · RN-02 · CA-4
"""

# Definición de rangos y tipos válidos según tabla RF-01
CAMPOS = {
    "fr":          {"tipo": int,   "min": 1,    "max": 60,   "unidad": "rpm"},
    "fc":          {"tipo": int,   "min": 20,   "max": 200,  "unidad": "bpm"},
    "pas":         {"tipo": int,   "min": 40,   "max": 250,  "unidad": "mmHg"},
    "temperatura": {"tipo": float, "min": 30.0, "max": 42.0, "unidad": "°C"},
    "avpu":        {"tipo": str,   "opciones": ["A", "V", "P", "U"]},
    "spo2":        {"tipo": int,   "min": 50,   "max": 100,  "unidad": "%"},
    "edad":        {"tipo": int,   "min": 0,    "max": 120,  "unidad": "años"},
    "eva":         {"tipo": int,   "min": 0,    "max": 10,   "unidad": "—"},
}


def validate_inputs(params: dict) -> dict:
    """
    Valida los 8 parámetros fisiológicos de entrada.

    Parámetros:
        params : dict con claves fr, fc, pas, temperatura, avpu, spo2, edad, eva

    Retorna:
        {
            "valido": bool,
            "errores": [{"campo": str, "mensaje": str}, ...]
        }
    """
    errores = []

    for campo, reglas in CAMPOS.items():
        valor = params.get(campo)

        # RN-01: Campo obligatorio
        if valor is None:
            errores.append({
                "campo": campo,
                "mensaje": f"Campo obligatorio. No puede estar vacío.",
            })
            continue

        # Validación de tipo
        tipo_esperado = reglas["tipo"]
        if not isinstance(valor, tipo_esperado):
            # Intentar conversión implícita para tolerancia (ej: 37 como float)
            try:
                valor = tipo_esperado(valor)
            except (ValueError, TypeError):
                errores.append({
                    "campo": campo,
                    "mensaje": f"Tipo de dato incorrecto. Se esperaba {tipo_esperado.__name__}.",
                })
                continue

        # Validación de rango (RN-02)
        if "opciones" in reglas:
            if str(valor).upper() not in reglas["opciones"]:
                errores.append({
                    "campo": campo,
                    "mensaje": f"Valor inválido. Opciones permitidas: {', '.join(reglas['opciones'])}.",
                })
        else:
            if not (reglas["min"] <= valor <= reglas["max"]):
                errores.append({
                    "campo": campo,
                    "mensaje": (
                        f"Valor fuera de rango. "
                        f"Rango válido: {reglas['min']} – {reglas['max']} {reglas['unidad']}."
                    ),
                })

    return {
        "valido": len(errores) == 0,
        "errores": errores,
    }
