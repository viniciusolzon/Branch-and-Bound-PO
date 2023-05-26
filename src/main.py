# importação do pacote mip
from mip import *
import sys
# from bnb import BranchAndBound

# class BranchAndBound():
#     def __init__(self):
#         self.lower_bound = 999999
#         self.valorObj = 0

#     def podar(self):
#         if True:
#             return True
#         else:
#             return False

#     def solve(self):
#         print("\tBranch and Bound\n\nEscolha o método de exploração da árvore:")
#         print("(1) Busca em profundidade - Depth First Search")
#         print("(2) Busca em largura      - Breadth First Search")
#         escolha = int(input("-> "))
#         pass

# salva modelo em arquivo lp, e mostra o conteúdo
def save(model, filename):
  model.write(filename) # salva modelo em arquivo
  with open(filename, "r") as f: # lê e exibe conteúdo do arquivo
    print(f.read())

def solve(model):
  status = model.optimize()

  if status != OptimizationStatus.OPTIMAL:
    return

  print("Status = ", status)
  print(f"Solution value  = {model.objective_value:.2f}\n")
  
  print("Solution:")
  for v in model.vars:
      print(f"{v.name} = {v.x:.2f}")

def main():

  ################################
  ####### Lendo a instancia ######
  ################################

  # file_path = "src/instance1.txt"
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

  model = Model(name= "Branch and Bound", sense=MAXIMIZE, solver_name=CBC)

  x = [model.add_var(var_type=BINARY, lb=0.0, name=f"x_{i+1}") for i in range(num_variaveis)]
  
  model.objective = xsum(int(funcao_obj[i]) * x[i] for i in range(len(funcao_obj)))

  for i in range(num_restricoes):
    model += xsum(int(restricoes[i][j]) * x[j] for j in range(num_variaveis)) <= int(restricoes[i][-1])

  save(model, "modelo1.lp")
  solve(model)

  ################################
  ########## Algoritmo ###########
  ################################


  

if __name__ == "__main__":
  # bnb = BranchAndBound()
  # bnb.solve()
  main()
# soluções ótimas do teobaldo: 20, 24, 19 e 10
