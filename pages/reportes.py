import streamlit as st
from datetime import datetime

def mostrar(df_filtrado):
    st.markdown("<h1>📅 Reportes Ejecutivos</h1>", unsafe_allow_html=True)
    
    df_filtrado['mes'] = df_filtrado['sale_date'].dt.strftime('%Y-%m')
    resumen = df_filtrado.groupby('mes').agg({
        'total_sale': 'sum',
        'quantity': 'sum'
    }).reset_index()
    resumen.columns = ['Mes', 'Ventas Totales', 'Unidades']
    st.dataframe(resumen, use_container_width=True)
    
    st.divider()
    
    top = df_filtrado.nlargest(10, 'total_sale')[['sale_date', 'total_sale', 'category']]
    st.dataframe(top, use_container_width=True)
    
    csv = df_filtrado.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Descargar CSV", csv, f"reporte_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")