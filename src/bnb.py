# importação do pacote mip
from mip import *
import numpy as np
import sys

# salva modelo em arquivo lp, e mostra o conteúdo
def save(model, filename):
    model.write(filename) # salva modelo em arquivo
    with open(filename, "r") as f: # lê e exibe conteúdo do arquivo
        print(f.read())


def Integer(variable):
    if variable - int(variable) == 0:
        return True
    return False


def proximity(variable):
    # print(f"Variable = {variable}")
    return abs(variable - 0.5)


def getBranchVariableIndex(variable_value_list):
        # tira todos os valores inteiros e de valor 0 (temporariamente) da lista de valores das variaveis
        value_list = [i for i in variable_value_list if i != 0 or not Integer(i)]
        # escolhe a variavel fracionaria mais proxima de 0,5
        branch_variable = min(value_list, key=proximity)
        return variable_value_list.index(branch_variable) # caso tenha mais de uma variável com o mesmo valor estamos escolhendo a de menor índice


class Node():
    def __init__(self, model):
        self.model = model
        self.cost = float("inf")

    def integralSolution(self):
        variable_value_list = self.getVariableValueList()
        non_integer_list = [i for i in variable_value_list if i != 0 or not Integer(i)]
        if len(non_integer_list) == 0:
            # print("Poda por integralidade")
            return True

    def isInfeasible(self):
        status = self.model.optimize()
        if status == OptimizationStatus.INFEASIBLE:
            print("Solucao e inviavel")
            return True
        return False

    def toPrune(self, lb):
        # INVIABILIDADE
        # se a solução for inviavels podamos
        if self.isInfeasible():
            return True
        print("Solucao e viavel")
       
        # INTEGRALIDADE
        # se a solução for inteira podamos
        if self.integralSolution():
            return True
        print("Solucao nao e inteira")
    
        # LIMITANTE
        # se a solução for inteira e possuir um valor menor do que o lower bound atual podamos
        if self.integralSolution() and self.model.objective_value <= lb:
            # print("Poda por limitante")
            return True
        print("Solucao nao e menor que lower bound")

    def getVariableValueList(self):
        variable_value_list = []
        for i in range(len(self.model.vars)):
            variable_value_list.append(self.model.var_by_name(f"x_{i+1}").x)
        return variable_value_list

    def solve(self):
        status = self.model.optimize()

        if status != OptimizationStatus.OPTIMAL:
            return

        print("Status = ", status)
        print(f"Solution value  = {self.model.objective_value:.2f}\n")
        
        print("Solution:")
        for v in self.model.vars:
            print(f"{v.name} = {v.x:.2f}")
        print("###########################################################")


def solveProblem(baseModel):

    root = Node(baseModel)
    best_node = Node(baseModel)
    best_node.cost = 0 # mesma coisa que o lower_bound ou limite primal
    
    tree = []
    tree.append(root)

    # branch and bound
    while len(tree) != 0:
        node = tree[-1] # estrategia de busca em profundidade, vamos pelo ultimo no inserido na lista de nos (DFS)
        node.solve()
        # save(node.model, "modelo1.lp")
        
        # se satisfazer algum dos tres criterios de poda, ele poda o no atual (tira ele da lista de nos)
        if not node.toPrune(best_node.model.objective_value):
            # se a solução for inteira e possuir um valor maior do que a melhor solução existente, atualizamos a melhor
            if node.integralSolution() and node.model.objective_value >= best_node.model.objective_value:
                best_node = node

            # escolhe a variavel pra ser ramificada (de valor fracionario mais proximo de 0,5)
            variable_value_list = node.getVariableValueList()
            branch_variable = getBranchVariableIndex(variable_value_list)
            
            # primeiro filho iguala essa variavel a 0
            node.model += node.model.vars[branch_variable] == 0
            tree.append(node)
            print("\nnRestricoes do filho 1:")
            for i in node.model.constrs:
                print(i)

            # segundo filho iguala essa variavel a 1
            node.model.remove(node.model.constrs[-1])
            node.model += node.model.vars[branch_variable] == 1
            tree.append(node)
            print("\nRestricoes do filho 2:")
            for i in node.model.constrs:
                print(i)
        else:
            # print(f"\nArvore antes da remocao: {tree}")
            tree.remove(node)
            # print(f"\nArvore depois da remocao: {tree}")
