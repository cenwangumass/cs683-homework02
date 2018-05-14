import copy

from sudoku import Sudoku


def _run_waterfall(waterfall, sudoku, domains):
    while True:
        changed = False

        for inference in waterfall:
            domains, domains_changed = inference(sudoku, domains)
            if domains is None:
                return

            if domains_changed:
                changed = True

        if not changed:
            break

    return domains


def _initialize_domains(sudoku: Sudoku):
    domains = {}

    for variable in sudoku.assigned_variables:
        i, j = variable
        domains[variable] = {sudoku.data[i][j]}
    for variable in sudoku.unassigned_variables:
        domains[variable] = set(range(1, 10))

    return domains


def backtracking_with_waterfall(sudoku, waterfall=None):
    domains = _initialize_domains(sudoku)
    _run_waterfall(waterfall, sudoku, domains)
    success, statistics = _backtracking(sudoku, domains, waterfall, {'n': 0})
    return statistics


def _backtracking(sudoku: Sudoku,
                  domains: dict,
                  waterfall,
                  statistics: dict = None) -> (bool, dict):
    if sudoku.is_complete():
        return True, statistics

    min_variable = None
    min_n = None
    for variable in domains:
        if variable in sudoku.unassigned_variables:
            n = len(domains[variable])
            if n == 1:
                min_variable = variable
                break
            elif min_n is None or n < min_n:
                min_variable = variable
                min_n = n
    variable = min_variable

    domain = domains[variable]
    if not domain:
        return False, statistics

    statistics['n'] += len(domain) - 1

    for value in domain:
        if not sudoku.has_conflict(variable, value):
            sudoku.assign(variable, value)

            updated_domains = copy.deepcopy(domains)
            updated_domains[variable] = {value}

            updated_domains = _run_waterfall(waterfall, sudoku, updated_domains)

            if updated_domains is None:
                sudoku.undo(variable)
            else:
                success, statistics = _backtracking(sudoku, updated_domains,
                                                    waterfall, statistics)
                if success:
                    return success, statistics
                else:
                    sudoku.undo(variable)

    return False, statistics
