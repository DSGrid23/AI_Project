import random
from cnf import generate_clauses

def walksat(matrix, clauses, p=0.5, max_flips=100000):
    assignment = {}
    variable_list = [] 
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            var_index = i * len(matrix[i]) + j + 1
            if matrix[i][j] == '_':
                assignment[var_index] = random.choice([True, False])
                variable_list.append(var_index)
            elif matrix[i][j] == 'T':
                assignment[var_index] = True
            else:
                assignment[var_index] = False

    for _ in range(max_flips):
        unsatisfied = [clause for clause in clauses if not is_satisfied(clause, assignment)]
        if not unsatisfied:
            return [assignment[v] for v in sorted(assignment)]

        clause = random.choice(unsatisfied)
        if random.random() < p:
            var = abs(random.choice(clause)) 
        else:
            var = select_variable_to_flip(clause, clauses, assignment)

        assignment[var] = not assignment[var] 

    return None 

def is_satisfied(clause, assignment):
    return any(assignment[abs(x)] == (x > 0) for x in clause)

def select_variable_to_flip(clause, clauses, assignment):
    best_var = None
    min_unsatisfied = float('inf')

    for var in clause:
        var = abs(var)
        assignment[var] = not assignment[var] 
        unsatisfied = sum(not is_satisfied(c, assignment) for c in clauses)

        if unsatisfied < min_unsatisfied:
            min_unsatisfied = unsatisfied
            best_var = var

        assignment[var] = not assignment[var]  # flip back

    return best_var

def optimal(matrix):
    clauses = generate_clauses(matrix)  
    return walksat(matrix, clauses)


