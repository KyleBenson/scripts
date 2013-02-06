#! /usr/bin/python
#
synopsis = "sendgrid_water_jugs.py quarts_needed pot_size (pot_size)+ ..."
#
# Inputs: Integer sizes (in quarts) of water jugs.
# Outputs: List of moves needed to get the required number of quarts
#
# example: ./send_grid_water_jugs 4 3 5
#
# (c) Kyle Benson 2012

# Solves the water jugs problem. Pot_sizes should be a list.

# Represents a jug that can be filled with water, poured into another jug,
# have another jug poured into it, or dumped out.

import sys
from copy import deepcopy
from itertools import permutations
from heapq import *

class Jug:
    def __init__(self, capacity, water_level=0):
        self.capacity = capacity
        self.water_level = water_level

    def __str__(self):
        return '%d/%d' % (self.water_level,self.capacity)

    def __repr__(self):
        return self.__str__()

    def fill(self):
        self.water_level = self.capacity

    def dump_out(self):
        self.water_level = 0;

    def pour_into(self, other_jug):
        water_poured = min(self.water_level,
                           other_jug.capacity - other_jug.water_level)
        self.water_level -= water_poured
        other_jug.water_level += water_poured

    def is_empty(self):
        return self.water_level == 0

    def is_full(self):
        return self.water_level == self.capacity

# This represents a state of the water jug problem. It contains Jugs.
# The states are comparable using the '<' operator, which is based on their
# estimated distance to the goal state.
class JugState:
    def __init__(self, target, jugs=[]):
        self.jugs = jugs
        self.target = target
        self.goal_distance = -1
        self.goal_achieved = False
        self.actions = []
        self.update_distance()

    def __repr__(self):
        return "Target = %d\nDistance = %d\n%s" % (self.target,self.goal_distance,self.jugs)

    def __str__(self):
        return ','.join([str(jug.water_level) for jug in self.jugs])

    # Heuristic for searching the state space with an A* search.
    # Will require at least 2 steps if only one jug has water, otherwise
    # at least 2 steps.
    # I ignore the trivial case of one jug having the right capacity as it will
    # be quickly found while exploring the state space.
    def update_distance(self):
        jugs_with_water = 0
        for jug in self.jugs:
            if jug.water_level == self.target:
                self.goal_achieved = True
                self.goal_distance = len(self.actions)
                return
            if not jug.is_empty():
                jugs_with_water += 1
        
        self.goal_distance = len(self.actions) + (2 if jugs_with_water <= 1 else 1)

    # Define '<' operator for use in heapq
    def __lt__(self, other):
        return self.goal_distance < other.goal_distance

    # Returns a list of deep copies of the current state, where each new element
    # has had one of the possible jug actions performed.  It will NOT return
    # a state in which all jugs are empty.
    # The argument is a dictionary mapping of string representations of states
    # that have already been explored and therefore should not be returned.
    def expand(self,explored_states):
        new_states = []

        for i in range(len(self.jugs)):
            if not self.jugs[i].is_full():
                next_state = deepcopy(self)
                next_state.jugs[i].fill()

                if str(next_state) not in explored_states:
                    next_state.update_distance()
                    next_state.actions.append(['fill',i])
                    new_states.append(next_state)
                    explored_states[str(next_state)] = True

            if not self.jugs[i].is_empty():
                next_state = deepcopy(self)
                next_state.jugs[i].dump_out()

                if str(next_state) not in explored_states:
                    next_state.update_distance()
                    next_state.actions.append(['dump',i])
                    new_states.append(next_state)
                    explored_states[str(next_state)] = True

        # Find all unexplored combinations of pouring one jug into another.
        for (i,j) in permutations(range(len(self.jugs)),2):
            if not self.jugs[i].is_empty() and not self.jugs[j].is_full():
                next_state = deepcopy(self)
                next_state.jugs[i].pour_into(next_state.jugs[j])

                if str(next_state) not in explored_states:
                    next_state.update_distance()
                    next_state.actions.append(['pour',i,j])
                    new_states.append(next_state)
                    explored_states[str(next_state)] = True

        return new_states

# Create a new water jugs problem and solve it using a heapq to order the
# problem states, thereby exploring 'closer' states first.
# Returns the final JugState.
def water_jugs(quarts_needed, pot_sizes):
    jugs = [Jug(size) for size in pot_sizes]
    states = [JugState(quarts_needed,jugs)]
    explored_states = {str(states[0]) : True}
    
    while not states[0].goal_achieved:
        for new_state in heappop(states).expand(explored_states):
            heappush(states,new_state)
            
    return states[0]
    
# Formats the actions taken to reach the final state nicely on separate lines.
def format_answer(final_state):
    answer = []
    capacities = [jug.capacity for jug in final_state.jugs]
    for action in final_state.actions:
        if action[0] == 'dump':
            answer.append('Dump the %d-quart pot out.' % capacities[action[1]])
        elif action[0] == 'fill':
            answer.append('Fill the %d-quart pot completely.' % capacities[action[1]])
        elif action[0] == 'pour':
            answer.append('Pour the %d-quart pot into the %d-quart one.' % 
                          (capacities[action[1]], capacities[action[2]]))

    for (i,jug) in enumerate(final_state.jugs):
        if jug.water_level == final_state.target:
            answer.append('The %d-quart pot has %d quarts in it so get cooking!' % 
                          (capacities[i],final_state.target))
    return '\r\n'.join(answer)
    
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Not enough arguments (need at least 3). Follow this format:\n%s" % synopsis
        sys.exit(-1)

    quarts_needed = int(sys.argv[1])
    pot_sizes = [int(x) for x in sys.argv[2:]]

    answer = water_jugs(quarts_needed, pot_sizes)
    print format_answer(answer)
