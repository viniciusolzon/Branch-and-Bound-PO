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
    if (variable - int(variable)) == 0:
        return True
    else:
        return False


def proximity(variable):
    return abs(variable - 0.5)


# def getBranchVariableIndex(variable_value_list):
#         value_list = []
#         # lista de variaveis que possuem valores fracionarios
#         for value in variable_value_list:
#             print(f"{value} - {int(value)} == {value - int(value)}")
#             if (value - int(value)) != 0:
#                 value_list.append(value)

#         # lista de variaveis que possuem valores fracionarios
#         # value_list = [i for i in variable_value_list if i != 0 or not Integer(i)]
#         print(f"LISTA DE TODAS AS VARIAVEIS: ", variable_value_list)
#         print(f"LISTA DE VARIAVEIS FRACIONARIAS A SEREM ESCOLHIDAS: ", value_list)

#         # escolhe a variavel fracionaria mais proxima de 0,5
#         branch_variable = min(value_list, key=proximity)
#         return variable_value_list.index(branch_variable) # caso tenha mais de uma variável com o mesmo valor estamos escolhendo a de menor índice


class Node():
    def __init__(self, model):
        self.model = model
        self.status = 0

    def getBranchVariableIndex(self):
        
        # lista de todas as variaveis do modelo
        variable_value_list = []
        for variable in self.model.vars:
            variable_value_list.append(variable.x)

        # lista de variaveis que possuem valores fracionarios
        value_list = []
        for value in variable_value_list:
            # print(f"{value} - {int(value)} == {value - int(value)}")
            if (value - int(value)) != 0:
                value_list.append(value)

        # lista de variaveis que possuem valores fracionarios
        # value_list = [i for i in variable_value_list if i != 0 or not Integer(i)]
        print(f"LISTA DE TODAS AS VARIAVEIS: ", variable_value_list)
        print(f"LISTA DE VARIAVEIS FRACIONARIAS A SEREM ESCOLHIDAS: ", value_list)

        # escolhe a variavel fracionaria mais proxima de 0,5
        branch_variable = min(value_list, key=proximity)
        return variable_value_list.index(branch_variable) # caso tenha mais de uma variável com o mesmo valor estamos escolhendo a de menor índice


    def getVariableValueList(self):
        variable_value_list = []
        for i in range(len(self.model.vars)):
            variable_value_list.append(self.model.var_by_name(f"x_{i+1}").x)
        return variable_value_list

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
        # se a solução for inviavels podamos
        # branch_variable = self.getBranchVariableIndex()
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


    # def roundVariables(self, num_digits):
    #     for variable in self.model.vars:
    #         print(f"VARIAVEL {variable} ANTES DE SER ARREDONDADA = {variable.x}")
    #         print(f"VARIAVEL {variable} DEPOIS DE SER ARREDONDADA = {round(variable.x, num_digits)}")

    def solve(self):
        status = self.model.optimize()
        self.state = status
        if status != OptimizationStatus.OPTIMAL:
            return


def solveProblem(baseModel):
    print("\t\t##### Branch and Bound #####")
    print("(1) Busca em Largura")
    print("(2) Busca em Profundidade")
    choice = 1
    choice = int(input("-> "))

    root = Node(baseModel)
    best_node = Node(baseModel)
    lower_bound = 0

    tree = []
    tree.append(root)

    # branch and bound
    for i in range(10):
    # while len(tree) != 0:
        if choice == 1:
            node = tree[0] # estrategia de busca em largura, vamos pelo primeiro da lista de nos (BFS)
        elif choice == 2:
            node = tree[-1] # estrategia de busca em profundidade, vamos pelo ultimo da lista de nos (DFS)
        
        # save(node.model, "modelo1.lp")
        print("***********************************************************************************************")
        node.solve()
        # print(f"VARIAVEL {node.model.vars[6]} ANTES DE SER ARREDONDADA = {node.model.vars[6].x}")
        # print(f"VARIAVEL {node.model.vars[6]} DEPOIS DE SER ARREDONDADA = {round(node.model.vars[6].x, 4)}")

        print("\n\nRestricoes do pai:")
        for i in node.model.constrs:
            print(i)
        
        if node.state == OptimizationStatus.OPTIMAL:
            # tentamos atualizar o lower_bound
            if node.integralSolution() and node.model.objective_value > lower_bound:
                print(f"Atualizamos o lowerbound para {node.model.objective_value}")
                lower_bound = float(node.model.objective_value)
                best_node.model = node.model.copy()

            # branch_variable = node.getBranchVariableIndex()
            variable_value_list = []
            for variable in node.model.vars:
                variable_value_list.append(variable.x)

            # lista de variaveis que possuem valores fracionarios
            value_list = []
            for value in variable_value_list:
                # print(f"{value} - {int(value)} == {value - int(value)}")
                if (value - int(value)) != 0:
                    value_list.append(value)
        

        # lista de variaveis que possuem valores fracionarios
        # value_list = [i for i in variable_value_list if i != 0 or not Integer(i)]
        print(f"LISTA DE TODAS AS VARIAVEIS: ", variable_value_list)
        print(f"LISTA DE VARIAVEIS FRACIONARIAS A SEREM ESCOLHIDAS: ", value_list)

        # se podar for possivel, a gente poda(tira esse no da lista de nos)
        if node.toPrune(lower_bound):
            print("VAMOS PODAR (ESSE NO NAO VAI GERAR FILHOS)")
            # print(f"\nTamanho da arvore antes da remocao: {len(tree)}")
            tree.remove(node)
            # print(f"Tamanho da arvore depois da remocao: {len(tree)}\n")
            
        # se nao puder podar ele, cria dois filhos e inserimos os dois na lista de nos
        else:       
            # escolhe a variavel pra ser ramificada (de valor fracionario mais proximo de 0,5)
            # variable_value_list = node.getVariableValueList()
            # branch_variable = getBranchVariableIndex(variable_value_list)
            branch_variable = node.getBranchVariableIndex()
            print(f"VARIAVEL A SER RAMIFICADA PARA O NO ATUAL: {node.model.vars[branch_variable]}")

            # primeiro filho iguala essa variavel a 0
            left_node = Node(node.model.copy())
            left_node.model += left_node.model.vars[branch_variable] == 0
            tree.append(left_node)
            print("\n\nRestricoes do filho 1:")
            for i in left_node.model.constrs:
                print(i)

            # segundo filho iguala essa variavel a 1
            right_node = Node(node.model.copy())
            right_node.model += right_node.model.vars[branch_variable] == 1
            tree.append(right_node)
            print("\nRestricoes do filho 2:")
            for i in right_node.model.constrs:
                print(i)
            
            # remove o no atual pois ja resolvemos ele
            tree.remove(node)

        print(f"Valor da solucao do pai = {node.model.objective_value}")
        
    # quando todos no da arvore estiverem fechados, mostramos a melhor solucao encontrada
    print(f"\n\n-> Custo da melhor solucao encontrada = {lower_bound:.4f}\n")