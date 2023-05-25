# importação do pacote mip
from mip import *

def main():
    A = range(1, 8)
    D = range(1, 7)
    M = ['A', 'B', 'C', 'D', 'E', 'F']
    Ma = {1: ['A', 'B'], 2: ['A', 'E'], 3: ['A', 'C'], 4: ['A', 'F'], 5: ['B', 'D', 'F'], 6: ['C'], 7: ['C', 'D', 'E']}
  
    model = Model(sense=MINIMIZE, solver_name=CBC)

    x = {d: {m: model.add_var(var_type=BINARY, name=f"x_{d}_{m}") for m in M} for d in D}
    y = {d: model.add_var(var_type=BINARY, name=f"y_{d}") for d in D}

    model.objective = xsum(y[d] for d in D)

    for m in M:
        model += xsum(x[d][m] for d in D) == 1

    for d in D:
        for a in A:
            model += xsum(x[d][m] for m in Ma[a]) <= y[d]

    # salva modelo em arquivo lp, e mostra o conteúdo
    model.write("model.lp") # salva modelo em arquivo
    with open("model.lp", "r") as f: # lê e exibe conteúdo do arquivo
        print(f.read())
    status = model.optimize()

    print(f"Status = {status}\n")
    if status == OptimizationStatus.OPTIMAL:
        print(f"São necessários no mínimo {int(model.objective_value)} dias para realizar as provas.\n")

        day = 1
        for d in D:
            if int(y[d].x) == 1:
                print(f"Dia {day}: ", ", ".join([m for m in M if int(x[d][m].x) == 1]))
                day += 1

if __name__ == "__main__":
    main()