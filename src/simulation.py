from sympy import *

from src.circuit import *
from src.theorems import *

class Simulation:
    def __init__(self, circuit):
        print("Simulation en cours")
        self.circuit = circuit
        if len(circuit.wires) == 0:
            print("Attention : Aucun fil trouvé, simulation annulée")
            return

        if len(circuit.components) == 0:
            print("Attention : Aucun composant trouvé, simulation annulée")
            return

        self.list_unknowns()
        self.establish_equations()

        self.solve_equations()

    def establish_equations(self):
        self.equations = []
        for theorem in theorem_list:
            if theorem.target_class == Wire:
                for wire in self.circuit.wires:
                    if theorem.support(wire):
                        self.equations += theorem.apply(wire)
            elif theorem.target_class == Component:
                for component in self.circuit.components:
                    if theorem.support(component):
                        self.equations += theorem.apply(component)

        self.equations += [ Eq(self.circuit.wires[0].symbol, 0) ]
        print("Équations établies : ", self.equations)

    def list_unknowns(self):
        self.unknowns = []
        for wire in self.circuit.wires:
            self.unknowns.append(wire.symbol)
        print("Inconnues listées :", self.unknowns)

    def solve_equations(self):
        print(solve(self.equations, self.unknowns))


