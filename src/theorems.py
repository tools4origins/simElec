from sympy import Eq

from src.component_structures import *


class Theorem:
    def support(self, target):
        if not isinstance(target, self.target_class):
            return False

        if self.target_class == Wire:
            return (False not in [ component.support(self, target)
                                   for component in target.connections ])
        elif self.target_class == Component:
            return target.support(self, target)


class MillmanTheorem(Theorem):
    def __init__(self):
        self.target_class = Wire

    def apply(self, wire):
        numerator_terms = []
        denominator_terms = []
        for component in wire.connections:
            if 'millman_term' in dir(component):
                millman_term = component.millman_term
            else:
                millman_term = self.millman_term

            numerator_terms.append(millman_term(wire, component))
            denominator_terms.append(1 / component.symbol)

        return [ Eq(wire.symbol,
                    sum(numerator_terms) / sum(denominator_terms)) ]

    def millman_term(self, wire, component):
        if wire in component.connections:
            if wire == component.connections[0]:
                oppositeWire = component.connections[1]
            elif wire == component.connections[1]:
                oppositeWire = component.connections[0]
            else:
                raise Exception("Millman ne peut pas s'appliquer à cette borne")

            return oppositeWire.symbol / component.symbol
        else:
            raise Exception("Recherche d'un terme de millman "
                             "pour un composant ne touchant pas le fil")


class TerminalRelation(Theorem):
    def __init__(self):
        self.target_class = Component

    def apply(self, component):
        return [component.get_terminal_relation()]

theorem_list = [MillmanTheorem(), TerminalRelation()]
