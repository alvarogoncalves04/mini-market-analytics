"""
Funciones para cargar y filtrar datos
"""

import pandas as pd
import sqlite3
import streamlit as st
from src.config import DB_PATH

@st.cache_data
def cargar_datos():
    """Carga los datos desde SQLite"""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM sales", conn)
    conn.close()
    df['sale_date'] = pd.to_datetime(df['sale_date'])
    df['dia_semana'] = df['sale_date'].dt.day_name()
    df['mes'] = df['sale_date'].dt.strftime('%Y-%m')
    return df

def aplicar_filtros(df, rango_fechas, categoria):
    """Aplica filtros de fecha y categoría"""
    df_filtrado = df.copy()
    df_filtrado = df_filtrado[
        (df_filtrado['sale_date'].dt.date >= rango_fechas[0]) & 
        (df_filtrado['sale_date'].dt.date <= rango_fechas[1])
    ]
    if categoria != 'Todas':
        df_filtrado = df_filtrado[df_filtrado['category'] == categoria]
    return df_filtrado

def calcular_metricas(df):
    """Calcula las métricas principales"""
    total_ventas = df['total_sale'].sum()
    num_transacciones = len(df)
    ticket_promedio = total_ventas / num_transacciones if num_transacciones > 0 else 0
    cantidad_promedio = df['quantity'].mean()
    return total_ventas, num_transacciones, ticket_promedio, cantidad_promedio