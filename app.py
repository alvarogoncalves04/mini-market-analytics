"""
DASHBOARD INTERACTIVO - VERSIÓN ELEGANTE
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
# CONFIGURACIÓN DE LA PÁGINA (debe ser lo primero)
# ============================================
st.set_page_config(
    page_title="Mini Market Analytics",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# CSS PERSONALIZADO (diseño elegante)
# ============================================
st.markdown("""
<style>
    /* Fondo general con gradiente */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }
    
    /* Tarjetas con efecto vidrio */
    .custom-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .custom-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.5);
    }
    
    /* Títulos */
    h1 {
        background: linear-gradient(135deg, #ffe6f0, #ffb3c6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3em !important;
        font-weight: 700 !important;
    }
    
    /* Subtítulos */
    .custom-subtitle {
        color: #a0a0d0;
        font-size: 1.1em;
        margin-bottom: 30px;
    }
    
    /* Métricas */
    .metric-label {
        color: #c0c0e0;
        font-size: 0.9em;
        letter-spacing: 1px;
    }
    
    .metric-value {
        background: linear-gradient(135deg, #ffffff, #e0e0ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5em !important;
        font-weight: 700 !important;
    }
    
    /* Sidebar elegante */
    [data-testid="stSidebar"] {
        background: rgba(15, 12, 41, 0.9);
        backdrop-filter: blur(12px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Botones */
    .stButton > button {
        background: linear-gradient(135deg, #ff758c, #ff7eb3);
        border: none;
        border-radius: 30px;
        color: white;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 5px 20px rgba(255, 117, 140, 0.4);
    }
    
    /* Divider personalizado */
    .custom-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #ff758c, #ff7eb3, transparent);
        margin: 30px 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# ENCABEZADO
# ============================================
col_logo, col_title = st.columns([1, 5])

with col_logo:
    st.markdown("<h1 style='font-size: 3em;'>🏪</h1>", unsafe_allow_html=True)

with col_title:
    st.markdown("<h1>Mini Market Analytics</h1>", unsafe_allow_html=True)
    st.markdown("<p class='custom-subtitle'>Dashboard inteligente con datos reales de supermercado</p>", unsafe_allow_html=True)

st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)

# ============================================
# CARGAR DATOS (con caché)
# ============================================
@st.cache_data
def cargar_datos():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM sales", conn)
    conn.close()
    
    # Convertir fecha
    df['sale_date'] = pd.to_datetime(df['sale_date'])
    df['mes'] = df['sale_date'].dt.strftime('%B')
    df['dia_semana'] = df['sale_date'].dt.day_name()
    
    return df

df = cargar_datos()

# ============================================
# MÉTRICAS PRINCIPALES (en tarjetas elegantes)
# ============================================
st.markdown("<h2 style='color: #e0e0ff; margin-bottom: 20px;'>📊 Resumen Ejecutivo</h2>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

def metric_card(col, label, value, delta=None, icon="📈"):
    with col:
        st.markdown(f"""
        <div class='custom-card'>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <span style='font-size: 2em;'>{icon}</span>
                <span class='metric-label'>{label}</span>
            </div>
            <div class='metric-value'>{value}</div>
        </div>
        """, unsafe_allow_html=True)

total_ventas = df['total_sale'].sum()
num_transacciones = len(df)
precio_promedio = df['price'].mean()
cantidad_promedio = df['quantity'].mean()

metric_card(col1, "Ventas Totales", f"{total_ventas:,.0f} PLN", icon="💰")
metric_card(col2, "Transacciones", f"{num_transacciones:,}", icon="📦")
metric_card(col3, "Ticket Promedio", f"{total_ventas/num_transacciones:.2f} PLN", icon="🎫")
metric_card(col4, "Artículos x Venta", f"{cantidad_promedio:.1f}", icon="🛒")

st.markdown("<br>", unsafe_allow_html=True)

# ============================================
# GRÁFICOS INTERACTIVOS (estilo moderno)
# ============================================
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.markdown("#### 🥧 Ventas por Categoría")
    
    ventas_categoria = df.groupby('category')['total_sale'].sum().reset_index()
    
    fig1 = px.pie(
        ventas_categoria,
        values='total_sale',
        names='category',
        hole=0.4,
        color_discrete_sequence=['#ff758c', '#ff7eb3', '#a8edea', '#fed6e3']
    )
    fig1.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2)
    )
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_graf2:
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.markdown("#### 📈 Evolución de Ventas")
    
    ventas_fecha = df.groupby(df['sale_date'].dt.date)['total_sale'].sum().reset_index()
    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=ventas_fecha['sale_date'],
        y=ventas_fecha['total_sale'],
        mode='lines+markers',
        line=dict(color='#ff758c', width=3),
        marker=dict(size=6, color='#ff7eb3'),
        fill='tozeroy',
        fillcolor='rgba(255, 117, 140, 0.2)'
    ))
    fig2.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================
# SEGUNDA FILA DE GRÁFICOS
# ============================================
col_graf3, col_graf4 = st.columns(2)

with col_graf3:
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.markdown("#### 📊 Top 10 de Cantidades")
    
    top_cantidades = df.nlargest(10, 'quantity')[['quantity', 'total_sale']].reset_index(drop=True)
    
    fig3 = px.bar(
        top_cantidades,
        x=top_cantidades.index,
        y='quantity',
        title="Mayores cantidades por transacción",
        labels={'x': 'Transacción', 'quantity': 'Cantidad'},
        color='total_sale',
        color_continuous_scale='pinkyl'
    )
    fig3.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='white'
    )
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_graf4:
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.markdown("#### 📊 Distribución de Precios")
    
    fig4 = px.histogram(
        df,
        x='price',
        nbins=30,
        title="Frecuencia de precios",
        labels={'price': 'Precio (PLN)', 'count': 'Frecuencia'},
        color_discrete_sequence=['#ff7eb3']
    )
    fig4.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        bargap=0.05
    )
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================
# TABLA DE DATOS (elegante)
# ============================================
st.markdown("""
<div class='custom-card' style='margin-top: 20px;'>
    <h3 style='margin-bottom: 20px;'>📋 Datos Recientes</h3>
</div>
""", unsafe_allow_html=True)

# Mostrar últimas 50 transacciones
st.dataframe(
    df[['sale_date', 'price', 'quantity', 'total_sale', 'category']].tail(50).style.format({
        'price': '{:.2f}',
        'total_sale': '{:.2f}'
    }),
    use_container_width=True,
    height=400
)

# ============================================
# PIE DE PÁGINA
# ============================================
st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)

col_footer1, col_footer2, col_footer3 = st.columns(3)
with col_footer1:
    st.markdown("<p style='color: #8080a0; text-align: center;'>📊 Datos reales de supermercado</p>", unsafe_allow_html=True)
with col_footer2:
    st.markdown("<p style='color: #8080a0; text-align: center;'>🏪 Mini Market Analytics</p>", unsafe_allow_html=True)
with col_footer3:
    st.markdown("<p style='color: #8080a0; text-align: center;'>✨ Dashboard interactivo</p>", unsafe_allow_html=True)

st.markdown("<p style='color: #606080; text-align: center; font-size: 0.8em; margin-top: 20px;'>Desarrollado con Streamlit, Plotly y Python</p>", unsafe_allow_html=True)