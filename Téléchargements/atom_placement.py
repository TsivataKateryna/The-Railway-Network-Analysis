"""NAMES OF THE AUTHOR(S): Alice Burlats <alice.burlats@uclouvain.be>"""

import random
from atom_placement_state import AtomPlacementState


class AtomPlacement:

    # An init state building is provided here but you can change it at will
    def init_state(self) -> AtomPlacementState:
        sites = []
        for atom_type, quantity in enumerate(self.n_types):
            for i in range(quantity):
                sites.append(atom_type)
        
        return AtomPlacementState(sites)

    # Returns the neighbor states of the given state as a list of AtomPlacementState
    def neighbors(self, state: AtomPlacementState) -> list[AtomPlacementState]:
        actual_state = state

        all_states = []
        for _ in range (1):
            states = []
            
            for i in range (self.n_sites):
                type_i = actual_state.sites_assignment[i]
                
                for j in range (i):
                    type_j = actual_state.sites_assignment[j]
                    
                    if (type_i != type_j):
                        new_state = AtomPlacementState(actual_state.sites_assignment.copy())
                        
                        a = new_state.sites_assignment[i]
                        new_state.sites_assignment[i] = new_state.sites_assignment[j]
                        new_state.sites_assignment[j] = a
                        states.append(new_state)
                        all_states.append(new_state)
            
            
            actual_state = random.choice(list(states))

        return all_states

    # Returns the objective value of the given state
    def value(self, state: AtomPlacementState) -> int:

        sum = 0
        for i, j in self.edges:
            type_i = state.sites_assignment[i]
            type_j = state.sites_assignment[j]

            sum += self.energy_matrix[type_i][type_j]
        return sum

    def __init__(self, filename: str):
        file = open(filename)
        line = file.readline()
        self.n_sites = int(line.split(' ')[0])
        self.k = int(line.split(' ')[1])
        self.n_edges = int(line.split(' ')[2])
        self.edges = []
        file.readline()

        self.n_types = [int(val) for val in file.readline().split(' ')]
        if sum(self.n_types) != self.n_sites:
            print('Invalid instance, wrong number of sites')
        file.readline()

        self.energy_matrix = []
        for i in range(self.k):
            self.energy_matrix.append([int(val) for val in file.readline().split(' ')])
        file.readline()

        for i in range(self.n_edges):
            self.edges.append([int(val) for val in file.readline().split(' ')])



