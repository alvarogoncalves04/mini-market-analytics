"""
Estilos CSS compartidos entre todas las páginas
"""

def get_base_styles(modo="dark"):
    """
    Devuelve los estilos CSS base
    modo: "dark" o "light"
    """
    
    if modo == "dark":
        fondo_gradiente = "linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%)"
        texto_principal = "#ffffff"
        texto_secundario = "#a0a0d0"
        tarjeta_bg = "rgba(255, 255, 255, 0.1)"
        tarjeta_border = "rgba(255, 255, 255, 0.2)"
        metric_gradient = "linear-gradient(135deg, #ffffff, #e0e0ff)"
    else:
        fondo_gradiente = "linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)"
        texto_principal = "#1a1a2e"
        texto_secundario = "#4a4a6a"
        tarjeta_bg = "rgba(255, 255, 255, 0.8)"
        tarjeta_border = "rgba(255, 255, 255, 0.5)"
        metric_gradient = "linear-gradient(135deg, #1a1a2e, #16213e)"
    
    return f"""
    <style>
        /* Fondo general */
        .stApp {{
            background: {fondo_gradiente};
        }}
        
        /* Ocultar el sidebar por defecto de Streamlit */
        [data-testid="stSidebar"] {{
            display: none;
        }}
        
        /* Sidebar personalizado fijo */
        .custom-sidebar {{
            position: fixed;
            left: 0;
            top: 0;
            width: 280px;
            height: 100vh;
            background: {tarjeta_bg};
            backdrop-filter: blur(15px);
            border-right: 1px solid {tarjeta_border};
            padding: 30px 20px;
            z-index: 999;
            transition: all 0.3s ease;
        }}
        
        /* Contenido principal (con margen para el sidebar) */
        .main-content {{
            margin-left: 280px;
            padding: 20px 30px;
        }}
        
        /* Tarjetas con efecto vidrio */
        .custom-card {{
            background: {tarjeta_bg};
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 20px;
            border: 1px solid {tarjeta_border};
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        
        .custom-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.5);
        }}
        
        /* Títulos */
        h1 {{
            background: linear-gradient(135deg, #ff758c, #ff7eb3);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 2.5em !important;
            font-weight: 700 !important;
        }}
        
        h2 {{
            color: {texto_principal};
            margin-bottom: 20px;
        }}
        
        h3 {{
            color: {texto_secundario};
        }}
        
        /* Métricas */
        .metric-label {{
            color: {texto_secundario};
            font-size: 0.85em;
            letter-spacing: 1px;
        }}
        
        .metric-value {{
            background: {metric_gradient};
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 2.2em !important;
            font-weight: 700 !important;
        }}
        
        /* Links del sidebar */
        .nav-link {{
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px 16px;
            margin: 8px 0;
            border-radius: 12px;
            color: {texto_principal};
            text-decoration: none;
            transition: all 0.2s ease;
            cursor: pointer;
        }}
        
        .nav-link:hover {{
            background: rgba(255, 255, 255, 0.15);
            transform: translateX(5px);
        }}
        
        .nav-link.active {{
            background: rgba(255, 117, 140, 0.2);
            border-left: 3px solid #ff758c;
        }}
        
        .nav-icon {{
            font-size: 1.3em;
        }}
        
        /* Botón toggle modo */
        .toggle-btn {{
            position: fixed;
            bottom: 20px;
            left: 20px;
            background: {tarjeta_bg};
            backdrop-filter: blur(10px);
            border: 1px solid {tarjeta_border};
            border-radius: 30px;
            padding: 10px 20px;
            cursor: pointer;
            z-index: 1000;
            transition: all 0.3s ease;
        }}
        
        .toggle-btn:hover {{
            transform: scale(1.05);
        }}
        
        /* Botón exportar PDF */
        .export-btn {{
            background: linear-gradient(135deg, #ff758c, #ff7eb3);
            border: none;
            border-radius: 30px;
            padding: 8px 20px;
            color: white;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        
        .export-btn:hover {{
            transform: scale(1.02);
            box-shadow: 0 5px 20px rgba(255, 117, 140, 0.4);
        }}
        
        /* Divisor */
        .custom-divider {{
            height: 2px;
            background: linear-gradient(90deg, transparent, #ff758c, #ff7eb3, transparent);
            margin: 30px 0;
        }}
        
        /* Filtros */
        .filters-card {{
            background: {tarjeta_bg};
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 15px 20px;
            margin-bottom: 20px;
            border: 1px solid {tarjeta_border};
        }}
    </style>
    """