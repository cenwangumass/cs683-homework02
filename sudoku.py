import copy
from pprint import pprint


class Sudoku(object):
    all_variables = set((i, j) for i in range(9) for j in range(9))

    def __init__(self, data):
        self.data = data
        self._assigned_variables = self._get_assigned_variables()
        self._unmodifiable = frozenset(self._get_assigned_variables())

    @classmethod
    def from_string(cls, string):
        data = [line.split(' ') for line in string.strip().split('\n')]

        for i in range(9):
            for j in range(9):
                if data[i][j] == '-':
                    data[i][j] = 0
                else:
                    data[i][j] = int(data[i][j])

        return cls(data)

    @classmethod
    def from_file(cls, filename):
        with open(filename) as f:
            string = f.read()
        return cls.from_string(string)

    def print(self):
        pprint(self.data)

    def _get_assigned_variables(self):
        return set(
            (i, j) for i in range(9) for j in range(9) if self.data[i][j] != 0)

    @property
    def assigned_variables(self):
        return self._assigned_variables

    @property
    def unassigned_variables(self):
        return self.all_variables - self.assigned_variables

    def get_box(self, box):
        box_i, box_j = divmod(box, 3)
        box_i, box_j = box_i * 3, box_j * 3

        values = set()
        for i in range(box_i, box_i + 3):
            for j in range(box_j, box_j + 3):
                values.add(self.data[i][j])

        if 0 in values:
            values.remove(0)

        return values

    def has_conflict(self, variable, value):
        variable_i, variable_j = variable

        if variable in self.assigned_variables and self.data[variable_i][variable_j] != value:
            raise ValueError(f'{variable} already assigned, but the tested value is not equal to assigned value')

        for j in range(9):
            if self.data[variable_i][j] == value and j != variable_j:
                return True

        for i in range(9):
            if self.data[i][variable_j] == value and i != variable_i:
                return True

        box_i, box_j = variable_i // 3, variable_j // 3
        for i in range(3):
            for j in range(3):
                p, q = box_i * 3 + i, box_j * 3 + j
                if self.data[p][q] == value and p != variable_i and q != variable_j:
                    return True

        return False

    def pair_has_conflict(self, variable1, value1, variable2, value2):
        i1, j1 = variable1
        i2, j2 = variable2

        if variable1 in self._assigned_variables:
            if value1 != self.data[i1][j1]:
                raise ValueError(f'{variable1} already assigned')
        else:
            self.data[i1][j1] = value1

        if variable2 in self._assigned_variables:
            if value2 != self.data[i2][j2]:
                raise ValueError(f'{variable2} already assigned')

        has_conflict = self.has_conflict(variable2, value2)

        if variable1 not in self._assigned_variables:
            self.data[i1][j1] = 0

        return has_conflict

    def compute_remaining_values(self, variable):
        if variable in self.assigned_variables:
            raise ValueError(f'{variable} already assigned')

        variable_i, variable_j = variable
        used = set()

        for j in range(9):
            used.add(self.data[variable_i][j])

        for i in range(9):
            used.add(self.data[i][variable_j])

        box_i, box_j = variable_i // 3, variable_j // 3
        for i in range(3):
            for j in range(3):
                used.add(self.data[box_i * 3 + i][box_j * 3 + j])

        if 0 in used:
            used.remove(0)

        return set(range(1, 10)) - used

    def compute_neighbors(self, variable):
        variable_i, variable_j = variable
        neighbors = []

        for j in range(9):
            neighbor = (variable_i, j)
            if neighbor not in self._assigned_variables and neighbor != variable:
                neighbors.append(neighbor)

        for i in range(9):
            neighbor = (i, variable_j)
            if neighbor not in self._assigned_variables and neighbor != variable:
                neighbors.append(neighbor)

        box_i, box_j = variable_i // 3, variable_j // 3
        for i in range(3):
            for j in range(3):
                neighbor = (box_i * 3 + i, box_j * 3 + j)
                if neighbor not in self._assigned_variables and neighbor != variable:
                    neighbors.append(neighbor)

        return neighbors

    def assign(self, variable, value):
        if variable in self.assigned_variables:
            raise ValueError(f'{variable} already assigned')

        i, j = variable
        self.data[i][j] = value
        self._assigned_variables.add(variable)

    def undo(self, variable):
        if variable not in self.assigned_variables:
            raise ValueError(f'{variable} not assigned')

        i, j = variable
        self.data[i][j] = 0
        self._assigned_variables.remove(variable)

    def is_complete(self):
        return len(self._assigned_variables) == len(self.all_variables)

    def copy(self):
        data = copy.deepcopy(self.data)
        return Sudoku(data)
