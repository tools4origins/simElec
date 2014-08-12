from sympy import Symbol, Eq, I

from src.theorems import *

class Resistor(Dipole):
    def __init__(self, name, display=[]):
        Dipole.__init__(self, name, display)
        self.supported_theorem.append(MillmanTheorem)

    def get_symbol(self):
        return Symbol(self.name)


class Inductor(Dipole):
    def __init__(self, name, display=[]):
        Dipole.__init__(self, name, display)
        self.supported_theorem.append(MillmanTheorem)

    def get_symbol(self):
        return I*Symbol(self.name)*Symbol('w')


class Capacitor(Dipole):
    def __init__(self, name, display=[]):
        Dipole.__init__(self, name, display)
        self.supported_theorem.append(MillmanTheorem)

    def get_symbol(self):
        return 1 / (I*Symbol(self.name)*Symbol('w'))


class VoltageGenerator(Dipole):
    def __init__(self, name, display=[]):
        Dipole.__init__(self, name, display)
        self.supported_theorem.append(TerminalRelation)

    def get_symbol(self):
        return Symbol(self.name)

    def get_terminal_relation(self):
        return Eq(self.connections[1].symbol,
                  self.connections[0].symbol + self.symbol)
