import streamlit as st
import sys
import os
from datetime import datetime

# Conectar con la carpeta src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from mews_calculator import calculate_mews
from triage_classifier import classify
from validator import validate_inputs

# ─── 1. CONFIGURACIÓN VISUAL ───────────────────────────────────────────
st.set_page_config(page_title="Portal Clínico - SisTriage", page_icon="🏥", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #F4F6F9; }
    
    .clinic-banner {
        background: linear-gradient(135deg, #0077B6 0%, #00B4D8 100%);
        padding: 30px;
        border-radius: 12px;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(0, 119, 182, 0.12);
    }
    
    .clinic-card {
        background-color: #FFFFFF;
        padding: 25px;
        border-radius: 12px;
        border-top: 4px solid #00B4D8;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
        margin-bottom: 20px;
    }

    /* CLASE PARA FORZAR EL COLOR NEGRO EN TÍTULOS */
    .titulo-negro {
        color: #000000 !important;
        font-weight: 800 !important;
        font-size: 20px !important;
        margin-bottom: 15px !important;
        margin-top: 0px !important;
        display: block !important;
    }

    /* Forzar color negro en todos los textos de los formularios */
    div[data-testid="stWidgetLabel"] p, 
    div[data-testid="stWidgetLabel"] span,
    label p,
    label span {
        color: #000000 !important;
        font-weight: 700 !important;
        font-size: 15px !important;
    }

    /* NUEVO: Forzar color negro en los valores y textos de las Métricas (ej. "3 Puntos") */
    div[data-testid="stMetricValue"] > div,
    div[data-testid="stMetricLabel"] > div > p {
        color: #000000 !important;
    }

    /* Botones */
    .stButton>button {
        background: linear-gradient(135deg, #00B4D8 0%, #0077B6 100%) !important;
        color: white !important;
        font-weight: bold !important;
        font-size: 16px !important;
        padding: 14px 28px !important;
        border-radius: 8px !important;
        border: none !important;
    }
    .stButton>button:hover { transform: translateY(-2px); }
    </style>
""", unsafe_allow_html=True)

# ─── 2. BARRA LATERAL (CON SOPORTE RESTAURADO) ─────────────────────────────
with st.sidebar:
    st.markdown("<h2 style='text-align: center; font-size: 22px; color:#005F73;'>🏥 RedSalud Central</h2>", unsafe_allow_html=True)
    st.divider()
    st.markdown("<h3 style='color: #000000;'>Datos de Sesión</h3>", unsafe_allow_html=True)
    st.info("👤 **Usuario:** Personal de Enfermería\n\n🏢 **Servicio:** Urgencias Adultos\n\n🟢 **Servidor:** Conectado")
    st.divider()
    # SECCIÓN DE SOPORTE RESTAURADA
    st.markdown("<h3 style='color: #000000;'>🛠️ Soporte Interno</h3>", unsafe_allow_html=True)
    st.caption("SisTriage v1.3 - Convenio de Ingeniería de Software U. Central 2026. Ante dudas del score, consulte el manual institucional MEWS.")

# ─── 3. BANNER PRINCIPAL ──────────────────────────────────────────────────
st.markdown("""
    <div class="clinic-banner">
        <h1 style='color: white; margin: 0; font-size: 32px;'>Módulo Oficial de Admisión y Triaje</h1>
        <p style='color: #E0F7FA; margin: 8px 0 0 0; font-size: 16px;'>Clasificación automatizada de urgencias bajo estándar del protocolo MEWS</p>
    </div>
""", unsafe_allow_html=True)

# ─── 4. DATOS PERSONALES DEL PACIENTE ──────────────────────────────────────
st.markdown("<h3 style='color: #000000;'>👤 Ficha de Identificación del Paciente</h3>", unsafe_allow_html=True)
st.markdown('<div class="clinic-card">', unsafe_allow_html=True)

st.markdown('<div class="titulo-negro">📋 Datos Filiatorios y Demográficos</div>', unsafe_allow_html=True)

p_col1, p_col2, p_col3 = st.columns(3)

with p_col1:
    nombre = st.text_input("Nombre Completo", placeholder="Ej: Juan Pérez Gómez")
    edad = st.number_input("Edad (Años)", min_value=0, max_value=120, value=35)
    correo = st.text_input("Correo Electrónico", placeholder="paciente@ejemplo.com")

with p_col2:
    peso = st.number_input("Peso (kg)", min_value=1.0, max_value=250.0, value=70.0, step=0.1)
    telefono = st.text_input("Número Telefónico", placeholder="+56 9 XXXX XXXX")

with p_col3:
    altura = st.number_input("Altura (m)", min_value=0.30, max_value=2.50, value=1.70, step=0.01)
    emergencia = st.text_input("Número de Emergencia (Contacto)", placeholder="Familiar / Tutor")

st.markdown('</div>', unsafe_allow_html=True)

# ─── 5. SIGNOS VITALES ─────────────────────────────────────────────────────
st.markdown("<h3 style='color: #000000;'>📝 Control de Signos Vitales</h3>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="clinic-card">', unsafe_allow_html=True)
    st.markdown('<div class="titulo-negro">🫁 Función Cardiorespiratoria</div>', unsafe_allow_html=True)
    
    fr = st.number_input("Frecuencia Respiratoria (rpm)", min_value=1, max_value=60, value=14)
    fc = st.number_input("Frecuencia Cardíaca (bpm)", min_value=20, max_value=200, value=80)
    pas = st.number_input("Presión Arterial Sistólica (mmHg)", min_value=40, max_value=250, value=120)
    spo2 = st.number_input("Saturación de Oxígeno O₂ (%)", min_value=50, max_value=100, value=98)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="clinic-card">', unsafe_allow_html=True)
    st.markdown('<div class="titulo-negro">🧠 Estado General y Neurológico</div>', unsafe_allow_html=True)
    
    temperatura = st.number_input("Temperatura Corporal (°C)", min_value=30.0, max_value=42.0, value=37.0, step=0.1)
    avpu = st.selectbox("Nivel de Conciencia (Escala AVPU)", options=["A", "V", "P", "U"])
    eva = st.slider("Escala Visual Análoga del Dolor (EVA)", min_value=0, max_value=10, value=2)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── 6. PROCESAMIENTO ──────────────────────────────────────────────────────
if st.button("🚨 EJECUTAR CLASIFICACIÓN Y GUARDAR REGISTRO", use_container_width=True):
    if not nombre.strip():
        st.error("⚠️ El campo 'Nombre Completo' es obligatorio para archivar la ficha médica.")
    else:
        params = {
            "fr": fr, "fc": fc, "pas": pas, "temperatura": temperatura,
            "avpu": avpu, "spo2": spo2, "edad": edad, "eva": eva
        }
        
        validacion = validate_inputs(params)
        
        if not validacion["valido"]:
            st.error("❌ Error de Validación de Datos Institucionales")
            for error in validacion["errores"]:
                st.warning(f"⚠️ El campo **{error['campo'].upper()}** presenta inconsistencias: {error['mensaje']}")
        else:
            resultado_mews = calculate_mews(fr, fc, pas, temperatura, avpu, spo2, edad)
            score = resultado_mews["score_total"]
            
            triage = classify(score_total=score, avpu=avpu, spo2=spo2)
            nivel = triage["nivel"]
            tiempo = triage["tiempo_espera"]
            modificador = triage["modificador_aplicado"]
            
            fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            nombre_archivo = f"registro_{nombre.replace(' ', '_')}.txt"
            
            contenido_historial = f"""==================================================
REGISTRO CLÍNICO DE ADMISIÓN - SISTRIAGE
==================================================
Fecha/Hora de Atención: {fecha_actual}

[DATOS PERSONALES]
Nombre: {nombre}
Edad: {edad} años
Peso: {peso} kg
Altura: {altura} m
Correo: {correo}
Teléfono: {telefono}
Contacto Emergencia: {emergencia}

[SIGNOS VITALES]
Frecuencia Respiratoria: {fr} rpm
Frecuencia Cardíaca: {fc} bpm
Presión Arterial Sistólica: {pas} mmHg
Saturación O2: {spo2} %
Temperatura: {temperatura} °C
Escala AVPU: {avpu}
Escala EVA (Dolor): {eva}/10

[DICTAMEN DE TRIAGE]
Score MEWS Calculado: {score} Puntos
Clasificación Asignada: Nivel {nivel}
Tiempo Máximo de Espera: {tiempo}
Modificador del Sistema: {modificador if modificador else "Ninguno"}
==================================================
\n"""
            
            with open(nombre_archivo, "a", encoding="utf-8") as f:
                f.write(contenido_historial)
                
            st.success(f"💾 ¡Ficha clínica guardada con éxito en el archivo de historial local: `{nombre_archivo}`!")
            
            st.markdown("---")
            
            # CAMBIO AQUÍ: Aplicamos la clase titulo-negro para el informe y dictamen, haciéndolo un poco más grande
            st.markdown('<div class="titulo-negro" style="font-size: 24px; margin-top: 10px;">📊 Informe y Dictamen del Triage</div>', unsafe_allow_html=True)
            
            if nivel == "Verde":
                color_badge, color_text, border_color = "#D4EDDA", "#155724", "#28A745"
            elif nivel == "Amarillo":
                color_badge, color_text, border_color = "#FFF3CD", "#856404", "#FFC107"
            elif nivel == "Naranja":
                color_badge, color_text, border_color = "#FFE8D6", "#D97706", "#F97316"
            else: # Rojo
                color_badge, color_text, border_color = "#F8D7DA", "#721C24", "#DC3545"
                
            st.markdown(f"""
                <div style="background-color: {color_badge}; border-left: 6px solid {border_color}; padding: 25px; border-radius: 8px; margin-bottom: 20px;">
                    <h2 style="color: {color_text}; margin: 0; font-size: 26px;">Clasificación: Nivel {nivel}</h2>
                    <p style="color: {color_text}; margin: 8px 0 0 0; font-size: 18px; font-weight: bold;">🚨 Tiempo de Respuesta Estándar: {tiempo}</p>
                </div>
            """, unsafe_allow_html=True)
            
            res_col1, res_col2 = st.columns(2)
            with res_col1:
                st.metric(label="Puntaje MEWS Total del Paciente", value=f"{score} Puntos")
            with res_col2:
                if modificador:
                    st.warning(f"⚙️ **Criterio de Ajuste Clínico:** {modificador}")
                else:
                    st.success("✅ Clasificación directa sin alertas secundarias detectadas.")