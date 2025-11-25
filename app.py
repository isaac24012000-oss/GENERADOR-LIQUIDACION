"""
Aplicación Web Streamlit - Sistema de Liquidaciones WorldTel
Interfaz web para generar liquidaciones en PDF
"""

import streamlit as st
import pandas as pd
import sys
import os
from datetime import datetime

# Configuración de página
st.set_page_config(
    page_title="Liquidaciones WorldTel",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Importar generadores
sys.path.insert(0, os.path.dirname(__file__))
from generador_cache import GeneradorCache
from generador_pdf import GeneradorPDF

# Estilos CSS personalizados
st.markdown("""
<style>
    .main {
        padding-top: 2rem;
    }
    .stTitle {
        color: #203864;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    .header-info {
        background-color: #E7F3FF;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 2rem;
        border-left: 4px solid #4472C4;
    }
    .success-box {
        background-color: #E2F0D9;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #70AD47;
    }
    .info-box {
        background-color: #FFF2CC;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #FFC000;
    }
    .stats {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin-bottom: 2rem;
    }
    .stat-card {
        background-color: #F5F5F5;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
        border: 1px solid #DDDDDD;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# INICIALIZACIÓN
# ============================================================================

@st.cache_resource
def cargar_generador():
    """Carga el generador desde caché (ultra-rápido)"""
    # Mostrar barra de progreso
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    base_path = os.path.dirname(__file__)
    
    # Usar caché para carga rápida
    if GeneradorCache.archivo_cache_existe():
        status_text.info("⏳ Cargando desde caché...")
        progress_bar.progress(50)
    else:
        status_text.info("⏳ Primera carga... esto tomará ~5-10 segundos")
        progress_bar.progress(25)
    
    try:
        gen = GeneradorCache.obtener_generador(base_path)
        progress_bar.progress(100)
        status_text.empty()
        progress_bar.empty()
        return gen
    except Exception as e:
        status_text.error(f"❌ Error: {e}")
        raise

@st.cache_resource
def cargar_generador_pdf():
    """Carga el generador PDF"""
    return GeneradorPDF()

# Cargar generadores con estado
try:
    gen = cargar_generador()
    gen_pdf = cargar_generador_pdf()
except Exception as e:
    st.error(f"❌ Error al cargar sistema: {e}")
    st.stop()

# ============================================================================
# INTERFAZ PRINCIPAL
# ============================================================================

# Encabezado
col1, col2 = st.columns([3, 1])
with col1:
    st.title("📄 Generador de Liquidaciones")
    st.markdown("**WorldTel** - Sistema de Generación de Liquidaciones")

with col2:
    st.info(f"📅 {datetime.now().strftime('%d/%m/%Y')}")

# Mensaje de estado
if 'sistema_listo' not in st.session_state:
    st.session_state.sistema_listo = True
    with st.success("✅ Sistema cargado correctamente"):
        st.write("Todos los datos están en memoria. Sistema listo para usar.")

# Información del sistema
html_info = f"""
<div class="header-info">
    <strong>📊 Sistema Operativo</strong><br>
    RUCs únicos: <strong>{len(gen.obtener_rucs())}</strong> | 
    Casos totales: <strong>9,137</strong> | 
    Campañas: <strong>4</strong>
</div>
"""
st.markdown(html_info, unsafe_allow_html=True)

# ============================================================================
# FORMULARIO DE GENERACIÓN
# ============================================================================

st.markdown("## 🔧 Generar Liquidación")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Seleccione RUC")
    
    # Búsqueda de RUC
    rucs = gen.obtener_rucs()
    rucs_str = [str(r) for r in rucs]
    
    ruc_input = st.text_input(
        "Ingrese RUC:",
        placeholder="Ejemplo: 20212246698",
        key="ruc_input"
    )
    
    # Buscar RUC
    ruc_encontrado = None
    campanas_disponibles = []
    
    if ruc_input:
        # Búsqueda exacta o parcial
        coincidencias = [r for r in rucs_str if ruc_input in r]
        
        if coincidencias:
            if len(coincidencias) == 1:
                ruc_encontrado = float(coincidencias[0])
                campanas_disponibles = gen.obtener_campanas_ruc(ruc_encontrado)
            else:
                st.warning(f"⚠️ {len(coincidencias)} coincidencias encontradas")
                ruc_seleccionado = st.selectbox(
                    "Seleccione el RUC correcto:",
                    coincidencias,
                    key="ruc_select"
                )
                ruc_encontrado = float(ruc_seleccionado)
                campanas_disponibles = gen.obtener_campanas_ruc(ruc_encontrado)
        else:
            st.error("❌ RUC no encontrado")

with col2:
    st.markdown("### Seleccione Campaña")
    
    if ruc_encontrado and campanas_disponibles:
        campana_seleccionada = st.selectbox(
            "Campaña:",
            campanas_disponibles,
            key="campana_select"
        )
    else:
        st.info("Ingrese un RUC válido para ver las campañas disponibles")
        campana_seleccionada = None

# Información adicional
if ruc_encontrado and campana_seleccionada:
    st.markdown("---")
    st.markdown("### 📋 Información del Deudor")
    
    try:
        datos_ruc = gen.filtrar_por_ruc_campana(ruc_encontrado, campana_seleccionada)
        razon_social = datos_ruc.iloc[0]['RAZON_SOCIAL']
        total_deuda = datos_ruc['DEUDA_CON_MORA'].sum()
        num_registros = len(datos_ruc)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            ruc_formateado = str(int(ruc_encontrado))
            st.metric("RUC", ruc_formateado)
        with col2:
            st.metric("Registros", num_registros)
        with col3:
            st.metric("Total Deuda", f"S/. {total_deuda:.2f}")
        
        st.info(f"**Razón Social:** {razon_social}")
        
        # Formulario de opciones
        st.markdown("---")
        st.markdown("### ⚙️ Opciones Adicionales")
        
        col1, col2 = st.columns(2)
        with col1:
            direccion = st.text_input(
                "Dirección (opcional):",
                placeholder="Calle Principal 123",
                key="direccion"
            )
        
        with col2:
            fecha_pago = st.date_input(
                "Fecha de pago:",
                datetime.now(),
                key="fecha_pago"
            )
        
        # Botón de generación
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            generar = st.button(
                "📥 Generar PDF",
                use_container_width=True,
                type="primary"
            )
        
        with col2:
            ver_datos = st.button(
                "📊 Ver Datos",
                use_container_width=True
            )
        
        # Generar PDF
        if generar:
            with st.spinner("Generando PDF..."):
                try:
                    # Generar PDF
                    pdf_bytes = gen_pdf.generar_liquidacion_pdf(
                        ruc=ruc_encontrado,
                        campana=campana_seleccionada,
                        razon_social=razon_social,
                        datos_ruc=datos_ruc,
                        direccion=direccion,
                        fecha_pago=fecha_pago.strftime('%d/%m/%Y')
                    )
                    
                    # Nombre del archivo
                    campana_abrev = campana_seleccionada.replace(" ", "_").upper()[:10]
                    ruc_str = str(int(ruc_encontrado))
                    nombre_archivo = f"LIQUIDACION_{ruc_str}_{campana_abrev}_{fecha_pago.strftime('%d%m%Y')}.pdf"
                    
                    # Botón de descarga
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.download_button(
                            label="📥 Descargar PDF",
                            data=pdf_bytes,
                            file_name=nombre_archivo,
                            mime="application/pdf",
                            use_container_width=True
                        )
                    
                    html_success = f"""
                    <div class="success-box">
                        <strong>✅ PDF generado exitosamente</strong><br>
                        <small>{nombre_archivo}</small>
                    </div>
                    """
                    st.markdown(html_success, unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"❌ Error al generar PDF: {e}")
        
        # Ver datos
        if ver_datos:
            st.markdown("---")
            st.markdown("### 📊 Detalle de Deuda")
            
            # Preparar datos para mostrar
            datos_tabla = []
            total_fondo_general = 0
            total_mora_general = 0
            total_admin_general = 0
            
            for idx, row in datos_ruc.iterrows():
                fondo = row['FONDO_NOMINAL']
                admin = row['COMISION_NOMINAL']
                mora = row.get('MORA', 0)
                interes_admin = row['SEGURO_NOMINAL'] + row['AFP_NOMINAL']
                total_admin_row = admin + interes_admin
                deuda_con_mora = row['DEUDA_CON_MORA']
                
                datos_tabla.append({
                    'CUSSP': row['CUSSP'],
                    'Período': row['OPERACION'],
                    'Fondo': f"{fondo:.2f}",
                    'Mora': f"{mora:.2f}",
                    'Total Fondo': f"{deuda_con_mora:.2f}",
                    'Total Admin': f"{total_admin_row:.2f}",
                })
                
                total_fondo_general += deuda_con_mora
                total_mora_general += mora
                total_admin_general += total_admin_row
            
            df_datos = pd.DataFrame(datos_tabla)
            
            # Mostrar tabla de datos
            st.dataframe(df_datos, use_container_width=True, hide_index=True)
            
            # Mostrar fila de totales como texto grande y destacado
            col1, col2, col3, col4, col5, col6 = st.columns(6)
            with col1:
                st.metric("", "TOTAL", delta=None)
            with col2:
                st.metric("", "", delta=None)
            with col3:
                st.metric("", "", delta=None)
            with col4:
                st.metric("Mora Total", f"S/. {total_mora_general:.2f}")
            with col5:
                st.metric("Total Fondo", f"S/. {total_fondo_general:.2f}")
            with col6:
                st.metric("Total Admin", f"S/. {total_admin_general:.2f}")
    
    except Exception as e:
        st.error(f"❌ Error: {e}")

# ============================================================================
# BARRA LATERAL
# ============================================================================

with st.sidebar:
    st.markdown("## 📚 Información")
    
    st.markdown("### 🎯 Campañas Disponibles")
    campanas = {
        "PRESUNTA": "PRESUNTA",
        "DEUDA REAL TOTAL": "DEUDA REAL TOTAL",
        "REDIRECCIONAMIENTO": "REDIRECCIONAMIENTO",
        "PREJUDICIAL FLUJO": "PREJUDICIAL FLUJO"
    }
    for campana in campanas.values():
        casos = len([ruc for ruc in gen.obtener_rucs() if (ruc, campana) in gen.rucs_por_campana])
        st.write(f"• **{campana}**: {casos} casos")
    
    st.markdown("---")
    st.markdown("### 📊 Estadísticas")
    st.write(f"• **RUCs únicos**: {len(gen.obtener_rucs())}")
    st.write(f"• **Casos totales**: 9,137")
    st.write(f"• **Registros**: 460,843")
    st.write(f"• **Período**: 2008-2021")
    
    st.markdown("---")
    st.markdown("### ℹ️ Acerca de")
    st.info("""
    **Sistema de Liquidaciones WorldTel v2.0**
    
    Aplicación web para generación rápida de liquidaciones en PDF.
    
    - Interfaz intuitiva
    - Generación instantánea
    - PDF descargable
    - Multi-campaña
    """)
    
    st.markdown("---")
    st.markdown(f"*Actualizado: {datetime.now().strftime('%d/%m/%Y %H:%M')}*")
