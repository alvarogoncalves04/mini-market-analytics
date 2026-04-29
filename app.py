"""
DASHBOARD PRINCIPAL - Mini Market Analytics
Ejecutar con: streamlit run app.py
"""

import streamlit as st
from utils.styles import get_styles
from utils.data import cargar_datos, aplicar_filtros
from pages import mostrar_inicio, mostrar_analisis, mostrar_reportes, mostrar_datos

# Configuración
st.set_page_config(
    page_title="Mini Market Analytics",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inicializar estado
if 'modo' not in st.session_state:
    st.session_state.modo = "dark"
if 'pagina' not in st.session_state:
    st.session_state.pagina = "inicio"

# Aplicar estilos
st.markdown(get_styles(st.session_state.modo), unsafe_allow_html=True)

# ============================================
# SIDEBAR CON COLUMNAS (sin HTML)
# ============================================
# Creamos un contenedor vacío en la izquierda usando columnas
col_sidebar, col_main = st.columns([1, 5])

with col_sidebar:
    st.markdown("""
    <div style="padding: 20px 10px;">
        <div style="text-align: center; margin-bottom: 30px;">
            <span style="font-size: 3em;">🏪</span>
            <h3 style="margin: 10px 0 5px 0;">Mini Market</h3>
            <p style="color: #a0a0d0; font-size: 0.8em;">Analytics</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Botones de navegación
    if st.button("📊 Inicio", use_container_width=True, key="btn_inicio"):
        st.session_state.pagina = "inicio"
        st.rerun()
    
    if st.button("📈 Análisis", use_container_width=True, key="btn_analisis"):
        st.session_state.pagina = "analisis"
        st.rerun()
    
    if st.button("📅 Reportes", use_container_width=True, key="btn_reportes"):
        st.session_state.pagina = "reportes"
        st.rerun()
    
    if st.button("🗂️ Datos", use_container_width=True, key="btn_datos"):
        st.session_state.pagina = "datos"
        st.rerun()
    
    st.markdown("---")
    
    # Modo oscuro/claro
    if st.button("🌓 " + ("Modo Claro" if st.session_state.modo == "dark" else "Modo Oscuro"), use_container_width=True):
        st.session_state.modo = "light" if st.session_state.modo == "dark" else "dark"
        st.rerun()
    
    st.markdown("---")
    st.caption("✨ Dashboard")
    st.caption("📊 Datos reales")

# ============================================
# CONTENIDO PRINCIPAL
# ============================================
with col_main:
    # Cargar datos
    df = cargar_datos()
    
    # Filtros
    st.markdown('<div class="filters-card">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        fecha_min = df['sale_date'].min().date()
        fecha_max = df['sale_date'].max().date()
        rango_fechas = st.date_input("📅 Rango de fechas", value=(fecha_min, fecha_max))
    
    with col2:
        categorias = ['Todas'] + sorted(df['category'].unique().tolist())
        categoria = st.selectbox("🏷️ Categoría", categorias)
    
    with col3:
        st.markdown('<div style="height: 28px;"></div>', unsafe_allow_html=True)
        if st.button("🔄 Actualizar", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Aplicar filtros
    df_filtrado = aplicar_filtros(df, rango_fechas, categoria)
    
    # Mostrar página seleccionada
    if st.session_state.pagina == "inicio":
        mostrar_inicio(df_filtrado)
    elif st.session_state.pagina == "analisis":
        mostrar_analisis(df_filtrado)
    elif st.session_state.pagina == "reportes":
        mostrar_reportes(df_filtrado)
    elif st.session_state.pagina == "datos":
        mostrar_datos(df_filtrado)