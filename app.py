"""
DASHBOARD ELEGANTE - Mini Market Analytics
Ejecutar con: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
from datetime import datetime
from src.config import DB_PATH

# ============================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================
st.set_page_config(
    page_title="Mini Market Analytics",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# INICIALIZAR ESTADO DE SESIÓN
# ============================================
if 'modo' not in st.session_state:
    st.session_state.modo = "dark"

if 'pagina' not in st.session_state:
    st.session_state.pagina = "inicio"

# ============================================
# FUNCIÓN PARA OBTENER ESTILOS CSS
# ============================================
def get_styles(modo):
    if modo == "dark":
        fondo = "linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%)"
        texto = "#ffffff"
        texto_sec = "#a0a0d0"
        tarjeta_bg = "rgba(255, 255, 255, 0.1)"
        tarjeta_border = "rgba(255, 255, 255, 0.2)"
        gradiente_metric = "linear-gradient(135deg, #ffffff, #e0e0ff)"
    else:
        fondo = "linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)"
        texto = "#1a1a2e"
        texto_sec = "#4a4a6a"
        tarjeta_bg = "rgba(255, 255, 255, 0.8)"
        tarjeta_border = "rgba(255, 255, 255, 0.5)"
        gradiente_metric = "linear-gradient(135deg, #1a1a2e, #16213e)"
    
    return f"""
    <style>
        /* Fondo general */
        .stApp {{
            background: {fondo};
        }}
        
        /* Ocultar sidebar nativo de Streamlit */
        [data-testid="stSidebar"] {{
            display: none;
        }}
        
        /* Sidebar personalizado fijo */
        .custom-sidebar {{
            position: fixed;
            left: 0;
            top: 0;
            width: 260px;
            height: 100vh;
            background: {tarjeta_bg};
            backdrop-filter: blur(15px);
            border-right: 1px solid {tarjeta_border};
            padding: 30px 15px;
            z-index: 999;
        }}
        
        /* Contenido principal */
        .main-content {{
            margin-left: 280px;
            padding: 20px 30px;
        }}
        
        /* Tarjetas con efecto vidrio */
        .custom-card {{
            background: {tarjeta_bg};
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 20px;
            border: 1px solid {tarjeta_border};
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        
        .custom-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.5);
        }}
        
        /* Títulos */
        h1 {{
            background: linear-gradient(135deg, #ff758c, #ff7eb3);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 2.5em !important;
            font-weight: 700 !important;
        }}
        
        h2 {{
            color: {texto};
            margin-bottom: 20px;
        }}
        
        /* Métricas */
        .metric-label {{
            color: {texto_sec};
            font-size: 0.85em;
            letter-spacing: 1px;
        }}
        
        .metric-value {{
            background: {gradiente_metric};
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 2.2em !important;
            font-weight: 700 !important;
        }}
        
        /* Navegación */
        .nav-link {{
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px 16px;
            margin: 8px 0;
            border-radius: 12px;
            color: {texto};
            text-decoration: none;
            cursor: pointer;
            transition: all 0.2s ease;
        }}
        
        .nav-link:hover {{
            background: rgba(255, 255, 255, 0.15);
            transform: translateX(5px);
        }}
        
        .nav-link.active {{
            background: rgba(255, 117, 140, 0.2);
            border-left: 3px solid #ff758c;
        }}
        
        .nav-icon {{
            font-size: 1.3em;
        }}
        
        /* Botón toggle */
        .toggle-btn {{
            position: fixed;
            bottom: 20px;
            left: 20px;
            background: {tarjeta_bg};
            backdrop-filter: blur(10px);
            border: 1px solid {tarjeta_border};
            border-radius: 30px;
            padding: 10px 18px;
            cursor: pointer;
            z-index: 1000;
            font-size: 0.9em;
            color: {texto};
        }}
        
        /* Botón exportar */
        .export-btn {{
            background: linear-gradient(135deg, #ff758c, #ff7eb3);
            border: none;
            border-radius: 30px;
            padding: 8px 20px;
            color: white;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        
        .export-btn:hover {{
            transform: scale(1.02);
            box-shadow: 0 5px 20px rgba(255, 117, 140, 0.4);
        }}
        
        /* Divisor */
        .custom-divider {{
            height: 2px;
            background: linear-gradient(90deg, transparent, #ff758c, #ff7eb3, transparent);
            margin: 30px 0;
        }}
        
        /* Filtros */
        .filters-card {{
            background: {tarjeta_bg};
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 15px 20px;
            margin-bottom: 20px;
            border: 1px solid {tarjeta_border};
        }}
    </style>
    """

# ============================================
# APLICAR ESTILOS
# ============================================
st.markdown(get_styles(st.session_state.modo), unsafe_allow_html=True)

# ============================================
# SIDEBAR FIJO (HTML)
# ============================================
sidebar_html = f"""
<div class="custom-sidebar">
    <div style="text-align: center; margin-bottom: 30px;">
        <span style="font-size: 3em;">🏪</span>
        <h3 style="margin: 10px 0 5px 0;">Mini Market</h3>
        <p style="color: #a0a0d0; font-size: 0.8em;">Analytics Dashboard</p>
    </div>
    
    <div>
        <div class="nav-link {'active' if st.session_state.pagina == 'inicio' else ''}" onclick="window.location.href='?page=inicio'">
            <span class="nav-icon">📊</span>
            <span>Inicio</span>
        </div>
        <div class="nav-link {'active' if st.session_state.pagina == 'analisis' else ''}" onclick="window.location.href='?page=analisis'">
            <span class="nav-icon">📈</span>
            <span>Análisis</span>
        </div>
        <div class="nav-link {'active' if st.session_state.pagina == 'reportes' else ''}" onclick="window.location.href='?page=reportes'">
            <span class="nav-icon">📅</span>
            <span>Reportes</span>
        </div>
        <div class="nav-link {'active' if st.session_state.pagina == 'datos' else ''}" onclick="window.location.href='?page=datos'">
            <span class="nav-icon">🗂️</span>
            <span>Datos</span>
        </div>
    </div>
</div>

<div class="toggle-btn" onclick="window.location.href='?toggle=modo'">
    {'🌙' if st.session_state.modo == 'dark' else '☀️'} 
    {'Modo Oscuro' if st.session_state.modo == 'light' else 'Modo Claro'}
</div>
"""

st.markdown(sidebar_html, unsafe_allow_html=True)

# ============================================
# MANEJAR PARÁMETROS DE URL
# ============================================
query_params = st.query_params

if 'toggle' in query_params and query_params['toggle'] == 'modo':
    st.session_state.modo = "light" if st.session_state.modo == "dark" else "dark"
    st.rerun()

if 'page' in query_params:
    st.session_state.pagina = query_params['page']

# ============================================
# CARGAR DATOS
# ============================================
@st.cache_data
def cargar_datos():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM sales", conn)
    conn.close()
    df['sale_date'] = pd.to_datetime(df['sale_date'])
    df['dia_semana'] = df['sale_date'].dt.day_name()
    df['mes'] = df['sale_date'].dt.strftime('%Y-%m')
    return df

df = cargar_datos()

# ============================================
# FILTROS GLOBALES
# ============================================
st.markdown('<div class="main-content">', unsafe_allow_html=True)

st.markdown('<div class="filters-card">', unsafe_allow_html=True)
col_f1, col_f2, col_f3 = st.columns(3)

with col_f1:
    fecha_min = df['sale_date'].min().date()
    fecha_max = df['sale_date'].max().date()
    rango_fechas = st.date_input(
        "📅 Rango de fechas",
        value=(fecha_min, fecha_max),
        min_value=fecha_min,
        max_value=fecha_max
    )

with col_f2:
    categorias = ['Todas'] + sorted(df['category'].unique().tolist())
    categoria_seleccionada = st.selectbox("🏷️ Categoría", categorias)

with col_f3:
    st.markdown('<div style="height: 28px;"></div>', unsafe_allow_html=True)
    if st.button("🔄 Actualizar Dashboard", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Aplicar filtros
df_filtrado = df.copy()
df_filtrado = df_filtrado[(df_filtrado['sale_date'].dt.date >= rango_fechas[0]) & 
                          (df_filtrado['sale_date'].dt.date <= rango_fechas[1])]

if categoria_seleccionada != 'Todas':
    df_filtrado = df_filtrado[df_filtrado['category'] == categoria_seleccionada]

# ============================================
# CONTENIDO SEGÚN PÁGINA SELECCIONADA
# ============================================

# ---------- PÁGINA INICIO ----------
if st.session_state.pagina == "inicio":
    st.markdown("<h1>🏪 Dashboard Principal</h1>", unsafe_allow_html=True)
    
    total_ventas = df_filtrado['total_sale'].sum()
    num_transacciones = len(df_filtrado)
    ticket_promedio = total_ventas / num_transacciones if num_transacciones > 0 else 0
    cantidad_promedio = df_filtrado['quantity'].mean()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="custom-card">
            <div style="display: flex; justify-content: space-between;">
                <span style="font-size: 2em;">💰</span>
                <span class="metric-label">Ventas Totales</span>
            </div>
            <div class="metric-value">{total_ventas:,.0f} PLN</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="custom-card">
            <div style="display: flex; justify-content: space-between;">
                <span style="font-size: 2em;">📦</span>
                <span class="metric-label">Transacciones</span>
            </div>
            <div class="metric-value">{num_transacciones:,}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="custom-card">
            <div style="display: flex; justify-content: space-between;">
                <span style="font-size: 2em;">🎫</span>
                <span class="metric-label">Ticket Promedio</span>
            </div>
            <div class="metric-value">{ticket_promedio:.2f} PLN</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="custom-card">
            <div style="display: flex; justify-content: space-between;">
                <span style="font-size: 2em;">🛒</span>
                <span class="metric-label">Artículos x Venta</span>
            </div>
            <div class="metric-value">{cantidad_promedio:.1f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)
    
    col_graf1, col_graf2 = st.columns(2)
    
    with col_graf1:
        ventas_categoria = df_filtrado.groupby('category')['total_sale'].sum().reset_index()
        fig1 = px.pie(ventas_categoria, values='total_sale', names='category', hole=0.4,
                      color_discrete_sequence=['#ff758c', '#ff7eb3', '#a8edea', '#fed6e3'])
        fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white')
        st.plotly_chart(fig1, use_container_width=True)
    
    with col_graf2:
        ventas_fecha = df_filtrado.groupby(df_filtrado['sale_date'].dt.date)['total_sale'].sum().reset_index()
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=ventas_fecha['sale_date'], y=ventas_fecha['total_sale'],
                                  mode='lines+markers', line=dict(color='#ff758c', width=3),
                                  fill='tozeroy', fillcolor='rgba(255, 117, 140, 0.2)'))
        fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white',
                           xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'))
        st.plotly_chart(fig2, use_container_width=True)

# ---------- PÁGINA ANÁLISIS ----------
elif st.session_state.pagina == "analisis":
    st.markdown("<h1>📈 Análisis Detallado</h1>", unsafe_allow_html=True)
    
    # Ventas por día de semana
    orden_dias = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    nombres_dias = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
    
    ventas_dia = df_filtrado.groupby('dia_semana')['total_sale'].sum().reindex(orden_dias).reset_index()
    ventas_dia['dia_semana'] = nombres_dias
    
    fig3 = px.bar(ventas_dia, x='dia_semana', y='total_sale', 
                  title="Ventas por Día de Semana",
                  labels={'dia_semana': 'Día', 'total_sale': 'Ventas (PLN)'},
                  color='total_sale', color_continuous_scale='pinkyl')
    fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white')
    st.plotly_chart(fig3, use_container_width=True)
    
    col_a1, col_a2 = st.columns(2)
    
    with col_a1:
        fig4 = px.histogram(df_filtrado, x='price', nbins=30, title="Distribución de Precios",
                            labels={'price': 'Precio (PLN)', 'count': 'Frecuencia'},
                            color_discrete_sequence=['#ff7eb3'])
        fig4.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white')
        st.plotly_chart(fig4, use_container_width=True)
    
    with col_a2:
        top_cantidad = df_filtrado.groupby('category')['quantity'].sum().reset_index()
        fig5 = px.bar(top_cantidad, x='category', y='quantity', 
                      title="Cantidad Vendida por Categoría",
                      labels={'category': 'Categoría', 'quantity': 'Cantidad'},
                      color='category', color_discrete_sequence=['#ff758c', '#ff7eb3', '#a8edea'])
        fig5.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white')
        st.plotly_chart(fig5, use_container_width=True)

# ---------- PÁGINA REPORTES ----------
elif st.session_state.pagina == "reportes":
    st.markdown("<h1>📅 Reportes Ejecutivos</h1>", unsafe_allow_html=True)
    
    # Resumen mensual
    st.markdown("<h3>📊 Resumen Mensual</h3>", unsafe_allow_html=True)
    resumen_mensual = df_filtrado.groupby('mes').agg({
        'total_sale': ['sum', 'mean', 'count'],
        'quantity': 'sum'
    }).reset_index()
    resumen_mensual.columns = ['Mes', 'Ventas Totales', 'Ticket Promedio', 'Transacciones', 'Unidades']
    resumen_mensual['Ventas Totales'] = resumen_mensual['Ventas Totales'].round(2)
    resumen_mensual['Ticket Promedio'] = resumen_mensual['Ticket Promedio'].round(2)
    st.dataframe(resumen_mensual, use_container_width=True)
    
    st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)
    
    # Top transacciones
    st.markdown("<h3>🏆 Top 10 Transacciones por Monto</h3>", unsafe_allow_html=True)
    top_transacciones = df_filtrado.nlargest(10, 'total_sale')[['sale_date', 'price', 'quantity', 'total_sale', 'category']]
    top_transacciones = top_transacciones.round(2)
    st.dataframe(top_transacciones, use_container_width=True)
    
    # Exportar CSV
    st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)
    csv = df_filtrado.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Descargar Reporte (CSV)", data=csv, file_name=f"reporte_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv")

# ---------- PÁGINA DATOS ----------
elif st.session_state.pagina == "datos":
    st.markdown("<h1>🗂️ Datos Completos</h1>", unsafe_allow_html=True)
    
    st.dataframe(df_filtrado[['sale_date', 'price', 'quantity', 'total_sale', 'category']].style.format({
        'price': '{:.2f}',
        'total_sale': '{:.2f}'
    }), use_container_width=True, height=500)

st.markdown('</div>', unsafe_allow_html=True)