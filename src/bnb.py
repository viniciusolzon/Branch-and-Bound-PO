class Node():
    def __init__(self):
        self.lower_bound = 0
        self.objValue
        self.choice = 2 # por padrão executaremos a busca em largura (Breadth First Search)

    def prune(self):
        if True:
            return True
        else:
            return False

    def solve(self):
        print("\tBranch and Bound\n\nEscolha o método de exploração da árvore:")
        print("(1) Busca em profundidade - Depth First Search")
        print("(2) Busca em largura      - Breadth First Search")
        self.choice = int(input("-> "))
        pass