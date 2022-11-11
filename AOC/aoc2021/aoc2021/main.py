import sys
import os
import shutil
from pathlib import Path

from string import Template

from aoc2021.solver import SOLVERS, MODULES
from aoc2021.utils import input_path

DIR_PATH = Path(os.path.dirname(__file__))
TEMPLATE_DIR = DIR_PATH / "template"


def boiler(args=sys.argv):
    day = int(args[1])

    inpath = input_path(day)
    if not os.path.exists(inpath):
        open(inpath, "w").close()

    templatepath = TEMPLATE_DIR / "solver.py"
    solverpath = DIR_PATH / "solver" / f"day{day:02d}.py"
    if not os.path.exists(solverpath):
        with open(templatepath, "r") as inf, open(solverpath, "w") as outf:
            template = Template(inf.read())
            outf.write(template.safe_substitute({"DAY": day}))

    return sys.exit(0)

    if not os.path.exists(solverpath):
        open(solverpath, "w").close()


def run(args=sys.argv):
    day = int(args[1])
    MODULES[day].main()
