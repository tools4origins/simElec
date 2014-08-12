from sympy import Symbol

class Wire:
    def __init__(self, circuit, display=[]):
        self.circuit = circuit
        self.display = display
        self.connections = []
        self.name = self.circuit.generate_wire_name()
        self.symbol = Symbol("P_" + self.name)
        print('Fil nommé', self.name, 'créé')


class Component:
    def __init__(self, name, display):
        self.name = name
        self.display = display
        self.symbol = self.get_symbol()
        self.supportedTheorem = []
        print("Composant de valeur", self.name, "créé")

    def support(self, theoremUsed, target):
        return (True in [ isinstance(theoremUsed, theorem)
                          for theorem in self.supportedTheorem ])


class Dipole(Component):
    def __init__(self, name, display):
        Component.__init__(self, name, display)
        self.connections = [None] * 2
    
    def add_connections(self, wire, terminal):
        if(terminal in range(2)):
            if self.connections[terminal] is not None:
                print("Erreur : deux fils sur la même borne, non supporté")
            else:
                self.connections[terminal] = wire
