from cnf import *

def simplify_clauses(literal, clauses):
    new_clauses = []
    for clause in clauses:
        if literal in clause:
            continue  # Clause is satisfied, so it's removed
        if -literal in clause:
            new_clause = [x for x in clause if x != -literal]
            if not new_clause:  # Clause is empty, unsatisfiable
                return [], True
            new_clauses.append(new_clause)
        else:
            new_clauses.append(clause)
    return new_clauses, False

def backtracking(cnf, symbols, model):
    if not cnf:
        return True, model
    if any(not clause for clause in cnf):
        return False, {}
    
    # Heuristic: Choose the literal that appears in the most clauses
    literal = max(symbols, key=lambda x: sum(x in clause or -x in clause for clause in cnf))
    symbols.remove(literal)

    for val in [literal, -literal]:
        model[abs(val) - 1] = val
        new_cnf, empty_found = simplify_clauses(val, cnf)
        if not empty_found:
            result, final_model = backtracking(new_cnf, symbols, model)
            if result:
                return True, final_model
    
    symbols.add(literal)  # backtrack: re-add the symbol
    return False, {}

def backtrack_solver(matrix):
    clauses = generate_clauses(matrix)
    symbols = {abs(literal) for clause in clauses for literal in clause}
    model = [0] * max(symbols, default=0)

    satisfiable, final_model = backtracking(clauses, symbols, model)
    if satisfiable:
        return final_model
    return None
