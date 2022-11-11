import os
from pathlib import Path

DIR_PATH = Path(os.path.dirname(__file__))

files = [f for f in os.listdir(DIR_PATH) if f.endswith(".txt")]
DAYS_IMPLEMENTED = len(files)
