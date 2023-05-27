# importação do pacote mip
from mip import *
import numpy as np
import sys
# from bnb import BranchAndBound


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


def getVariableValueList(model, variable_amount):
  variable_list = []
  for i in range(variable_amount):
    variable_list.append(model.var_by_name(f"x_{i+1}").x)
  return variable_list


def Integer(variable):
  if variable - int(variable) == 0:
    return True
  return False


def proximity(variable):
    return abs(variable - 0.5)


def getBranchVariableIndex(variable_value_list):
  # tira todos os valores inteiros e de valor 0 (temporariamente) da lista de valores das variáveis
  value_list = [i for i in variable_value_list if i != 0 or not Integer(i)]
  branch_variable = min(value_list, key=proximity)
  return variable_value_list.index(branch_variable) # caso tenha mais de uma variável com o mesmo valor estamos escolhendo a de menor índice


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

  model = Model(name= "Branch and Bound", sense=MAXIMIZE, solver_name=CBC)

  x = [model.add_var(var_type=CONTINUOUS, lb=0.0, name=f"x_{i+1}") for i in range(num_variaveis)]
  
  model.objective = xsum(int(funcao_obj[i]) * x[i] for i in range(len(funcao_obj)))

  for i in range(num_restricoes):
    model += xsum(int(restricoes[i][j]) * x[j] for j in range(num_variaveis)) <= int(restricoes[i][-1])

  solve(model)
  

  list = getVariableValueList(model, num_variaveis)
  branch_variable_index = getBranchVariableIndex(list)
  model += x[branch_variable_index] == 1
  solve(model)
  
  list = getVariableValueList(model, num_variaveis)
  branch_variable_index = getBranchVariableIndex(list)
  model += x[branch_variable_index] == 0
  solve(model)
  
  list = getVariableValueList(model, num_variaveis)
  branch_variable_index = getBranchVariableIndex(list)
  model += x[branch_variable_index] == 0
  solve(model)

  save(model, "modelo1.lp")


  ################################
  ########## Algoritmo ###########
  ################################

  # model += x[1] == 1

  # model += x[2] == 0

  # model += x[0] == 0

  # save(model, "modelo1.lp")
  # solve(model)
  
#   Node BranchBound_DFS(Data *data, double **cost){ // executa o algoritmo utilizando busca por profundidade DFS(Depth First Search)
# 	Node root; // cria o nó raíz da árvore
#     Node best_solution; // cria o nó em que será guardada a melhor solução
# 	best_solution.cost = numeric_limits<double>::infinity(); // seta o custo da melhor solução inicialmente para "infinito"
# 	list<Node> tree;
# 	tree.push_back(root); // cria a árvore que será preenchida e feita a busca nela
#     // a "árvore" será na verdade uma lista em que iremos inserindo e removendo no começo e/ou no final de acordo com o algortimo

# 	double upper_bound = 99999999; // "qualquer", ou seja, o primeiro upper_bound encontrado já será atribuído a essa variável devido ao seu custo

# 	while(!tree.empty()){ // equanto todos os nós da árvore não forem analisados
#     	// auto node = tree.end(); // assim não funciona, precisa ser assim aí na linha de baixo
#     	auto node = prev(tree.end()); // vai pelo último nó -> DFS strategy

# 		getSolutionHungarian(*node, data); // calcula a solução do subtour atual

#         // se for debugar descomenta a linha de baixo, mas o melhor pra debuggar é logo aqui embaixo na linha 231
#         // show_info(*node);

# 		if(node->cost > upper_bound){ // solução gerada pelo algoritmo húngaro do assignment problema é descartada pois o custo é maior que o upper bound
# 			tree.erase(node);
# 			continue;
# 		}
# 		if(node->feasible == true){ // se a solução for viável
# 			if(node->cost < best_solution.cost){// e se o custo da solução for menor que o o custo da melhor solução encontrada até agora
#                 best_solution = *node; // atualizamos a melhor solução
# 				upper_bound = node->cost; // upper_bound é atualizado com o custo dessa nova solução
#                 // Solução viável foi gerada, caso queira olhar as soluções geradas na execução do algoritmo descomenta "show_info()"
#                 // show_info(best_solution);
# 			}

# 			tree.erase(node); // esse nó já foi analisado então tira ele da árvore
# 			continue;
# 		}
#         // Solução inviável foi gerada, caso queira olhar as soluções geradas na execução do algoritmo descomenta "show_info()"
#         // else{
#         //         // show_info(node);
#         // }
        
# 	# aqui tava dando mt problema pq o (node.subtours[i].size()) nunca era < que (node.subtours[0].size()) no final da função getSolutionHungarian() então
# 	# o node->pick não era escolhido, fazendo com que ele ficasse com o valor inicializado, e eu não setava ele inicialmente pra 0, então ele pegava lixo
# 	# de memória. Logo, esse loop aqui de baixo nunca era inicializado e bugava o código. Pra arrumar só seto o pick inicial pra zero, ou seja, se ele não
# 	# achar nenhum tour menor pra escolher, (todos são do mesmo tamanho), ele escolhe o primeiro.
#   for(int i = 0; i < node->subtours[node->pick].size() - 1; i++){ // Adiciona folhas/filhos na árvore
#     Node new_node;
#     new_node.forbidden_arcs = node->forbidden_arcs; // atribui os arcos proibidos do nó da árvore ao nó atual que será inserido no final da árvore

#     pair<int, int> new_forbidden_arc;
#     new_forbidden_arc.first = node->subtours[node->pick][i];
#     new_forbidden_arc.second = node->subtours[node->pick][i + 1];

#     new_node.forbidden_arcs.push_back(new_forbidden_arc);
#     tree.insert(tree.end(), new_node); // insere novos nós na árvore de busca
#   }

#   tree.erase(node);
# }

#     return best_solution; 
# }

if __name__ == "__main__":
  # bnb = BranchAndBound()
  # bnb.solve()
  main()
# soluções ótimas do teobaldo: 20, 24, 19 e 10
