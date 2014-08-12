from string import ascii_letters

from sympy import Symbol

from src.components import *

class Circuit:
    def __init__(self):
        self.initialize()
        print("Circuit créé avec succès")

    def initialize(self):
        self.components = []
        self.wires = []
        self._wires_named = 0

    def example_circuit(self):
        self.initialize()

        coordTestE = [[2,0], [3,0]]
        coordTestR1 = [[1,4], [2,4]]
        coordTestR2 = [[3,4], [4,4]]
        coordTestR3 = [[5,4], [6,4]]
        coordTestFil1 = [[2,0], [0,0], [0,4], [1,4]]
        coordTestFil2 = [[2,4], [2,4], [3,4], [4,4]]
        coordTestFil3 = [[4,4], [4,4], [5,4], [5,4]]
        coordTestFil4 = [[5,4], [7,4], [7,0], [3,0]]

        E = VoltageGenerator('E', coordTestE)
        R1 = Resistor('R1', coordTestR1)
        R2 = Resistor('R2', coordTestR2)
        R3 = Resistor('R3', coordTestR3)
        A = Wire(self, coordTestFil1)
        B = Wire(self, coordTestFil2)
        C = Wire(self, coordTestFil3)

        self.addComponent(E)
        self.addComponent(R1)
        self.addComponent(R2)
        self.addComponent(R3)

        self.addWire(A)
        self.addWire(B)
        self.addWire(C)

        self.connect(R1, 0, A)
        self.connect(R1, 1, B)

        self.connect(R2, 0, B)
        self.connect(R2, 1, C)

        self.connect(R3, 0, B)
        self.connect(R3, 1, C)

        self.connect(E, 0, A)
        self.connect(E, 1, C)

    def generate_wire_name(self):
        alphabet = ascii_letters[26:]
        
        num = self._wires_named
        name = alphabet[num % 26]

        while num >= 26:
            num //= 26
            name = alphabet[num%26 - 1] + name

        self._wires_named += 1

        return name

    def connect(self, component, terminal, wire):
        component.add_connections(wire, terminal)

        wire.connections.append(component)
        print("Liaison créée")

    def addComponent(self, component):
        self.components.append(component)

    def removeComponent(self, deleted_component):
        self.components.remove(deleted_component)
        for wire in self.wires:
            component = find_component_by_name(wire.connections,
                                               deleted_component.name)
            if component is not None:
                wire.connections.remove(component)

    def addWire(self, wire):
        self.wires.append(wire)

    def removeWire(self, wire):
        self.wires.remove(wire)
        for component in self.components:
            terminal = find_terminal_by_wire_name(component.connections.items(),
                                                  wire.name)
            if terminal is not None:
                del component.connections[terminal]


def find_wire_by_name(wire_list, wire_name):
    for wire in wire_list:
        if wire.name == wire_name:
            return wire

def find_terminal_by_wire_name(wire_dict_values, wire_name):
    for terminal, wire in wire_dict_values:
        if wire.name == wire_name:
            return terminal

def find_component_by_name(component_list, component_name):
    for component in component_list:
        if component is None:
            continue

        if component.name == component_name:
            return component
