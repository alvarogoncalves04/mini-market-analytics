import sqlite3
from src.config import DB_PATH

def init_database():
    """
    Crea la base de datos y las tablas si no existen.
    Ejecutar UNA SOLA VEZ al inicio.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Crear la tabla de ventas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_date DATE,
            price REAL,
            quantity INTEGER,
            total_sale REAL,
            category TEXT
        )
    ''')
    
    # Crear índices para búsquedas rápidas
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_date ON sales(sale_date)')
    
    conn.commit()
    conn.close()
    print("✅ Base de datos inicializada")

def save_chunk_to_db(df_chunk):
    """
    Guarda un trozo de datos limpios en la base de datos
    """
    if len(df_chunk) == 0:
        return 0
    
    conn = sqlite3.connect(DB_PATH)
    
    # Seleccionar solo las columnas que necesitamos
    df_to_save = df_chunk[['time', 'prices', 'quantities', 'total_sale', 'category']].copy()
    
    # Renombrar columnas para que coincidan con la tabla
    df_to_save = df_to_save.rename(columns={
        'time': 'sale_date',
        'prices': 'price',
        'quantities': 'quantity'
    })
    
    # Guardar en la tabla
    df_to_save.to_sql('sales', conn, if_exists='append', index=False)
    
    conn.close()
    return len(df_to_save)