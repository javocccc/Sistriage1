"""
test_validator.py
Pruebas unitarias — Módulo M3: validator
SisTriage · ERS v1.1

Cobertura: CP-01/CP-N2 (normales), CB-01/CB-02 (borde), CE-01/CE-02 (error),
           CRN-05b (múltiples campos inválidos)
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from validator import validate_inputs


PARAMS_VALIDOS = {
    "fr": 14, "fc": 80, "pas": 120, "temperatura": 37.0,
    "avpu": "A", "spo2": 98, "edad": 35, "eva": 2
}


# ─── CASOS NORMALES ───────────────────────────────────────────────────────────

def test_CP01_todos_validos():
    """CP-01: Parámetros completamente válidos → valido=True, sin errores"""
    r = validate_inputs(PARAMS_VALIDOS.copy())
    assert r["valido"] is True
    assert r["errores"] == []
    print("✓ CP-01 PASS: todos los parámetros válidos")


def test_CPN2_valores_extremos_validos():
    """CP-N2: Valores en extremos válidos del rango → aceptados"""
    params = {
        "fr": 1, "fc": 20, "pas": 40, "temperatura": 30.0,
        "avpu": "U", "spo2": 50, "edad": 0, "eva": 0
    }
    r = validate_inputs(params)
    assert r["valido"] is True
    print("✓ CP-N2 PASS: valores en extremo inferior del rango válidos")


# ─── CASOS DE BORDE ───────────────────────────────────────────────────────────

def test_CB01_FC_limite_superior_valido():
    """CB-01: FC = 200 (límite exacto superior válido) → aceptado"""
    params = {**PARAMS_VALIDOS, "fc": 200}
    r = validate_inputs(params)
    assert r["valido"] is True, f"FC=200 debe ser válido, errores: {r['errores']}"
    print("✓ CB-01 PASS: FC=200 en límite válido aceptado")


def test_CB02_FC_limite_fuera_de_rango():
    """CB-02: FC = 201 (justo fuera del rango) → rechazado con mensaje"""
    params = {**PARAMS_VALIDOS, "fc": 201}
    r = validate_inputs(params)
    assert r["valido"] is False
    campos_error = [e["campo"] for e in r["errores"]]
    assert "fc" in campos_error
    print("✓ CB-02 PASS: FC=201 fuera de rango rechazado")


# ─── CASOS DE ERROR ───────────────────────────────────────────────────────────

def test_CE01_campo_pas_vacio():
    """CE-01 / CL-08 / RN-01: PAS = None → campo obligatorio, no se calcula"""
    params = {**PARAMS_VALIDOS, "pas": None}
    r = validate_inputs(params)
    assert r["valido"] is False
    campos_error = [e["campo"] for e in r["errores"]]
    assert "pas" in campos_error
    # Verificar que el mensaje indica obligatoriedad
    msg = next(e["mensaje"] for e in r["errores"] if e["campo"] == "pas")
    assert "obligatorio" in msg.lower()
    print("✓ CE-01 PASS: PAS vacío → error obligatorio")


def test_CE02_FC_fuera_de_rango():
    """CE-02 / CP-07 / RN-02: FC = 250 → rechazado antes del cálculo"""
    params = {**PARAMS_VALIDOS, "fc": 250}
    r = validate_inputs(params)
    assert r["valido"] is False
    campos_error = [e["campo"] for e in r["errores"]]
    assert "fc" in campos_error
    msg = next(e["mensaje"] for e in r["errores"] if e["campo"] == "fc")
    assert "rango" in msg.lower()
    print("✓ CE-02 PASS: FC=250 fuera de rango rechazado")


# ─── REGLA DE NEGOCIO ─────────────────────────────────────────────────────────

def test_CRN05b_multiples_campos_invalidos():
    """CRN-05b: Múltiples campos inválidos → error por cada uno"""
    params = {**PARAMS_VALIDOS, "fc": 250, "pas": None, "temperatura": 28.0}
    r = validate_inputs(params)
    assert r["valido"] is False
    campos_error = [e["campo"] for e in r["errores"]]
    assert "fc" in campos_error
    assert "pas" in campos_error
    assert "temperatura" in campos_error
    assert len(r["errores"]) >= 3
    print(f"✓ CRN-05b PASS: {len(r['errores'])} errores detectados simultáneamente")


# ─── RUNNER ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 55)
    print("SisTriage · Pruebas M3 validator")
    print("=" * 55)
    test_CP01_todos_validos()
    test_CPN2_valores_extremos_validos()
    test_CB01_FC_limite_superior_valido()
    test_CB02_FC_limite_fuera_de_rango()
    test_CE01_campo_pas_vacio()
    test_CE02_FC_fuera_de_rango()
    test_CRN05b_multiples_campos_invalidos()
    print("=" * 55)
