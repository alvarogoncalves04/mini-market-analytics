import pandas as pd

def clean_chunk(df_chunk):
    """
    Limpia un trozo de datos.
    Recibe un DataFrame, devuelve el mismo DataFrame limpio.
    """
    
    # 1. Convertir la columna de fecha a datetime
    if 'time' in df_chunk.columns:
        df_chunk['time'] = pd.to_datetime(df_chunk['time'], errors='coerce')
        # Eliminar filas con fecha inválida
        df_chunk = df_chunk.dropna(subset=['time'])
    
    # 2. Convertir precios (coma a punto, texto a número)
    if 'prices' in df_chunk.columns:
        # Reemplazar coma por punto (ej: "3,05" → "3.05")
        df_chunk['prices'] = df_chunk['prices'].astype(str).str.replace(',', '.')
        # Convertir a número, errores se vuelven NaN
        df_chunk['prices'] = pd.to_numeric(df_chunk['prices'], errors='coerce')
        # Eliminar precios negativos o cero
        df_chunk = df_chunk[df_chunk['prices'] > 0]
    
    # 3. Convertir cantidades a número y filtrar
    if 'quantities' in df_chunk.columns:
        df_chunk['quantities'] = pd.to_numeric(df_chunk['quantities'], errors='coerce')
        # Eliminar cantidades negativas
        df_chunk = df_chunk[df_chunk['quantities'] > 0]
        # Eliminar cantidades imposibles (>10,000 unidades)
        df_chunk = df_chunk[df_chunk['quantities'] <= 10000]
    
    # 4. Calcular el total de la venta (precio × cantidad)
    if 'prices' in df_chunk.columns and 'quantities' in df_chunk.columns:
        df_chunk['total_sale'] = df_chunk['prices'] * df_chunk['quantities']
    
    return df_chunk