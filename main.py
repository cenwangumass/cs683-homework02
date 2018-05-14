import json

from sudoku import Sudoku
from backtracking import backtracking, minimum_remaining_values
from backtracking_with_waterfall import backtracking_with_waterfall
from ac3 import ac3
from naked_pairs import naked_pairs


def get_statistics_text(sudoku_id, statistics):
    n = statistics['n']
    plural = 'guesses' if n > 1 else 'guess'
    verb = 'are' if n > 1 else 'is'
    return f"Sudoku {sudoku_id}: {n} {plural} {verb} made"


def main():
    with open('sudokus.json') as f:
        sudokus = json.load(f)

    # print('Backtracking')
    # for sudoku_id, string in sudokus.items():
    #     sudoku = Sudoku.from_string(string)
    #     statistics = backtracking(sudoku)
    #     print(get_statistics_text(sudoku_id, statistics))

    # print('Backtracking with MRV')
    # next_variable_heuristic = minimum_remaining_values
    # for sudoku_id, string in sudokus.items():
    #     sudoku = Sudoku.from_string(string)
    #     statistics = backtracking(sudoku, next_variable_heuristic=next_variable_heuristic)
    #     print(get_statistics_text(sudoku_id, statistics))
    
    # print('Backtracking with AC3')
    # for sudoku_id, string in sudokus.items():
    #     sudoku = Sudoku.from_string(string)
    #     statistics = backtracking_with_waterfall(sudoku, [ac3])
    #     print(get_statistics_text(sudoku_id, statistics))

    print('Backtracking with waterfall')
    for sudoku_id, string in sudokus.items():
        sudoku = Sudoku.from_string(string)
        statistics = backtracking_with_waterfall(sudoku, [ac3, naked_pairs])
        print(get_statistics_text(sudoku_id, statistics))


if __name__ == '__main__':
    main()
