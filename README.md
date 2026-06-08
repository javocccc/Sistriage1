# 🏥 SisTriage — Sistema Avanzado de Triaje Clínico

> **Clasificación automatizada de urgencias hospitalarias mediante el algoritmo MEWS (Modified Early Warning Score)**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B.svg)](https://streamlit.io/)
[![Pytest](https://img.shields.io/badge/Pytest-Testing-yellow.svg)](https://docs.pytest.org/)

**Autores:** Javier Carrasco · Matías Olivares  
**Stakeholders:** Benjamín López · Fernando Godoy  
**Docente:** Gonzalo Honores · Universidad Central de Chile (2026)

---

## 📋 Descripción del Proyecto

SisTriage es una solución de software diseñada para resolver la saturación en las salas de urgencias. El sistema captura los signos vitales de los pacientes y calcula de manera algorítmica y sin margen de error el **Score MEWS**, clasificando al paciente en 4 niveles de prioridad (Verde, Amarillo, Naranja, Rojo) y dictaminando su tiempo de espera ideal.

**El proyecto cuenta con dos interfaces funcionales:**
1. **Core CLI (Terminal):** Un entorno interactivo de línea de comandos ligero, ideal para despliegues rápidos y pruebas en servidores sin interfaz gráfica.
2. **Portal Clínico Web:** Una interfaz gráfica moderna, institucional y de alto contraste (adaptada para entornos hospitalarios), con persistencia de datos locales y generación de fichas clínicas.

---

## ✨ Características Principales

- **⚙️ Motor Lógico Aislado:** Lógica de negocio (Cálculo MEWS, Clasificación y Validación) modularizada en la carpeta `src/`.
- **🌐 Interfaz Web Streamlit:** Diseño responsivo con paleta de colores institucional (Cyan, Celeste, Blanco, Gris) e inyección de CSS personalizado para asegurar alto contraste (textos negros puros).
- **💾 Historial Clínico Local:** Capacidad de registrar y guardar los datos filiatorios y médicos del paciente en un archivo `.txt` automatizado.
- **🛡️ Alta Tolerancia a Errores:** Validación exhaustiva de tipos de datos, campos vacíos y valores fisiológicos fuera de rango (ej. FC > 200).
- **🧪 Cobertura de Testing:** 25 pruebas unitarias automatizadas a través de `pytest`.

---

## 📂 Estructura del Repositorio

```text
Sistriage1/
│
├── web_app.py                       ← Interfaz WEB (Portal Clínico Principal)
├── main.py                          ← Interfaz CLI (Consola interactiva)
├── requirements.txt                 ← Dependencias del proyecto
├── README.md                        ← Documentación
│
├── src/                             ← Lógica de Negocio
│   ├── mews_calculator.py           ← (M1) Cálculo del score MEWS
│   ├── triage_classifier.py         ← (M2) Clasificación y modificadores
│   └── validator.py                 ← (M3) Validación de datos de entrada
│
└── tests/                           ← Pruebas Unitarias
    ├── test_mews_calculator.py      
    ├── test_triage_classifier.py    
    └── test_validator.py
```

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
python -m pip install -r requirements.txt
```

### 🖥️ Uso del Sistema
```bash
python -m streamlit run web_app.py
```

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
##🚨 Guía de Solución de Problemas (Troubleshooting)

| Síntoma / Error | Causa Raíz | Solución Rápida |
|-------|-------|-----------|
| Fatal error in launcher: Unable to create process| Acceso directo de pip dañado en Windows.| Usa siempre python -m pip install <paquete> para forzar el uso del entorno de Python actual.| Usa siempre python -m pip install <paquete> para forzar el uso del entorno de Python actual. |
| No such file or directory: 'requeriments.txt' | Error de tipeo (typo) al buscar el archivo de dependencias. | verifica escribir correctamente requirements.txt. |
| AttributeError: module 'streamlit' has no attribute 'number' | Error de sintaxis en el código web. | Cambiar la función st.number.input() por st.number_input(). |
| Textos blancos/grises en la Web (Falta de contraste) | El Modo Oscuro predeterminado de Streamlit oculta los estilos inyectados. | Ve al Menú superior derecho de la web (⚙️) > Settings > Theme > Cambiar a Light. Luego presiona Ctrl + F5. |

    
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
