from bnb import *

from mip import *
import numpy as np
import sys

def solve(model):
    status = model.optimize()

    if status != OptimizationStatus.OPTIMAL:
        return

    print("Status = ", status)
    print(f"Solution value  = {model.objective_value:.2f}\n")

    print("Solution:")
    for v in model.vars:
        print(f"{v.name} = {v.x:.2f}")
    print("###########################################################")

def save(model, filename):
    model.write(filename) # salva modelo em arquivo
    with open(filename, "r") as f: # lê e exibe conteúdo do arquivo
        print(f.read())

def main():
    ################################
    ####### Lendo a instancia ######
    ################################

    # file_path = "src/teste1.txt"
    file_path = sys.argv[1]
    f = open(file_path, "r")
    
    first_line  = f.readline().split()
    funcao_obj = f.readline().split()

    num_variaveis = int(first_line[0]) # numero de variaveis (variaveis enumeradas de 1 a n)
    num_restricoes = int(first_line[1]) # número de restricoes (restricoes enumerados de 1 a n)
    
    restricoes = []
    for i in range(num_restricoes):
        restricoes.append(f.readline().split()) 

    ################################
    ####### Criando o modelo #######
    ################################

    model = Model(name= "Branch and Bound pai", sense=MAXIMIZE, solver_name=CBC)

    x = [model.add_var(var_type=CONTINUOUS, lb=0.0, name=f"x_{i+1}") for i in range(num_variaveis)]
    
    model.objective = xsum(int(funcao_obj[i]) * x[i] for i in range(len(funcao_obj)))

    for i in range(num_restricoes):
        model += xsum(int(restricoes[i][j]) * x[j] for j in range(num_variaveis)) <= int(restricoes[i][-1])

    # save(model, "modelo1.lp")
    # solve(model)
    
    solveProblem(model)


if __name__ == "__main__":
  main()
# soluções ótimas do teobaldo: 20, 24, 19 e 10
# unico problema agora e que na instacia 2 de Teobaldo estamos achando o otimo como 25, o resto ta ok
