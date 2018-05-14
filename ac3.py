import itertools
from typing import Dict, Tuple, Set

from sudoku import Sudoku


def ac3(sudoku: Sudoku, domains: dict):
    all_variables = sudoku.all_variables
    queue = list(itertools.permutations(all_variables, 2))

    domains_changed = False
    while queue:
        variable1, variable2 = queue.pop()
        if _revise(sudoku, domains, variable1, variable2):
            domains_changed = True

            if not domains[variable1]:
                return None, domains_changed

            for variable3 in sudoku.compute_neighbors(variable1):
                if variable3 != variable2:
                    queue.append((variable3, variable1))

    return domains, domains_changed


def _revise(sudoku: Sudoku, domains: Dict[Tuple, Set], variable1, variable2):
    to_remove = set()

    for value1 in domains[variable1]:
        satisfiable = False
        for value2 in domains[variable2]:
            if not sudoku.pair_has_conflict(variable1, value1, variable2, value2):
                satisfiable = True
                break

        if not satisfiable:
            to_remove.add(value1)

    domains[variable1] -= to_remove

    return len(to_remove) > 0
