import streamlit as st
import plotly.express as px

def mostrar(df_filtrado):
    st.markdown("<h1>📈 Análisis Detallado</h1>", unsafe_allow_html=True)
    
    # Días de semana
    orden_dias = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    nombres_dias = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
    
    df_filtrado['dia_semana'] = df_filtrado['sale_date'].dt.day_name()
    ventas_dia = df_filtrado.groupby('dia_semana')['total_sale'].sum().reindex(orden_dias).reset_index()
    ventas_dia['dia_semana'] = nombres_dias
    
    fig = px.bar(ventas_dia, x='dia_semana', y='total_sale', title="Ventas por Día")
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.histogram(df_filtrado, x='price', nbins=30, title="Distribución de Precios")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        top = df_filtrado.groupby('category')['quantity'].sum().reset_index()
        fig = px.bar(top, x='category', y='quantity', title="Cantidad por Categoría")
        st.plotly_chart(fig, use_container_width=True)