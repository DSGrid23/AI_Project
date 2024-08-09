import sys
from Gem_Hunter import *
import time

def main():
    methods= {'Optimal': optimal, "Backtracking":backtrack_solver}
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        for method in methods:
            print("Method:", method)
            solve = GemHunter(input_file,method)
            print("\n")
        solution = PySat_solver(read_input(input_file))
        if solution:
            for row in solution:
                print(' '.join(row))
        
    
    else:
        print("Execute the program with the following command: python main.py <input_file>")

if __name__ == "__main__":
    input_file='input5x5'
    solve= GemHunter(input_file, "Brute-force")
    solution = PySat_solver(read_input(input_file))
    if solution:
        for row in solution:
            print(' '.join(row)) 
    #main()
    