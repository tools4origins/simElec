import json

from string import ascii_letters
from sympy import Symbol

from src.components import *

class Circuit:
    def __init__(self):
        self.initialize()

    def initialize(self):
        self.components = []
        self.wires = []
        self._wires_named = 0

    def example_circuit(self):
        self.initialize()

        coord_E = [[2,0], [3,0]]
        coord_R1 = [[1,4], [2,4]]
        coord_R2 = [[3,4], [4,4]]
        coord_R3 = [[5,4], [6,4]]
        coord_wire_1 = [[2,0], [0,0], [0,4], [1,4]]
        coord_wire_2 = [[2,4], [2,4], [3,4], [4,4]]
        coord_wire_3 = [[4,4], [4,4], [5,4], [5,4]]

        E = VoltageGenerator('E', coord_E)
        R1 = Resistor('R1', coord_R1)
        R2 = Resistor('R2', coord_R2)
        R3 = Resistor('R3', coord_R3)
        A = Wire(self, coord_wire_1)
        B = Wire(self, coord_wire_2)
        C = Wire(self, coord_wire_3)

        self.add_component(E)
        self.add_component(R1)
        self.add_component(R2)
        self.add_component(R3)

        self.add_wire(A)
        self.add_wire(B)
        self.add_wire(C)

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

    def add_component(self, component):
        self.components.append(component)

    def remove_component(self, deleted_component):
        self.components.remove(deleted_component)
        for wire in self.wires:
            component = Circuit.find_component(wire.connections,
                                               deleted_component.name)
            if component is not None:
                wire.connections.remove(component)

    def add_wire(self, wire):
        self.wires.append(wire)

    def remove_wire(self, wire):
        self.wires.remove(wire)
        for component in self.components:
            terminal = Circuit.find_terminal(component.connections,
                                                  wire.name)
            if terminal is not None:
                del component.connections[terminal]

    def find_wire(wire_list, wire_name):
        for wire in wire_list:
            if wire.name == wire_name:
                return wire

    def find_terminal(connections, wire_name):
        for terminal, wire in connections.items():
            if wire.name == wire_name:
                return terminal

    def find_component(component_list, component_name):
        for component in component_list:
            if component is None:
                continue

            if component.name == component_name:
                return component

    def save(self):
        print(json.dumps(self))

    def load(self, json_string):
        for key, value in json_string:
            self[key] = value
