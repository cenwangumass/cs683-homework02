from typing import Callable

from sudoku import Sudoku


def random_next_variable(sudoku: Sudoku):
    return next(iter(sudoku.unassigned_variables))


def minimum_remaining_values(sudoku: Sudoku):
    min_variable = None
    min_n = None
    for variable in sudoku.unassigned_variables:
        n = sudoku.compute_remaining_values(variable)
        if min_n is None or n < min_n:
            min_variable = variable
            min_n = n
    return min_variable


def backtracking(sudoku, next_variable_heuristic=None):
    domains = {
        variable: range(1, 10)
        for variable in sudoku.unassigned_variables
    }

    if next_variable_heuristic is None:
        next_variable_heuristic = random_next_variable

    success, statistics = _backtracking(sudoku, domains,
                                        next_variable_heuristic, {'n': 0})
    return statistics


def _backtracking(sudoku: Sudoku,
                  domains: dict,
                  next_variable_heuristic: Callable,
                  statistics: dict = None) -> (bool, dict):
    if sudoku.is_complete():
        return True, statistics

    variable = next_variable_heuristic(sudoku)
    domain = domains[variable]
    if not domain:
        return False, statistics

    statistics['n'] += len(domain) - 1

    for value in domain:
        if not sudoku.has_conflict(variable, value):
            sudoku.assign(variable, value)
            success, statistics = _backtracking(
                sudoku, domains, next_variable_heuristic, statistics)
            if success:
                return success, statistics
            else:
                sudoku.undo(variable)

    return False, statistics
