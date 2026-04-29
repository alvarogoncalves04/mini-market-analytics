import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from src.config import DB_PATH

st.set_page_config(page_title="Análisis", page_icon="📈", layout="wide")

@st.cache_data
def cargar_datos():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM sales", conn)
    conn.close()
    df['sale_date'] = pd.to_datetime(df['sale_date'])
    df['dia_semana'] = df['sale_date'].dt.day_name()
    return df

df = cargar_datos()

st.title("📈 Análisis Detallado")

# Ventas por día de semana
st.subheader("📅 Ventas por Día de Semana")

orden_dias = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
nombres_dias = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']

ventas_dia = df.groupby('dia_semana')['total_sale'].sum().reindex(orden_dias).reset_index()
ventas_dia['dia_semana'] = nombres_dias

fig1 = px.bar(ventas_dia, x='dia_semana', y='total_sale', 
              title="Ventas por Día de Semana",
              labels={'dia_semana': 'Día', 'total_sale': 'Ventas (PLN)'},
              color='total_sale', color_continuous_scale='pinkyl')
fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig1, use_container_width=True)

# Distribución de precios
st.subheader("💰 Distribución de Precios")

fig2 = px.histogram(df, x='price', nbins=30, title="Frecuencia de Precios",
                    labels={'price': 'Precio (PLN)', 'count': 'Frecuencia'},
                    color_discrete_sequence=['#ff7eb3'])
fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig2, use_container_width=True)

# Top productos por cantidad
st.subheader("🏆 Top Categorías por Cantidad Vendida")

top_cantidad = df.groupby('category')['quantity'].sum().reset_index().sort_values('quantity', ascending=False)

fig3 = px.bar(top_cantidad, x='category', y='quantity', 
              title="Cantidad Vendida por Categoría",
              labels={'category': 'Categoría', 'quantity': 'Cantidad'},
              color='category', color_discrete_sequence=['#ff758c', '#ff7eb3', '#a8edea'])
fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig3, use_container_width=True)

# Ticket promedio por categoría
st.subheader("🎫 Ticket Promedio por Categoría")

ticket_categoria = df.groupby('category')['total_sale'].mean().reset_index()

fig4 = px.bar(ticket_categoria, x='category', y='total_sale',
              title="Ticket Promedio por Categoría",
              labels={'category': 'Categoría', 'total_sale': 'Ticket Promedio (PLN)'},
              color='category')
fig4.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig4, use_container_width=True)