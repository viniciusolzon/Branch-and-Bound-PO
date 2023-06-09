import sys
from bnb import *

def main():
    ################################
    ####### Lendo a instancia ######
    ################################

    file_path = sys.argv[1]
    f = open(file_path, "r")
    
    first_line  = f.readline().split() # primeira linha
    funcao_obj = f.readline().split() # segunda linha

    num_variaveis = int(first_line[0]) # numero de variaveis (variaveis enumeradas de 1 a n)
    num_restricoes = int(first_line[1]) # número de restricoes (restricoes enumerados de 1 a n)
    
    restricoes = []
    for i in range(num_restricoes):
        restricoes.append(f.readline().split()) 

    ################################
    ####### Criando o modelo #######
    ################################

    model = Model(name= "Branch and Bound pai", sense=MAXIMIZE, solver_name=CBC)

    x = [model.add_var(var_type=CONTINUOUS, lb=0.0, ub = 1.0, name=f"x_{i+1}") for i in range(num_variaveis)]
    
    model.objective = xsum(int(funcao_obj[i]) * x[i] for i in range(len(funcao_obj)))

    for i in range(num_restricoes):
        model += xsum(int(restricoes[i][j]) * x[j] for j in range(num_variaveis)) <= int(restricoes[i][-1])
    
    # save(model, "modelo1.lp")
    
    solveProblem(model)

if __name__ == "__main__":
  main()
# SOLUCAO OTIMA DAS INSTANCIAS TESTE: 20, 24, 19 e 10, RESPECTIVAMENTE
