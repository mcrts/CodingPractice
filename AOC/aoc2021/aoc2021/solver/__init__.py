import importlib
import os
from pathlib import Path

DIR_PATH = Path(os.path.dirname(__file__))

files = [f for f in os.listdir(DIR_PATH) if f.endswith(".py") and f.startswith("day")]
DAYS_IMPLEMENTED = len(files)

MODULES = {
    k: importlib.import_module(f".", package=f"aoc2021.solver.day{k:02d}")
    for k in range(1, DAYS_IMPLEMENTED + 1)
}

SOLVERS = {
    (day, part): m.solver01 if part == 1 else m.solver02
    for day, m in MODULES.items()
    for part in (1, 2)
}
