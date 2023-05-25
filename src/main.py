# importação do pacote mip
from mip import *

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

def solve(model):
  status = model.optimize()

  if status != OptimizationStatus.OPTIMAL:
    return

  print("Status = ", status)
  print(f"Solution value  = {model.objective_value:.2f}\n")
  
  print("Solution:")
  for v in model.vars:
      print(f"{v.name} = {v.x:.2f}")

# salva modelo em arquivo lp, e mostra o conteúdo
def save(model, filename):
  model.write(filename) # salva modelo em arquivo
  with open(filename, "r") as f: # lê e exibe conteúdo do arquivo
    print(f.read())

def main():
    file_path = "src/instance1.txt"
    f = open(file_path, "r")
    
    first_line  = f.readline().split()
    funcao_obj = f.readline().split()
    # print(first_line)
    # print(funcao_obj)

    num_variaveis = int(first_line[0]) # numero de variaveis (variaveis enumeradas de 1 a n)
    num_restricoes = int(first_line[1]) # número de restricoes (restricoes enumerados de 1 a n)
    
    # print(f"Numero de variaveis = {num_variaveis}")
    # print(f"Numero de restricoes = {num_restricoes}")
    # print(f"\n\tMax: ", end = "")
    # for i in range(len(funcao_obj)):
    #     print(f"{funcao_obj[i]}x{i+1} + ", end = "")
    # print()
    
    restricoes = []
    for i in range(num_restricoes):
        restricoes.append(f.readline().split()) 
    # print(restricoes)

    # print(f"s.a:")
    # for i in range(num_restricoes):
    #     for j in range(num_variaveis):
    #         print(f"{restricoes[i][j]}x{j+1} + ", end = "")
    #     print(f" <= {restricoes[i][j+1]}")

    # print()


    model = Model(sense=MAXIMIZE, solver_name=CBC)

    x = [model.add_var(var_type=CONTINUOUS, lb=0.0, name=f"x_{i+1}") for i in range(num_variaveis)]

    
    model.objective = xsum([i] for i in funcao_obj * x[j] for j in range(num_variaveis))

    for i in range(num_restricoes):
        model += xsum(int(restricoes[i][j]) * x[j] for j in range(num_variaveis)) <= int(restricoes[i][-1])


    save(model, "modelo1.lp")
    solve(model)

if __name__ == "__main__":
    # bnb = BranchAndBound()
    # bnb.solve()
    main()