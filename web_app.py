import streamlit as st
import sys
import os
import csv
from datetime import datetime

# Conectar al ecosistema interno
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from mews_calculator import calculate_mews
from triage_classifier import classify
from validator import validate_inputs

# ─── 1. CONFIGURACIÓN VISUAL Y CONTROL DE COLORES PERSONALIZADOS ───────
st.set_page_config(
    page_title="SisTriage v2.0 - Suite Médica Hospitalaria",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    /* 1. CONFIGURACIÓN DE FONDOS CLAROS (Para alta legibilidad) */
    .stApp { 
        background-color: #F8FAFC !important; 
    }
    [data-testid="stSidebar"] {
        background-color: #E2E8F0 !important;
    }
    
    /* 2. FORZAR NEGRO EN TEXTOS GENERALES, ETIQUETAS Y LEYENDAS */
    html, body, .stApp, .stApp p, .stApp label, .stApp span, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp li, .stApp small, .stApp div {
        color: #000000 !important;
    }
    
    /* Regla específica para los títulos de campos exteriores (ej: "Tipo de Identificación") */
    div[data-testid="stWidgetLabel"] p, label {
        color: #000000 !important; 
        font-weight: 700 !important;
        font-size: 0.95rem !important;
    }
    
    /* 3. TEXTO CLARO ADENTRO DE SELECTBOX Y NUMBER_INPUT */
    div[data-baseweb="select"] div, 
    div[data-testid="stNumberInput"] input,
    div[data-testid="stTextInput"] input,
    .stSelectbox div[data-selected="true"] {
        color: #FFFFFF !important;
        background-color: #1E293B !important; 
        font-weight: 600 !important;
    }

    /* Controles numéricos (+/-) visibles y elegantes */
    div[data-testid="stNumberInput"] button {
        background-color: #334155 !important;
        color: #FFFFFF !important;
        border: 1px solid #475569 !important;
    }

    /* Cabecera institucional limpia */
    .header-banner {
        background: linear-gradient(135deg, #E2E8F0 0%, #F1F5F9 100%);
        padding: 24px 32px;
        border-radius: 12px;
        margin-bottom: 24px;
        border: 2px solid #CBD5E1;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    
    /* Contenedores y Tarjetas Clínicas */
    .medical-card {
        background: #FFFFFF !important;
        padding: 24px;
        border-radius: 10px;
        border: 1px solid #CBD5E1;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }

    /* Títulos internos de las tarjetas */
    .card-title {
        font-weight: 700;
        font-size: 1.15rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #CBD5E1;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Pestañas de Navegación superiores (Tabs) */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #E2E8F0 !important;
        border-radius: 6px 6px 0px 0px;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #CBD5E1 !important;
        border: 1px solid #94A3B8;
    }

    /* Botón de Procesamiento de Admisión */
    .stButton>button {
        background: linear-gradient(135deg, #E2E8F0 0%, #CBD5E1 100%) !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        padding: 0.75rem 1.5rem !important;
        border-radius: 8px !important;
        border: 2px solid #94A3B8 !important;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #CBD5E1 0%, #94A3B8 100%) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }
    </style>
""", unsafe_allow_html=True)

# ─── 2. PANEL LATERAL INFORMATIVO ──────────────────────────────────────
with st.sidebar:
    st.markdown("### 🏥 RedSalud Central")
    st.caption("Sistema Integrado de Urgencias Médicas")
    st.divider()
    
    st.markdown("#### 👤 Operador Clínico")
    st.markdown("""
    - **Rol:** Enfermero/a de Triage
    - **Turno:** Diurno (08:00 - 20:00)
    - **Puesto:** Box Admisión #3
    - **Servicio:** Urgencia Adulto
    """)
    st.divider()
    
    st.markdown("#### ⚙️ Parámetros de Sistema")
    st.success("🟢 Conexión a BD Central activa")
    st.caption("SisTriage v2.0 Enterprise Release | Algoritmo MEWS Certificado.")

# ─── 3. CABECERA DE LA PÁGINA ──────────────────────────────────────────
st.markdown("""
    <div class="header-banner">
        <h1 style='margin: 0; font-size: 1.8rem; font-weight: 800;'>Módulo Central de Admisión y Triage</h1>
        <p style='margin: 6px 0 0 0; font-size: 0.95rem; font-weight: 600;'>Ingreso demográfico integral y evaluación estandarizada de gravedad clínica.</p>
    </div>
""", unsafe_allow_html=True)

# Pestañas para dividir ordenadamente la interfaz
tab_ingreso, tab_historial = st.tabs(["⚡ Admisión de Paciente", "🗃️ Historial de Turno Actual"])

with tab_ingreso:
    # ─── 4. MÓDULO DE IDENTIFICACIÓN Y DEMOGRAFÍA ──────────────────────────
    st.markdown('<div class="medical-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🪪 Identificación Ciudadana y Antecedentes Sociodemográficos</div>', unsafe_allow_html=True)
    
    col_id1, col_id2, col_id3, col_id4 = st.columns([1.5, 2, 1.5, 1])
    
    with col_id1:
        tipo_doc = st.selectbox("Tipo de Identificación", ["RUT Chileno", "Pasaporte Extranjero", "DNI / ID Internacional"])
    
    with col_id2:
        if tipo_doc == "RUT Chileno":
            num_doc = st.text_input("Número de RUT", placeholder="12.345.678-9", help="Ingrese con o sin puntos y guion.")
        else:
            num_doc = st.text_input("Número de Pasaporte o ID", placeholder="A123456789")
            
    with col_id3:
        nacionalidad = st.selectbox("Nacionalidad", [
            "Chilena", "Venezolana", "Colombiana", "Peruana", "Argentina", 
            "Boliviana", "Ecuatoriana", "Haitiana", "Otra nacionalidad"
        ])
        
    with col_id4:
        edad = st.number_input("Edad", min_value=0, max_value=120, value=35, step=1)

    col_dem1, col_dem2, col_dem3 = st.columns([2, 1.5, 1.5])
    with col_dem1:
        nombre = st.text_input("Nombre Completo del Paciente", placeholder="Ej. Ana María Silva Morales")
    with col_dem2:
        genero = st.selectbox("Sexo Biológico / Género Registral", ["Femenino", "Masculino", "Intersexual", "No Especificado"])
    with col_dem3:
        prevision = st.selectbox("Previsión / Seguro Médico", [
            "FONASA A", 
            "FONASA B", 
            "FONASA C", 
            "FONASA D", 
            "ISAPRE", 
            "PRAIS", 
            "Particular / Ley de Urgencia"
        ])

    col_dir1, col_dir2, col_dir3 = st.columns([2, 1.5, 1.5])
    with col_dir1:
        direccion = st.text_input("Dirección de Residencia", placeholder="Av. Providencia 1234, Dpto 402")
    with col_dir2:
        comuna = st.text_input("Comuna / Ciudad", placeholder="Santiago / Viña del Mar")
    with col_dir3:
        telefono = st.text_input("Teléfono de Contacto", placeholder="+56 9 8765 4321")
        
    st.markdown('</div>', unsafe_allow_html=True)

    # ─── 5. PARÁMETROS ANTROPOMÉTRICOS Y SIGNOS VITALES ──────────────────
    st.markdown('<div class="medical-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🩺 Biomarcadores y Evaluación Fisiológica de Ingreso</div>', unsafe_allow_html=True)
    
    c_bio1, c_bio2, c_bio3, c_bio4 = st.columns(4)
    with c_bio1:
        peso = st.number_input("Peso (kg)", min_value=1.0, max_value=250.0, value=70.0, step=0.5)
    with c_bio2:
        altura = st.number_input("Estatura (m)", min_value=0.30, max_value=2.40, value=1.70, step=0.01)
    with c_bio3:
        imc = round(peso / (altura ** 2), 1) if altura > 0 else 0
        st.metric("Índice de Masa Corporal (IMC)", f"{imc} kg/m²")
    with c_bio4:
        emergencia_contacto = st.text_input("Familiar o Tutor de Urgencia", placeholder="Nombre / Relación")

    st.markdown("<hr style='margin: 15px 0; border-color: #CBD5E1;'>", unsafe_allow_html=True)
    
    col_sv1, col_sv2, col_sv3, col_sv4 = st.columns(4)
    with col_sv1:
        fr = st.number_input("Frec. Respiratoria (rpm)", min_value=1, max_value=60, value=14, help="Respiraciones por minuto.")
        pas = st.number_input("Presión Sistólica (mmHg)", min_value=40, max_value=250, value=120)
    with col_sv2:
        fc = st.number_input("Frec. Cardíaca (bpm)", min_value=20, max_value=200, value=80, help="Latidos por minuto.")
        temperatura = st.number_input("Temperatura Corporal (°C)", min_value=30.0, max_value=42.0, value=36.8, step=0.1)
    with col_sv3:
        spo2 = st.number_input("Saturación Oxígeno O₂ (%)", min_value=50, max_value=100, value=98)
        eva = st.slider("Escala Dolor (EVA 0-10)", min_value=0, max_value=10, value=1)
    with col_sv4:
        avpu = st.selectbox("Estado Alerta (Escala AVPU)", options=["A", "V", "P", "U"], help="A: Alerta, V: Voz, P: Dolor, U: Inconsciente")
        sintomas_clave = st.text_input("Motivo Principal de Consulta", placeholder="Ej: Dolor torácico opresivo de 1h de evolución")

    st.markdown('</div>', unsafe_allow_html=True)

    # ─── 6. EJECUCIÓN CLÍNICA Y PROCESAMIENTO ────────────────────────────
    if st.button("⚖️ PROCESAR ADMISIÓN Y ASIGNAR TRIAGE CLÍNICO", use_container_width=True):
        params_validacion = {
            "nombre": nombre, "tipo_doc": tipo_doc, "num_doc": num_doc,
            "fr": fr, "fc": fc, "pas": pas, "temperatura": temperatura,
            "avpu": avpu, "spo2": spo2, "edad": edad, "eva": eva
        }
        
        resultado_validacion = validate_inputs(params_validacion)
        
        if not resultado_validacion["valido"]:
            st.error("🚨 **Interrupción de Admisión:** Se detectaron errores críticos en el formulario.")
            for error in resultado_validacion["errores"]:
                st.warning(f"⚠️ **{error['campo']}:** {error['mensaje']}")
        else:
            # Procesamiento Clínico
            resultado_mews = calculate_mews(fr, fc, pas, temperatura, avpu, spo2, edad)
            score = resultado_mews["score_total"]
            
            triage = classify(score_total=score, avpu=avpu, spo2=spo2)
            
            # SOLUCIÓN AL ERROR: Uso seguro de .get() para evitar KeyError
            nivel = triage.get("nivel", "Verde")
            tiempo = triage.get("tiempo_espera", triage.get("tiempo", "Inmediato"))
            modificador = triage.get("modificador_aplicado", triage.get("modificador", None))
            
            # Persistencia CSV
            archivo_bd = "base_datos_pacientes.csv"
            campos_bd = [
                "Fecha", "Documento", "Tipo_Doc", "Nombre", "Nacionalidad", "Edad", 
                "Genero", "Prevision", "Comuna", "Score_MEWS", "Nivel_Triage", "Tiempo_Espera"
            ]
            
            archivo_existe = os.path.isfile(archivo_bd)
            with open(archivo_bd, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                if not archivo_existe:
                    writer.writerow(campos_bd)
                writer.writerow([
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"), num_doc, tipo_doc, 
                    nombre, nacionalidad, edad, genero, prevision, comuna, score, nivel, tiempo
                ])
                
            st.toast("✅ Expediente clínico guardado con éxito.")
            
            # ─── VISUALIZACIÓN DEL DICTAMEN DE TRIAGE ───────────────────────
            colores_nivel = {
                "Verde": {"bg": "#DCFCE7", "border": "#16A34A"},
                "Amarillo": {"bg": "#FEF9C3", "border": "#CA8A04"},
                "Naranja": {"bg": "#FFEDD5", "border": "#EA580C"},
                "Rojo": {"bg": "#FEE2E2", "border": "#DC2626"}
            }
            cfg = colores_nivel.get(nivel, colores_nivel["Verde"])
            
            st.markdown(f"""
                <div style="background-color: {cfg['bg']}; border-left: 8px solid {cfg['border']}; padding: 24px; border-radius: 8px; margin: 24px 0;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <h2 style="color: #000000 !important; margin: 0; font-size: 1.7rem; font-weight: 800;">CATEGORÍA DE RIESGO: NIVEL {nivel.upper()}</h2>
                            <p style="color: #000000 !important; margin: 6px 0 0 0; font-size: 1.1rem; font-weight: 600;">⏱️ Meta de Atención Médica: {tiempo}</p>
                        </div>
                        <div style="background: #E2E8F0; color: #000000 !important; padding: 12px 24px; border-radius: 50px; font-weight: 800; font-size: 1.3rem; border: 2px solid #94A3B8;">
                            MEWS: {score} pts
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            c_info1, c_info2 = st.columns([1, 2])
            with c_info1:
                st.info(f"📋 **Especialidad:** {'Reanimación' if nivel=='Rojo' else 'Urgencia General'}")
            with c_info2:
                if modificador:
                    st.warning(f"⚡ **Alerta Biomecánica:** {modificador}")
                else:
                    st.success("✅ Estabilización compensada sin gatillantes críticos secundarios.")

with tab_historial:
    st.markdown("### 🗃️ Registro General de Triage en Turno")
    if os.path.isfile("base_datos_pacientes.csv"):
        import pandas as pd
        df = pd.read_csv("base_datos_pacientes.csv")
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        with open("base_datos_pacientes.csv", "rb") as f:
            st.download_button(
                label="📥 Descargar Base de Datos Completa (CSV / Excel)",
                data=f,
                file_name=f"reporte_triage_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    else:
        st.info("No hay pacientes registrados en el turno actual todavía.")