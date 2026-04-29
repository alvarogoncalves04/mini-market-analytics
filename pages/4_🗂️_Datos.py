import streamlit as st
import pandas as pd
import sqlite3
from src.config import DB_PATH

st.set_page_config(page_title="Datos", page_icon="🗂️", layout="wide")

@st.cache_data
def cargar_datos():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM sales", conn)
    conn.close()
    df['sale_date'] = pd.to_datetime(df['sale_date'])
    return df

df = cargar_datos()

st.title("🗂️ Datos Completos")

# Mostrar estadísticas
st.subheader("📊 Estadísticas del Dataset")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total de Filas", f"{len(df):,}")

with col2:
    st.metric("Total de Columnas", len(df.columns))

with col3:
    st.metric("Rango de Fechas", f"{df['sale_date'].min().date()} a {df['sale_date'].max().date()}")

st.divider()

# Vista previa
st.subheader("🔍 Vista Previa (primeras 100 filas)")

st.dataframe(df.head(100).style.format({
    'price': '{:.2f}',
    'total_sale': '{:.2f}'
}), use_container_width=True, height=400)

# Búsqueda
st.subheader("🔎 Búsqueda Personalizada")

col_busq1, col_busq2 = st.columns(2)

with col_busq1:
    categoria_buscar = st.selectbox("Filtrar por categoría", ['Todas'] + sorted(df['category'].unique().tolist()))

with col_busq2:
    min_venta = st.number_input("Venta mínima (PLN)", min_value=0.0, value=0.0, step=10.0)

# Aplicar filtros
df_filtrado = df.copy()
if categoria_buscar != 'Todas':
    df_filtrado = df_filtrado[df_filtrado['category'] == categoria_buscar]
if min_venta > 0:
    df_filtrado = df_filtrado[df_filtrado['total_sale'] >= min_venta]

st.write(f"Mostrando {len(df_filtrado)} filas")

st.dataframe(df_filtrado.style.format({
    'price': '{:.2f}',
    'total_sale': '{:.2f}'
}), use_container_width=True, height=400)