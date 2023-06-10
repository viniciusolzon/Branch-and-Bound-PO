# importação do pacote mip
from mip import *

# salva modelo em arquivo lp, e mostra o conteúdo
def save(model, filename):
    model.write(filename) # salva modelo em arquivo
    with open(filename, "r") as f: # lê e exibe conteúdo do arquivo
        print(f.read())

def Integer(variable):
    # 1 - (1) = 0 -> é inteira
    # 0.58 - (0) = 0.58 -> não é inteira
    if (variable - int(variable)) == 0:
        return True
    else:
        return False

def proximity(variable):
    return abs(variable - 0.5)


class Node():
    def __init__(self, model):
        self.model = model # um nó sempre vai ter um modelo
        self.state = 0 # pra falar se a solução é viável ou não, etc.

    def getBranchVariableIndex(self):
        # lista de variaveis do problema
        variable_value_list = []
        for i in range(len(self.model.vars)):
            variable_value_list.append(self.model.var_by_name(f"x_{i+1}").x)
        
        value_list = []
        # lista de variaveis que possuem valores fracionarios
        for variable in variable_value_list:
            if (variable - int(variable)) != 0:
                value_list.append(variable)

        print(f"LISTA DE VARIAVEIS FRACIONARIAS A SEREM ESCOLHIDAS: ", value_list)
        
        # escolhe a variavel fracionaria mais proxima de 0,5
        branch_variable_index = min(value_list, key = proximity)
        
        return variable_value_list.index(branch_variable_index) # caso tenha mais de uma variável com o mesmo valor estamos escolhendo a de menor índice

    def integralSolution(self):
        for i in range(len(self.model.vars)):
            result = self.model.vars[i].x - int(self.model.vars[i].x)
            if result != 0:
                return False
        return True

    def isInfeasible(self):
        if self.state == OptimizationStatus.INFEASIBLE:
            print("Solucao e inviavel")
            return True
        return False

    def toPrune(self, lb):
        # INVIABILIDADE
        # se a solução for inviavel podamos
        if self.isInfeasible():
            print("Solucao e inviavel")
            return True
        print("Solucao e viavel")
       
        # INTEGRALIDADE
        # se a solução for inteira podamos
        if self.integralSolution():
            print("Solucao e inteira")
            return True
        print("Solucao nao e inteira")
    
        # LIMITANTE
        # se a solução for inteira e possuir um valor menor do que o lower bound atual podamos
        if self.integralSolution() and self.model.objective_value <= lb:
            print("Solucao e menor que lower bound")
            return True
        print("Solucao nao e menor que lower bound")

    def solve(self):
        status = self.model.optimize()
        self.state = status

        if status != OptimizationStatus.OPTIMAL: # se o nó em questão não é inviável
            return


def solveProblem(baseModel):
    print("\t\t##### Branch and Bound #####")
    print("(1) Busca em Largura")
    print("(2) Busca em Profundidade")
    choice = 1
    choice = int(input("-> "))

    root = Node(baseModel) # cria nó raiz com o problema inicial
    best_node = Node(baseModel) # cria um nó pra guardar o melhor nó
    upper_bound = 0
    lower_bound = 0

    tree = [] # lista de nós
    tree.append(root) # adiciona a raíz

    # branch and bound
    while len(tree) != 0: # enquanto a árvore possuir nós abertos
        if choice == 1:
            node = tree[0] # estrategia de busca em largura, vamos pelo primeiro da lista de nos (BFS)
        elif choice == 2:
            node = tree[-1] # estrategia de busca em profundidade, vamos pelo ultimo da lista de nos (DFS)
        
        print("***********************************************************************************************")
        node.solve() # resolve o nó 
        tree.remove(node) # remove o no atual pois ja resolvemos ele

        if node.state == OptimizationStatus.OPTIMAL: # se a solucao for viável
            # tentamos atualizar o lower_bound
            if node.integralSolution() and node.model.objective_value > lower_bound:
                print(f"Atualizamos o lower bound para {node.model.objective_value}")
                lower_bound = float(node.model.objective_value)

                best_node = Node(node.model.copy())
                best_node.model.vars = node.model.vars

        # se nao puder podar ele, gera dois filhos e inserimos os dois na lista de nós
        if not node.toPrune(best_node.model.objective_value):

            # escolhe a variavel pra ser ramificada (de valor fracionario mais proximo de 0.5)
            branch_variable_index = node.getBranchVariableIndex()
            print(f"VARIAVEL A SER RAMIFICADA PARA O NO ATUAL: {node.model.vars[branch_variable_index]}")

            # primeiro filho iguala essa variavel a 0
            left_node = Node(node.model.copy())
            left_node.model += left_node.model.vars[branch_variable_index] == 0
            tree.append(left_node)

            # segundo filho iguala essa variavel a 1
            right_node = Node(node.model.copy())
            right_node.model += right_node.model.vars[branch_variable_index] == 1
            tree.append(right_node)

        else:
            print("VAMOS PODAR (ESSE NO NAO VAI GERAR FILHOS)")

        print(f"Valor da solucao do pai = {node.model.objective_value}")
        
    # quando todos nós da arvore estiverem podados, mostramos a melhor solucao viável encontrada para o problema
    print("\n\n############################################################################")
    print(f"A solucao viavel encontrada esta no maximo a {(upper_bound - lower_bound):.2f} unidades de custo de distancia da melhor solucao viavel do problema")
    
    print("Restricoes da melhor solucao encontrada:")
    for i in best_node.model.constrs:
        print(i)

    print("Variaveis da melhor solucao viavel encontrada:")
    for i in best_node.model.vars:
        print(f"{i} = {i.x}")

    print(f"Custo da melhor solucao viavel encontrada = {lower_bound:.2f}")
    print("############################################################################")
    