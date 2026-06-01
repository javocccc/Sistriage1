# 🏥 SisTriage — Sistema de Triaje de Urgencias Hospitalarias

> Clasificación automática de pacientes mediante algoritmo **MEWS** (Modified Early Warning Score)

**Ingeniería Civil en Computación e Informática · Universidad Central de Chile**  
Autores: Javier Carrasco · Matías Olivares  
Stakeholders: Benjamín López · Fernando Godoy  
Docente: Gonzalo Honores · ERS v1.1 · Mayo 2026

---

## 📋 Descripción

SisTriage resuelve un problema crítico en urgencias: sin clasificación objetiva, el personal puede atender casos leves mientras un paciente en riesgo vital espera. El sistema calcula el score MEWS a partir de 8 signos vitales y entrega una clasificación en 4 niveles de prioridad con trazabilidad completa.

**Error aceptable en el cálculo: 0.**

---

## 📂 Estructura del Repositorio

```
Sistriagee/
│
├── main.py                          ← Demo CLI interactiva (punto de entrada)
├── requirements.txt                 ← Dependencias (solo pytest)
├── README.md
│
├── src/
│   ├── mews_calculator.py           ← M1: cálculo del score MEWS
│   ├── triage_classifier.py         ← M2: clasificación + modificadores + override
│   └── validator.py                 ← M3: validación de parámetros de entrada
│
├── tests/
│   ├── test_mews_calculator.py      ← 9 pruebas unitarias M1 (incl. dataset 12/12)
│   ├── test_triage_classifier.py    ← 9 pruebas unitarias M2
│   └── test_validator.py            ← 7 pruebas unitarias M3
│
└── docs/
    ├── ERS_SisTriage_v1.1.docx      ← Especificación de Requisitos completa
    ├── modulos.md                   ← Diseño lógico: módulos, entradas, salidas
    ├── casos_de_prueba.md           ← Definición de los 25 casos de prueba
    ├── matriz_trazabilidad.md       ← RF → módulo → función → prueba → resultado
    └── arquitectura_logica_DFD.svg  ← Diagrama DFD
```

---

## ⚡ Inicio Rápido (para equipo QA)

### Requisitos previos
- Python **3.10 o superior**
- `pip` (incluido con Python)
- Sistema operativo: Windows 10+, macOS 12+, Linux (Ubuntu 20.04+)
- No se requiere base de datos ni servidor web

### 1. Clonar el repositorio
```bash
git clone https://github.com/javocccc/Sistriage1.git
cd Sistriage1
```

### 2. Instalar dependencia (solo pytest)
```bash
pip install -r requirements.txt
```

### 3. Ejecutar la demo interactiva
```bash
python main.py
```
Se abrirá un menú con 4 opciones:

| Opción | Descripción |
|--------|-------------|
| `1` | Demo automática — procesa 6 pacientes del dataset de prueba |
| `2` | Modo interactivo — ingresa un paciente manualmente |
| `3` | Demo de validación — muestra rechazo de datos inválidos |
| `4` | Ejecuta las pruebas unitarias (pytest) |

### 4. Ejecutar demo sin interacción (modo QA)
```bash
python main.py --demo
```

### 5. Ejecutar pruebas unitarias directamente
```bash
python -m pytest tests/ -v
```

**Resultado esperado:** `25 passed in ~0.1s`

---

## 🎯 Niveles de Clasificación MEWS

| Color | Nivel | Score MEWS | Tiempo máximo |
|-------|-------|-----------|--------------|
| 🟢 Verde | No urgente | 0 – 1 | > 2 horas |
| 🟡 Amarillo | Urgente | 2 – 3 | < 30 min |
| 🟠 Naranja | Muy urgente | 4 – 5 | < 10 min |
| 🔴 Rojo | Inmediato | ≥ 6 | Inmediato |

---

## ⚙️ Módulos Principales

| Módulo | Archivo | Responsabilidad |
|--------|---------|----------------|
| M1 | `src/mews_calculator.py` | Calcula score MEWS con desglose por variable |
| M2 | `src/triage_classifier.py` | Clasifica nivel + aplica modificadores (RN-03, RN-04) + override (RF-09) |
| M3 | `src/validator.py` | Valida rangos, tipos y completitud (RF-01, RN-01, RN-02) |

---

## 🧪 Cobertura de Pruebas

| Tipo | Cantidad | Módulos cubiertos |
|------|----------|------------------|
| Casos normales | 6 | M1, M2, M3 |
| Casos de borde | 8 | M1, M2, M3 |
| Casos de error | 5 | M2, M3 |
| Reglas de negocio | 6 | M1, M2 |
| **Total** | **25** | M1, M2, M3 |

---

## 📌 Reglas de Negocio Implementadas

| ID | Regla |
|----|-------|
| RN-01 | Todos los campos son obligatorios |
| RN-02 | Valores fuera de rango rechazados antes del cálculo |
| RN-03 | AVPU=U → nivel mínimo Naranja |
| RN-04 | SpO₂ < 85% → nivel mínimo Rojo |
| RF-09 | Override clínico manual requiere justificación ≥ 20 chars y nivel ≥ calculado |

---

## 🔍 Casos Críticos para el Equipo QA

1. **CE-01:** Ingresar PAS vacía → debe rechazarse con mensaje "Campo obligatorio"
2. **CE-02:** Ingresar FC=250 → debe rechazarse con mensaje de rango
3. **CRN-01:** AVPU=U con score=2 → debe clasificar Naranja (no Amarillo)
4. **CRN-02:** SpO₂=80 con score=1 → debe clasificar Rojo (no Verde)
5. **CB-03:** FR=9 → debe asignar 0 pts (no 2 pts del rango <9)
6. **CA-1:** Dataset completo 12/12 → todos deben coincidir con score esperado

---

## 📎 Referencias

- Subbe CP et al. (2001). *Validation of a Modified Early Warning Score.* QJM.
- ERS SisTriage v1.1 — Carrasco, Olivares (2026)
