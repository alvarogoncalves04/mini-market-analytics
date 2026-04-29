"""
DASHBOARD INTERACTIVO
Ejecutar con: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from src.config import DB_PATH

# Configuración de la página
st.set_page_config(
    page_title="Mini Market Analytics",
    page_icon="🏪",
    layout="wide"
)

# Título
st.title("🏪 Mini Market Analytics")
st.caption("Dashboard interactivo de datos reales de supermercado")

# ============================================
# CARGAR DATOS DESDE SQLITE
# ============================================
@st.cache_data
def cargar_datos():
    """Carga los datos desde la base de datos SQLite"""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM sales", conn)
    conn.close()
    return df

df = cargar_datos()

# ============================================
# MÉTRICAS PRINCIPALES
# ============================================
st.subheader("📊 Resumen General")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_ventas = df['total_sale'].sum()
    st.metric("💰 Ventas Totales", f"{total_ventas:,.2f} PLN")

with col2:
    num_transacciones = len(df)
    st.metric("📦 Número de Transacciones", f"{num_transacciones:,}")

with col3:
    precio_promedio = df['price'].mean()
    st.metric("💵 Precio Promedio", f"{precio_promedio:.2f} PLN")

with col4:
    cantidad_promedio = df['quantity'].mean()
    st.metric("📊 Cantidad Promedio", f"{cantidad_promedio:.1f} unidades")

# ============================================
# GRÁFICO DE VENTAS POR CATEGORÍA
# ============================================
st.subheader("📈 Ventas por Categoría")

ventas_categoria = df.groupby('category')['total_sale'].sum().reset_index()

fig1 = px.bar(
    ventas_categoria,
    x='category',
    y='total_sale',
    title="Total de Ventas por Categoría",
    labels={'category': 'Categoría', 'total_sale': 'Ventas (PLN)'},
    color='category'
)
st.plotly_chart(fig1, use_container_width=True)

# ============================================
# GRÁFICO DE VENTAS POR FECHA
# ============================================
st.subheader("📅 Tendencia de Ventas por Fecha")

# Convertir a fecha y agrupar
df['sale_date'] = pd.to_datetime(df['sale_date'])
ventas_fecha = df.groupby(df['sale_date'].dt.date)['total_sale'].sum().reset_index()

fig2 = px.line(
    ventas_fecha,
    x='sale_date',
    y='total_sale',
    title="Evolución de Ventas Diarias",
    labels={'sale_date': 'Fecha', 'total_sale': 'Ventas (PLN)'},
    markers=True
)
st.plotly_chart(fig2, use_container_width=True)

# ============================================
# TABLA DE DATOS
# ============================================
st.subheader("📋 Datos Detallados")

# Mostrar las primeras 100 filas
st.dataframe(df.head(100), use_container_width=True)

# ============================================
# PIE DE PÁGINA
# ============================================
st.divider()
st.caption("📊 Datos reales de supermercado - Dashboard creado con Streamlit")