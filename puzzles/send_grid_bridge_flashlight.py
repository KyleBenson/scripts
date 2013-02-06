#! /usr/bin/python
#
synopsis = "sendgrid_bridge_flashlight.py hiker_name crossing_time (hiker_name crossing_time)+ ..."
#
# Inputs: Alternating list of hiker name/crossing time combinations
# Outputs: hiker names that should cross at each step
#
# example: ./send_grid_bridge_flashlight.py Kyle 1 Michelle 2 Joe 5 Robin 10
#
# (c) Kyle Benson 2012

import sys
from heapq import *
from itertools import combinations

# Solves the problem of getting hikers across a bridge two at a time where a flashlight is needed at each crossing.
# Hikers is a list of names and crossing_times is a dictionary of the same names
# that maps to the number of minutes it takes that hiker to cross the bridge.
#
# The search space will be a priority queue ordered by an admissible heuristic
# for an A* search, the sum of the current shortest path and the minimum
# additional time required to get everyone across.
# Each element of the heap is a list containing a possible state of the problem.
# Each state contains the following: total_time, hikers_left, hikers_crossed, monves made
#
# Returns: list of moves made where each move is a round of sending hikers
# across and then (maybe) one back
def bridge_crossing(hikers, crossing_times):
    state_space = [[0, hikers[:], [], [],0]]

    while True:# len(state_space[0][1]) > 0:
        state = heappop(state_space)
        this_side = state[1]
        other_side = state[2]

        if len(this_side) <= 2:
            return state[3] + [[this_side,None]]
        
        else:
            for possible_crossers in combinations(this_side,2):
                for [returned_hiker,crossed_hiker] in [possible_crossers,sorted(possible_crossers)]:
                    new_this_side = [[crossing_times[hiker],hiker] for hiker in this_side if hiker != crossed_hiker]
                    new_this_side.sort(reverse=True)
                    min_time = 0

                    # At least every other hiker (when ordered) will have to cross
                    for i in range(0,len(new_this_side),2):
                        min_time += new_this_side[i][0]

                    # We also have to wait for at least the fastest hiker to 
                    # return with the flashlight len(this_side) - 2 times
                    min_time += (len(new_this_side) - 2) * new_this_side[-1][0]
                    
                    new_crossing_time = state[4] + max(crossing_times[returned_hiker],
                                                       crossing_times[crossed_hiker]) + crossing_times[returned_hiker]
                    heappush(state_space,
                             [new_crossing_time + min_time,
                              [hiker for [time,hiker] in new_this_side],
                              other_side + [crossed_hiker],
                              state[3] + [[possible_crossers,returned_hiker]],
                              new_crossing_time])

# Format the answer as a nice string giving the total minimum time to cross and
# describing each step on separate lines.
def format_answer(moves):
    answer = []
    time = 0
    for move in moves:
        answer.append("%s and %s cross the bridge." % (move[0][0], move[0][1]))
        time += max(crossing_times[x] for x in move[0])
        if move[1] != None:
            answer.append("%s returns with the flashlight." % move[1])
            time += crossing_times[move[1]]
    answer = ["The minimum time needed to cross the river is %d minutes." % time] + answer
    return "\r\n".join(answer)

##########################################################################
if __name__ == "__main__":                             
    argc = len(sys.argv)

    if argc < 5 or argc % 2 != 1:
        print "Invalid number of arguments.  Follow form:\n", synopsis
        sys.exit(-1)

    hikers = [sys.argv[i] for i in range(1, argc, 2)]
    crossing_times = {x : y for (x,y) in zip(hikers, [int(sys.argv[i]) for i in range(2, argc+1, 2)])}

    answer = bridge_crossing(hikers, crossing_times)
    print format_answer(answer)
    
