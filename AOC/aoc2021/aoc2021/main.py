import sys
import os
import shutil
from pathlib import Path

import subprocess

from aoc2021.solver import SOLVERS
from aoc2021.utils import input_path

DIR_PATH = Path(os.path.dirname(__file__))
TEMPLATE_DIR = DIR_PATH / "template" / "day"


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
    inpath = input_path(daynum)
    solver01 = SOLVERS[(daynum, 1)]
    solver02 = SOLVERS[(daynum, 2)]
    print(f"Day {daynum:02d} - Part01 :", solver01.solve(inpath))
    print(f"Day {daynum:02d} - Part02 :", solver02.solve(inpath))
