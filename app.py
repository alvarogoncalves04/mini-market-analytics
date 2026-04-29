"""
DASHBOARD PRINCIPAL - Mini Market Analytics
Ejecutar con: streamlit run app.py

Las páginas están en la carpeta pages/
- 1_📊_Inicio.py
- 2_📈_Analisis.py
- 3_📅_Reportes.py
- 4_🗂️_Datos.py
"""

import streamlit as st

# Configuración de la página principal
st.set_page_config(
    page_title="Mini Market Analytics",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título de bienvenida
st.title("🏪 Mini Market Analytics")

st.markdown("""
<div style="text-align: center; padding: 40px 20px;">
    <h2>Bienvenido al Dashboard</h2>
    <p style="font-size: 1.2em; color: #666;">
        Selecciona una página en el menú lateral para comenzar
    </p>
    <div style="margin-top: 40px;">
        <span style="font-size: 3em;">📊</span>
        <span style="font-size: 3em;">📈</span>
        <span style="font-size: 3em;">📅</span>
        <span style="font-size: 3em;">🗂️</span>
    </div>
    <div style="margin-top: 60px; padding: 20px; background: #f0f2f6; border-radius: 10px;">
        <h3>📌 ¿Qué encontrarás?</h3>
        <ul style="text-align: left; max-width: 400px; margin: 0 auto;">
            <li><strong>📊 Inicio</strong> - Métricas clave y gráficos principales</li>
            <li><strong>📈 Análisis</strong> - Ventas por día, distribución de precios</li>
            <li><strong>📅 Reportes</strong> - Resúmenes mensuales y top transacciones</li>
            <li><strong>🗂️ Datos</strong> - Tabla completa y búsqueda personalizada</li>
        </ul>
    </div>
</div>
""", unsafe_allow_html=True)

# Pie de página
st.divider()
st.caption("🏪 Mini Market Analytics | Datos reales de supermercado | Dashboard interactivo")