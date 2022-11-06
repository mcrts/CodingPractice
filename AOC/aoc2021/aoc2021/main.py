import importlib
import sys
import os
import shutil
from pathlib import Path

import subprocess

DIR_PATH = Path(os.path.dirname(__file__))
TEMPLATE_DIR = DIR_PATH / "template" / "day"
DAYS_IMPLEMENTED = 6
AOC_MODULES = {
    i: importlib.import_module(f"aoc2021.day{i:02d}.main")
    for i in range(1, DAYS_IMPLEMENTED + 1)
}


def boiler(args=sys.argv):
    daynum = int(args[1])
    src_path = TEMPLATE_DIR
    dst_path = DIR_PATH / f"day{daynum:02d}"
    shutil.copytree(src_path, dst_path, dirs_exist_ok=False)
    args = [
        "sed",
        "-i",
        f"""s/DAY = "01"/DAY = "{daynum:02d}"/g""",
        str(dst_path / "main.py"),
    ]
    subprocess.call(
        args,
        shell=False,
    )


def run(args=sys.argv):
    daynum = int(args[1])
    m = AOC_MODULES[daynum]
    inpath = m.INPATH
    print(f"Day {daynum:02d} - Part01 :", m.solver01.solve(inpath))
    print(f"Day {daynum:02d} - Part02 :", m.solver02.solve(inpath))
