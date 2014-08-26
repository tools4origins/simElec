from cmd import Cmd

from src.circuit import *
from src.simulation import *


class CLI(Cmd):
    def __init__(self):
        self.prompt = '> '
        Cmd.__init__(self)
        self.circuit = Circuit()
        self.display = print

        self.cmdloop('')

    def do_quit(self, args):
        """Quitte le programme"""
        print("Au revoir :)")
        raise SystemExit

    do_q = do_quit

    def do_add_component(self, args):
        """Ajoute un composant"""

        args = args.split(' ', 1)
        component_class = args[0]
        component_name = args[1]

        component_classes = {
            "g" : VoltageGenerator,
            "r" : Resistor,
            "l" : Inductor,
            "c" : Capacitor,
        }

        component = component_classes[args[0]](args[1])
        self.circuit.add_component(component)

    do_ac = do_add_component

    def do_add_wire(self, args):
        """Ajoute un fil"""
        wire = Wire(self.circuit, [])
        self.circuit.add_wire(wire)

    do_aw = do_add_wire

    def do_connect(self, args):
        """Connecte un composant et un fil"""

        args = args.split(' ', 2)
        wire_name = args[0]
        component_name = args[1]
        component_terminal = int(args[2])

        wire = Circuit.find_wire(self.circuit.wires, wire_name)
        component = Circuit.find_component(self.circuit.components,
                                           component_name)
        if wire is not None and component is not None:
            self.circuit.connect(component, component_terminal, wire)

    do_c = do_connect

    def do_delete_component(self, args):
        """Supprime un composant"""

        args = args.split(' ', 0)
        component_name = args[0]

        component = Circuit.find_component(self.circuit.components,
                                           component_name)
        self.circuit.remove_component(component)

    do_dc = do_delete_component

    def do_delete_wire(self, args):
        """Supprime un fil"""

        args = args.split(' ', 0)
        wire_name = args[0]
        wire = Circuit.find_wire(self.circuit.wires, wire_name)
        self.circuit.remove_wire(wire)

    do_dw = do_delete_wire

    def do_init(self, args):
        """Initialise un nouveau circuit"""
        self.circuit = Circuit()

    do_i = do_init

    def do_describe(self, args):
        """Liste les composants et les fils du circuit"""
        wires = self.circuit.wires
        components = self.circuit.components

        print(len(wires), "fils")
        for wire in wires:
            self.display("Fil", wire.name, "lié à",
                          [ component.name
                            for component in wire.connections ])

        print("")
        print(len(components), "composants")
        for component in components:
            self.display("Composant de type", component.type,
                         "et de valeur", component.name, "lié à",
                         [ wire.name if wire is not None else "~"
                          for wire in component.connections ])

    do_d = do_describe
    do_ls = do_describe

    def do_example_circuit(self, args):
        """Remplace le circuit actuel par un circuit de démonstration"""
        self.circuit.example_circuit()

    def do_simulate(self, args):
        """Simule le circuit"""
        self.simulation = Simulation(self.circuit)

    do_s = do_simulate
