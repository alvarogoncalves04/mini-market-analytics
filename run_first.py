"""
SCRIPT PRINCIPAL - Ejecutar UNA SOLA VEZ
Procesa el CSV y guarda los datos limpios en SQLite
"""

import sys
import time
from pathlib import Path

# Agregar la carpeta actual al path para poder importar 'src'
sys.path.insert(0, str(Path(__file__).parent))

from src.config import RAW_DATA_PATH
from src.data_loader import load_data_in_chunks
from src.data_cleaner import clean_chunk
from src.database import init_database, save_chunk_to_db

def main():
    print("=" * 50)
    print("🏪 MINI MARKET ANALYTICS")
    print("Procesando datos...")
    print("=" * 50)
    
    # 1. Verificar que el CSV existe
    if not RAW_DATA_PATH.exists():
        print(f"❌ ERROR: No se encuentra el archivo")
        print(f"   Buscado en: {RAW_DATA_PATH}")
        print("   Asegúrate de tener 'dataRSM.csv' en la carpeta 'data/'")
        return
    
    print(f"✅ Archivo encontrado")
    
    # 2. Inicializar la base de datos
    print("\n📁 Inicializando base de datos...")
    init_database()
    
    # 3. Procesar el CSV en trozos
    print("\n🔄 Procesando datos...")
    inicio = time.time()
    total_guardadas = 0
    chunk_num = 0
    
    for chunk in load_data_in_chunks():
        chunk_num += 1
        print(f"\n--- Trozo #{chunk_num} ---")
        
        # Limpiar el trozo
        chunk_limpio = clean_chunk(chunk)
        
        # Guardar en base de datos
        filas_guardadas = save_chunk_to_db(chunk_limpio)
        total_guardadas += filas_guardadas
        print(f"   💾 Guardadas {filas_guardadas} filas")
    
    # 4. Resumen final
    tiempo_total = time.time() - inicio
    
    print("\n" + "=" * 50)
    print("🎉 ¡PROCESO COMPLETADO! 🎉")
    print("=" * 50)
    print(f"📊 Total de filas guardadas: {total_guardadas:,}")
    print(f"⏱️ Tiempo total: {tiempo_total:.2f} segundos")
    print(f"💾 Base de datos: {RAW_DATA_PATH.parent.parent / 'mini_market.db'}")
    print("=" * 50)
    print("\n✅ Ahora puedes ejecutar el dashboard con:")
    print("   streamlit run app.py")
    print("=" * 50)

if __name__ == "__main__":
    main()