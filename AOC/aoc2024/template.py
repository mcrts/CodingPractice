import os
import shutil
import sys
from pathlib import Path

DIR = Path(os.path.dirname(os.path.realpath(__file__)))
TEMPLATE = DIR / "template_source.py"
FILES = DIR / "files"
TESTFILES = DIR / "files/test"


def main():
    day = int(sys.argv[1])
    shutil.copyfile(TEMPLATE, DIR / f"day{day:02}.py")
    open(FILES / f"day{day:02}.txt", "a").close()
    open(TESTFILES / f"day{day:02}.txt", "a").close()


if __name__ == "__main__":
    main()
