from sympy import Symbol

class Wire:
    def __init__(self, circuit, display=[]):
        self.circuit = circuit
        self.display = display
        self.connections = []
        self.name = self.circuit.generate_wire_name()
        self.symbol = Symbol("P_" + self.name)
        print('Fil nommé', self.name, 'créé')

    def merge(self, wire):
        self.connections += wire.connections
        self.display += wire.display
        for component in wire.connections:
            component.connections = [ self if w == wire else w
                                      for w in component.connections ]

class Component:
    def __init__(self, name, display):
        self.name = name
        self.display = display
        self.symbol = self.get_symbol()
        self.supported_theorem = []
        print("Composant de valeur", self.name, "créé")

    def support(self, theorem_used, target):
        return (True in [ isinstance(theorem_used, theorem)
                          for theorem in self.supported_theorem ])


class Dipole(Component):
    def __init__(self, name, display):
        Component.__init__(self, name, display)
        self.connections = [None] * 2
    
    def add_connections(self, wire, terminal):
        if terminal in range(2):
            if (self.connections[terminal] is not None and
                    self.connections[terminal] != wire):
                print("Attention : deux fils sur la même borne.\n"
                      "Fil", wire.name, "supprimé")
                self.connections[terminal].merge(wire)
                wire.circuit.wires.remove(wire)
            else:
                self.connections[terminal] = wire

