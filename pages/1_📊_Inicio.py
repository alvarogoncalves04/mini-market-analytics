import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
from src.config import DB_PATH

st.set_page_config(page_title="Inicio", page_icon="📊", layout="wide")

@st.cache_data
def cargar_datos():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM sales", conn)
    conn.close()
    df['sale_date'] = pd.to_datetime(df['sale_date'])
    return df

df = cargar_datos()

st.title("📊 Dashboard Principal")

# Métricas
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("💰 Ventas Totales", f"{df['total_sale'].sum():,.0f} PLN")

with col2:
    st.metric("📦 Transacciones", f"{len(df):,}")

with col3:
    st.metric("🎫 Ticket Promedio", f"{df['total_sale'].mean():.2f} PLN")

with col4:
    st.metric("🛒 Artículos x Venta", f"{df['quantity'].mean():.1f}")

st.divider()

# Gráficos
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    ventas_categoria = df.groupby('category')['total_sale'].sum().reset_index()
    fig1 = px.pie(ventas_categoria, values='total_sale', names='category', hole=0.4,
                  color_discrete_sequence=['#ff758c', '#ff7eb3', '#a8edea', '#fed6e3'])
    fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig1, use_container_width=True)

with col_graf2:
    ventas_fecha = df.groupby(df['sale_date'].dt.date)['total_sale'].sum().reset_index()
    fig2 = px.line(ventas_fecha, x='sale_date', y='total_sale', markers=True,
                   title="Evolución de Ventas", labels={'sale_date': 'Fecha', 'total_sale': 'Ventas'})
    fig2.update_traces(line_color='#ff758c')
    fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig2, use_container_width=True)