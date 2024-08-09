from cnf import *
from optimal import optimal
from backtrack import backtrack_solver
from bruteforce import bruteforce_solver
import time
from copy import deepcopy
method ={'Optimal': optimal, "Backtracking":backtrack_solver, "Brute-force":bruteforce_solver}
from pysat.solvers import Glucose3
class GemHunter:
    def __init__(self, file_name,method ):
        self.file_name = file_name
        self.method=method
        self.run_game()

    def run_game(self):
        self.puzzle = read_input(self.file_name)

        s_time = time.time()
        self.method_answer = getAnswer(self.puzzle, method.get(self.method, None))
        s_time = time.time() - s_time
        print("Time taken by", self.method, "method:", s_time, "seconds")
        output_file = 'output/output' + self.file_name[5:]+".txt"  # Change the output file path
        fo = open(output_file, 'w')   
        for i in range(len(self.method_answer)):
            for j in range(len(self.method_answer[0]) - 1):
                fo.write(self.method_answer[i][j] + ", ")
            fo.write(self.method_answer[i][j+1] + "\n")
        fo.close()

        

def getAnswer(board, function):
    puzzle = deepcopy(board)
    answer = convertResult(function(puzzle), puzzle)
    return answer

def convertResult(assignment, board):
    if assignment is None:
        return None
    result = [['G' for _ in range(len(board[0]))] for _ in range(len(board))]
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] != '_':
                result[i][j] = board[i][j]
            else:
                if assignment[i * len(board[0]) + j] > 0:
                    result[i][j] = 'T'
    return result


#PySat
def PySat_solver(matrix):
    height, width = len(matrix), len(matrix[0])
    solver = Glucose3()
    for i in range(height):
        for j in range(width):
            if matrix[i][j].isdigit():
                count = int(matrix[i][j])
                nbs = neighbors(matrix, i, j)
                # Generate combinations for both traps and safe cells
                for comb in combinations(nbs, count + 1):
                    solver.add_clause([-CellID(matrix, cell) for cell in comb])
                for comb in combinations(nbs, len(nbs) - count + 1):
                    solver.add_clause([CellID(matrix, cell) for cell in comb])

    # Solve and interpret the solution
    if solver.solve():
        solution = solver.get_model()
        result = [['_' for _ in range(width)] for _ in range(height)]
        for i in range(height):
            for j in range(width):
                if matrix[i][j] == '_':
                    cid = CellID(matrix, (i, j))
                    result[i][j] = 'T' if cid in solution else 'G'
        return result
    else:
        return None