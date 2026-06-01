"""
test_triage_classifier.py
Pruebas unitarias — Módulo M2: triage_classifier
SisTriage · ERS v1.1

Cobertura: CP-01/02 (normales), CB-04/CB-06 (borde), CE-03/CE-04 (error),
           CRN-01/CRN-02/CRN-04 (reglas de negocio)
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from triage_classifier import classify


# ─── CASOS NORMALES ───────────────────────────────────────────────────────────

def test_CP01_score0_nivel_verde():
    """CP-01: Score=0 → Verde, sin modificadores"""
    r = classify(score_total=0, avpu="A", spo2=98)
    assert r["nivel"] == "Verde"
    assert r["modificador_aplicado"] is None
    assert r["es_override"] is False
    print("✓ CP-01 PASS: score=0 → Verde")


def test_CP02_score14_nivel_rojo():
    """CP-02: Score=14 → Rojo"""
    r = classify(score_total=14, avpu="V", spo2=88)
    assert r["nivel"] == "Rojo"
    assert r["modificador_aplicado"] is None
    print("✓ CP-02 PASS: score=14 → Rojo")


# ─── CASOS DE BORDE ───────────────────────────────────────────────────────────

def test_CB04_score4_debe_ser_naranja():
    """CB-04: Score=4 → Naranja (límite exacto; no Amarillo que va hasta score=3)"""
    r = classify(score_total=4, avpu="A", spo2=95)
    assert r["nivel"] == "Naranja", f"Score=4 debe ser Naranja, obtenido: {r['nivel']}"
    print("✓ CB-04 PASS: score=4 → Naranja")


def test_CB06_score6_es_rojo():
    """CB-06: Score=6 → Rojo (umbral exacto de Rojo)"""
    r = classify(score_total=6, avpu="A", spo2=95)
    assert r["nivel"] == "Rojo"
    print("✓ CB-06 PASS: score=6 → Rojo")


# ─── CASOS DE ERROR ───────────────────────────────────────────────────────────

def test_CE03_override_sin_justificacion():
    """CE-03: Override clínico sin justificación → rechazado"""
    r = classify(score_total=0, avpu="A", spo2=98,
                 override_nivel="Rojo", override_justificacion=None)
    assert r["error"] is not None, "Debe retornar error"
    assert r["nivel"] == "Verde", "El nivel no debe cambiar sin justificación"
    assert r["es_override"] is False
    print("✓ CE-03 PASS: override sin justificación rechazado")


def test_CE04_override_baja_nivel():
    """CE-04: Override intenta bajar el nivel → rechazado"""
    r = classify(score_total=8, avpu="A", spo2=95,  # score=8 → Rojo
                 override_nivel="Verde", override_justificacion="Quiero bajar el nivel")
    assert r["error"] is not None
    assert r["nivel"] == "Rojo", "El nivel Rojo no puede bajar a Verde"
    print("✓ CE-04 PASS: override que baja nivel rechazado")


# ─── REGLAS DE NEGOCIO ────────────────────────────────────────────────────────

def test_CRN01_AVPU_U_fuerza_naranja():
    """CRN-01 / RN-03: AVPU=U con score bajo → forzar Naranja mínimo"""
    r = classify(score_total=2, avpu="U", spo2=95)
    assert r["nivel"] == "Naranja", f"AVPU=U debe forzar Naranja, obtenido: {r['nivel']}"
    assert "AVPU" in r["modificador_aplicado"]
    print("✓ CRN-01 PASS: AVPU=U → Naranja forzado")


def test_CRN02_spo2_bajo_fuerza_rojo():
    """CRN-02 / RN-04: SpO₂ < 85% con score bajo → forzar Rojo"""
    r = classify(score_total=1, avpu="A", spo2=80)
    assert r["nivel"] == "Rojo", f"SpO₂<85% debe forzar Rojo, obtenido: {r['nivel']}"
    assert "SpO" in r["modificador_aplicado"]
    print("✓ CRN-02 PASS: SpO₂<85% → Rojo forzado")


def test_CRN04_override_clinico_valido():
    """CRN-04 / RF-09: Override clínico válido con justificación suficiente"""
    r = classify(score_total=0, avpu="A", spo2=98,
                 override_nivel="Rojo",
                 override_justificacion="Sospecha de ACV isquémico, déficit motor agudo hemicuerpo derecho")
    assert r["nivel"] == "Rojo"
    assert r["es_override"] is True
    assert r["error"] is None
    print("✓ CRN-04 PASS: override clínico válido aplicado")


# ─── RUNNER ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 55)
    print("SisTriage · Pruebas M2 triage_classifier")
    print("=" * 55)
    test_CP01_score0_nivel_verde()
    test_CP02_score14_nivel_rojo()
    test_CB04_score4_debe_ser_naranja()
    test_CB06_score6_es_rojo()
    test_CE03_override_sin_justificacion()
    test_CE04_override_baja_nivel()
    test_CRN01_AVPU_U_fuerza_naranja()
    test_CRN02_spo2_bajo_fuerza_rojo()
    test_CRN04_override_clinico_valido()
    print("=" * 55)
