import streamlit as st
import pandas as pd
import sqlite3
from src.config import DB_PATH

st.set_page_config(page_title="Reportes", page_icon="📅", layout="wide")

@st.cache_data
def cargar_datos():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM sales", conn)
    conn.close()
    df['sale_date'] = pd.to_datetime(df['sale_date'])
    df['mes'] = df['sale_date'].dt.strftime('%Y-%m')
    return df

df = cargar_datos()

st.title("📅 Reportes Ejecutivos")

# Resumen mensual
st.subheader("📊 Resumen Mensual")

resumen_mensual = df.groupby('mes').agg({
    'total_sale': ['sum', 'mean', 'count'],
    'quantity': 'sum'
}).reset_index()

resumen_mensual.columns = ['Mes', 'Ventas Totales', 'Ticket Promedio', 'Transacciones', 'Unidades Vendidas']
resumen_mensual['Ventas Totales'] = resumen_mensual['Ventas Totales'].round(2)
resumen_mensual['Ticket Promedio'] = resumen_mensual['Ticket Promedio'].round(2)

st.dataframe(resumen_mensual, use_container_width=True)

# Top transacciones
st.subheader("🏆 Top 10 Transacciones por Monto")

top_transacciones = df.nlargest(10, 'total_sale')[['sale_date', 'price', 'quantity', 'total_sale', 'category']]
top_transacciones = top_transacciones.round(2)
top_transacciones.columns = ['Fecha', 'Precio Unitario', 'Cantidad', 'Total Venta', 'Categoría']

st.dataframe(top_transacciones, use_container_width=True)

# Resumen por categoría
st.subheader("📈 Resumen por Categoría")

resumen_categoria = df.groupby('category').agg({
    'total_sale': 'sum',
    'quantity': 'sum',
    'price': 'mean'
}).reset_index()

resumen_categoria.columns = ['Categoría', 'Ventas Totales', 'Unidades Vendidas', 'Precio Promedio']
resumen_categoria['Ventas Totales'] = resumen_categoria['Ventas Totales'].round(2)
resumen_categoria['Precio Promedio'] = resumen_categoria['Precio Promedio'].round(2)

st.dataframe(resumen_categoria, use_container_width=True)

# Exportar datos (CSV)
st.subheader("📥 Exportar Datos")

csv = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📄 Descargar datos completos (CSV)",
    data=csv,
    file_name="reporte_ventas.csv",
    mime="text/csv",
)