import pandas as pd
from src.config import RAW_DATA_PATH, CHUNK_SIZE

def count_rows_in_csv():
    """Cuenta cuántas filas tiene el CSV sin cargarlo completo"""
    with open(RAW_DATA_PATH, 'r', encoding='utf-8') as f:
        return sum(1 for _ in f) - 1

def load_data_in_chunks():
    """Generador que devuelve el CSV en trozos de CHUNK_SIZE filas"""
    contador = 0
    total_filas = count_rows_in_csv()
    
    print(f"📂 Cargando archivo: {RAW_DATA_PATH.name}")
    print(f"📊 Total de filas: {total_filas:,}")
    
    for chunk in pd.read_csv(
        RAW_DATA_PATH,
        sep=';',               # El CSV usa punto y coma como separador
        encoding='utf-8',      # Codificación del texto
        chunksize=CHUNK_SIZE,  # Filas por cada trozo
        low_memory=False       # Evita warnings
    ):
        contador += len(chunk)
        print(f"✅ Procesado {contador:,} de {total_filas:,} filas")
        yield chunk  # Devuelve un trozo pero sigue recordando dónde iba
    
    print("🎉 Carga completada")