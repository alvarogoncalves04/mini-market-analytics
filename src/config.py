import os
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"
RAW_DATA_PATH = DATA_DIR / "dataRSM.csv"
DB_PATH = ROOT_DIR / "mini_market.db"

CHUNK_SIZE = 50000

os.makedirs(DATA_DIR, exist_ok=True)