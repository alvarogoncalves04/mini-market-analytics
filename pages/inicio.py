import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def mostrar(df_filtrado):
    st.markdown("<h1>🏪 Dashboard Principal</h1>", unsafe_allow_html=True)
    
    total_ventas = df_filtrado['total_sale'].sum()
    num_transacciones = len(df_filtrado)
    ticket_promedio = total_ventas / num_transacciones if num_transacciones > 0 else 0
    cantidad_promedio = df_filtrado['quantity'].mean()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💰 Ventas Totales", f"{total_ventas:,.2f} PLN")
    with col2:
        st.metric("📦 Transacciones", f"{num_transacciones:,}")
    with col3:
        st.metric("🎫 Ticket Promedio", f"{ticket_promedio:.2f} PLN")
    with col4:
        st.metric("🛒 Artículos x Venta", f"{cantidad_promedio:.1f}")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        ventas_categoria = df_filtrado.groupby('category')['total_sale'].sum().reset_index()
        fig = px.pie(ventas_categoria, values='total_sale', names='category', hole=0.4)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        ventas_fecha = df_filtrado.groupby(df_filtrado['sale_date'].dt.date)['total_sale'].sum().reset_index()
        fig = px.line(ventas_fecha, x='sale_date', y='total_sale', markers=True)
        st.plotly_chart(fig, use_container_width=True)