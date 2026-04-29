"""
Estilos CSS compartidos
"""

def get_styles(modo):
    """Devuelve los estilos CSS según el modo (dark/light)"""
    
    if modo == "dark":
        fondo = "linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%)"
        texto = "#ffffff"
        texto_sec = "#a0a0d0"
        tarjeta_bg = "rgba(255, 255, 255, 0.1)"
        tarjeta_border = "rgba(255, 255, 255, 0.2)"
        gradiente_metric = "linear-gradient(135deg, #ffffff, #e0e0ff)"
        sidebar_bg = "rgba(20, 15, 45, 0.8)"
    else:
        fondo = "linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)"
        texto = "#1a1a2e"
        texto_sec = "#4a4a6a"
        tarjeta_bg = "rgba(255, 255, 255, 0.8)"
        tarjeta_border = "rgba(255, 255, 255, 0.5)"
        gradiente_metric = "linear-gradient(135deg, #1a1a2e, #16213e)"
        sidebar_bg = "rgba(230, 230, 250, 0.9)"
    
    return f"""
    <style>
        /* Ocultar sidebar nativo de Streamlit */
        [data-testid="stSidebar"] {{
            display: none;
        }}
        
        /* Ocultar header nativo */
        header {{
            display: none;
        }}
        
        /* Fondo general */
        .stApp {{
            background: {fondo};
        }}
        
        /* Estilo para la columna del sidebar (primera columna) */
        [data-testid="column"]:first-child {{
            background: {sidebar_bg};
            backdrop-filter: blur(15px);
            border-radius: 0 20px 20px 0;
            margin: 10px 0;
            padding: 15px 10px;
            height: calc(100vh - 20px);
            position: sticky;
            top: 10px;
        }}
        
        /* Tarjetas */
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
        
        h1 {{
            background: linear-gradient(135deg, #ff758c, #ff7eb3);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 2.5em !important;
            font-weight: 700 !important;
        }}
        
        .metric-label {{
            color: {texto_sec};
            font-size: 0.85em;
            letter-spacing: 1px;
        }}
        
        .metric-value {{
            background: {gradiente_metric};
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 2.2em !important;
            font-weight: 700 !important;
        }}
        
        .custom-divider {{
            height: 2px;
            background: linear-gradient(90deg, transparent, #ff758c, #ff7eb3, transparent);
            margin: 30px 0;
        }}
        
        .filters-card {{
            background: {tarjeta_bg};
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 15px 20px;
            margin-bottom: 20px;
            border: 1px solid {tarjeta_border};
        }}
        
        /* Botones dentro del sidebar */
        [data-testid="column"]:first-child button {{
            background: transparent;
            border: 1px solid {tarjeta_border};
            border-radius: 12px;
            margin: 5px 0;
            transition: all 0.2s ease;
        }}
        
        [data-testid="column"]:first-child button:hover {{
            background: rgba(255, 255, 255, 0.15);
            transform: translateX(5px);
            border-color: #ff758c;
        }}
        
        p, div, span {{
            color: {texto};
        }}
        
        /* Ajustes de texto en sidebar */
        [data-testid="column"]:first-child p,
        [data-testid="column"]:first-child div,
        [data-testid="column"]:first-child span {{
            color: {texto};
        }}
    </style>
    """