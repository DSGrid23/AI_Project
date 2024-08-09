from cnf import *
from itertools import product

def brute_force_sat(cnf):
    variables = list({abs(x) for clause in cnf for x in clause})
    for assignment in product([False, True], repeat=len(variables)):
        assignment_dict = dict(zip(variables, assignment))
        if all(any(assignment_dict[abs(x)] == (x > 0) for x in clause) for clause in cnf):
            return [key if val else -key for key, val in assignment_dict.items()]
    return None

def bruteforce_solver(matrix):
    clauses = set()
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] != '_':
                dnf = GenerateDNF(matrix, i, j)
                truth_table = GenerateTruthTable(dnf)
                cnf = GenerateCNF(truth_table, dnf)
                cnf.append([-CellID(matrix, (i, j))])
                clauses.update(tuple(clause) for clause in cnf)

    assignment = brute_force_sat(list(clauses))
    return assignment
