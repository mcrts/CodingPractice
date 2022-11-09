from . import day01, day02, day03, day04, day05, day06

DAYS_IMPLEMENTED = 6
SOLVERS = {
    (day, part): eval(f"day{day:02d}.solver{part:02d}")
    for day in range(1, DAYS_IMPLEMENTED + 1)
    for part in (1, 2)
}
