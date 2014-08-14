from src.circuit import *
from src.simulation import *


class CLI():
    def __init__(self):
        self.circuit = Circuit()
        self.circuit.example_circuit()
        self.display = print

    def launch(self):
        while True:

            self.display("\n"
            "Indiquez quelle action vous souhaitez réaliser :\n"
            "0 : Quittez le programme.\n"
            "1 : Ajouter un générateur.\n"
            "2 : Ajouter une résistance.\n"
            "3 : Ajouter une bobine.\n"
            "4 : Ajouter un condensateur.\n"
            "5 : Ajouter un fil.\n"
            "6 : Lier un fil et un composant.\n"
            "7 : Supprimer un composant.\n"
            "8 : Supprimer un fil.\n"
            "9 : Créer un nouveau circuit.\n"
            "10 : Afficher la structure du circuit.\n"
            "11 : Utiliser le circuit d'exemple.\n"
            "12 : Nouveau circuit\n"
            "13 : Simuler !\n")
            
            user_input = input()
            if user_input == '0':
                break

            elif user_input == '1':
                name = self.prompt("Comment souhaitez-vous nommer "
                                   "la tension de votre générateur ?")
                generator = VoltageGenerator(name)
                self.circuit.add_component(generator)

            elif user_input == '2':
                name = self.prompt("Comment souhaitez-vous nommer "
                                   "la valeur de votre résistance ?")
                resistor = Resistor(name)
                self.circuit.add_component(resistor)

            elif user_input == '3':
                name = self.prompt("Comment souhaitez-vous nommer "
                                   "l'inductance de votre bobine ?")
                inductor = Inductor(name)
                self.circuit.add_component(inductor)

            elif user_input == '4':
                name = self.prompt("Comment souhaitez-vous nommer "
                                   "la capacité de votre condensateur ?")
                capacitor = Capacitor(name)
                self.circuit.add_component(capacitor)

            elif user_input == '5':
                wire = Wire(self.circuit, [])
                self.circuit.add_wire(wire)

            elif user_input == '6':
                wire_name = self.prompt("Quel est le nom du fil ?")
                wire = Circuit.find_wire(self.circuit.wires, wire_name)
                component_name = self.prompt("Quel est le nom du composant ?")
                component = Circuit.find_component(self.circuit.components,
                                                   component_name)
                terminal = self.prompt_number("Sur quel borne du composant ?")
                if wire is not None and component is not None:
                    self.circuit.connect(component, terminal, wire)

            elif user_input == '7':
                name = self.prompt("Quel est le nom du composant à supprimer ?")
                component = Circuit.find_component(self.circuit.components,
                                                   name)
                self.circuit.remove_component(component)

            elif user_input == '8':
                wire_name = self.prompt("Quel est le nom du fil à supprimer ?")
                wire = Circuit.find_wire(self.circuit.wires, wire_name)
                self.circuit.remove_wire(wire)

            elif user_input == '9':
                self.circuit = Circuit()
                
            elif user_input == '10':
                for wire in self.circuit.wires:
                    self.display("Fil", wire.name, "lié à",
                                  [ component.name 
                                    for component in wire.connections ])

                for component in self.circuit.components:
                    self.display("Composant", component.name, "lié à",
                                  [ wire.name 
                                    for wire in component.connections 
                                    if wire is not None ])
                
            elif user_input == '11':
                self.circuit.example_circuit()

            elif user_input == '12':
                self.circuit.initialize()

            elif user_input == '13':
                self.simulation = Simulation(self.circuit)

    def prompt(self, text):
        while True:
            self.display(text)
            arg = input()
            if arg != '':
                return arg

    def prompt_number(self, text):
        while True:
            self.display(text)
            arg = input()
            try:
                return int(arg)
            except:
                self.display("Vous devez indiquez un nombre")
                pass
