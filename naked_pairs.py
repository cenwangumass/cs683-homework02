from collections import defaultdict

from sudoku import Sudoku


def naked_pairs(sudoku: Sudoku, domains: dict):
    domains_changed = False

    for i in range(9):
        domain_to_variables = defaultdict(list)

        for j in range(9):
            variable = i, j
            domain = frozenset(domains[variable])
            domain_to_variables[domain].append(variable)

        for domain, variables in domain_to_variables.items():
            if len(domain) > 1 and len(domain) == len(variables):
                js = set(variable[1] for variable in variables)
                for j in range(9):
                    if j not in js:
                        variable = i, j
                        if domains[variable] & domain:
                            domains[variable] -= domain
                            domains_changed = True

    for j in range(9):
        domain_to_variables = defaultdict(list)

        for i in range(9):
            variable = i, j
            domain = frozenset(domains[variable])
            domain_to_variables[domain].append(variable)

        for domain, variables in domain_to_variables.items():
            if len(domain) > 1 and len(domain) == len(variables):
                is_ = set(variable[0] for variable in variables)
                for i in range(9):
                    if i not in is_:
                        variable = i, j
                        if domains[variable] & domain:
                            domains[variable] -= domain
                            domains_changed = True

    return domains, domains_changed
