import fileinput
from itertools import combinations
from pysat.solvers import Glucose3



def read_input(filename):
    matrix = []
    for line in fileinput.input('input/' + filename + '.txt'):
        matrix.append(line.strip().split(','))
    return matrix

def neighbors(matrix, x, y):
    DIRECTION = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    return [
        (x + dx, y + dy)
        for dx, dy in DIRECTION
        if 0 <= x + dx < len(matrix) and 0 <= y + dy < len(matrix[0]) and matrix[x + dx][y + dy] == '_'
    ]
        
def CellID(matrix, cell):
    return cell[0] * len(matrix[0]) + cell[1] + 1

def GenerateDNF(matrix, i, j):
    dnf = []
    surrounding_cells = neighbors(matrix, i, j)
    for combination in combinations(surrounding_cells, int(matrix[i][j])):
        clause = []
        for cell in surrounding_cells:
            cell_id = CellID(matrix, cell)
            if cell in combination:
                clause.append(cell_id)  # cell is a trap
            else:
                clause.append(-cell_id)  # cell is not a trap
        dnf.append(clause)

    return dnf

def GenerateTruthTable(dnf_clauses):
    num_variables = len(set([abs(literal) for clause in dnf_clauses for literal in clause]))
    truth_table = []
    for i in range(2 ** num_variables):
        truth_table.append([])
        for j in range(num_variables):
            truth_table[-1].append((i >> j) & 1)
    
    return truth_table

def GenerateCNF(truth_table, dnf_clauses):
    cnf = []
    i = 0
    for row in truth_table:
        OR = False
        for clause in dnf_clauses:
            sorted_literal_index = sorted([abs(literal) for literal in clause])

            AND = True
            for literal in clause:
                idx = sorted_literal_index.index(abs(literal))
                AND &= row[idx] if literal > 0 else not row[idx]
            OR |= AND
        if OR == False:
            cnf.append(de_morgan([sorted_literal_index[literal] if truth_table[i][literal] == 1 else -1 * sorted_literal_index[literal] for literal in range(len(truth_table[i]))]))
        i += 1
    return cnf

def de_morgan(clause):
    return [-literal for literal in clause]

def cmp(e):
    return len(e)

def generate_clauses(matrix):
    row = len(matrix[0])
    cnfs = []
    existed = set() 
    for i in range(len(matrix)):
        for j in range(row):
            if matrix[i][j] != '_':
                dnf = GenerateDNF(matrix, i, j)
                truth_table = GenerateTruthTable(dnf)
                cnf = GenerateCNF(truth_table, dnf)
                for clause in cnf:
                    if tuple(clause) in existed:
                        cnf.pop(cnf.index(clause))
                    else:
                        existed.add(tuple(clause))
                cnfs.append(cnf)
    
    clauses = []
    for cnf in cnfs:
        for clause in cnf:
            clauses.append(clause)
    
    clauses.sort()
    clauses.sort(key=cmp)

    while len(clauses[0]) == 1:
        for clause in clauses:
            if len(clause) == 1:
                if clause[0] > 0:
                    if clause[0] % row == 0:
                        matrix[int(clause[0] / row) - 1][row - 1] = 'T'
                    else:
                        matrix[int(clause[0] / row)][clause[0] % row - 1] = 'T'
                else:
                    if abs(clause[0]) % row == 0:
                        matrix[int(abs(clause[0]) / row) - 1][row - 1] = 'G'
                    else:
                        matrix[int(abs(clause[0]) / row)][abs(clause[0]) % row - 1] = 'G'
                clauses.remove(clause)
                tmp = []
                tmp.append(-clause[0])
                for c in clauses:
                    if clause[0] in c:
                        clauses.remove(c)
                    if tmp[0] in c:
                        c.remove(tmp[0])
        clauses.sort()
        clauses.sort(key=cmp)
    return clauses

