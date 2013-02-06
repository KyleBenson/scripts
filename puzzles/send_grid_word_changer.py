#! /usr/bin/python
#
synopsis = "./send_grid_word_changer start_word end_word"
#
# Solves the word changing problem. Arguments should be start and end word.
# Input cases don't matter, everything will be capitalized.
#
# example: ./send_grid_word_changer SEND GRID"
#
# (c) Kyle Benson 2012

import sys
from copy import deepcopy
from heapq import *
from string import uppercase as possible_letters

word_dictionary = "4letter.words"
def read_word_dictionary():
    return {word.strip().upper() : False for word in open(word_dictionary).readlines()}

# This class represents a state of the word changer problem.
# It is comparable with others of its type so that the states can be placed
# in a priority queue for the purposes of efficienty searching the state space.
class MorphWord:
    def __init__(self,start_word,target_word):
        self.word = start_word
        self.target = target_word
        self.actions = [start_word]
        self.goal_distance = -1
        self.update_distance()

    def __str__(self):
        return self.word

    def __repr__(self):
        return self.__str__()

    # For comparison in a heapq
    def __lt__(self,other):
        return self.goal_distance < other.goal_distance

    # An estimate of the distance from the goal word. Is simply the number of
    # letters different from the goal word.
    def update_distance(self):
        distance = len(self.actions)
        for (letter1, letter2) in zip(self.word,self.target):
            if letter1 != letter2:
                distance += 1

        self.goal_distance = distance

    # Returns a list of all MorphWords that can be made from the current word
    # and that have not been explored yet, as represented by a 'True' entry
    # in the input dictionary of valid words.
    def expand(self,valid_words):
        new_states = []
        for i in range(len(self.word)):
            for let in possible_letters:
                new_word = self.word[:i] + let + self.word[i+1:]
                if new_word in valid_words and not valid_words[new_word]:
                    next_state = deepcopy(self)
                    next_state.word = new_word
                    next_state.actions.append(new_word)
                    next_state.update_distance()
                    new_states.append(next_state)
                    valid_words[new_word] = True

        return new_states

# Takes two words as input and finds a way to transform one to the other by
# only changing one letter at a time so that each in between word is found
# in the dictionary of words defined in this file.
def word_changer(start_word, end_word):
    # Store whether this valid word has been reached yet or not.
    valid_words = read_word_dictionary()
    end_word = end_word.upper()
    states = [MorphWord(start_word.upper(),end_word)]

    while str(states[0]) != end_word:
        for i in heappop(states).expand(valid_words):
            heappush(states,i)

    return states[0]

# Formats the word transitions nicely on separate lines
def format_answer(final_state):
    answer = []
    for move in final_state.actions:
        answer.append(move)

    return '\r\n'.join(answer)

##################################################################
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Must provide two words, like this:\n%s" % synopsis
        sys.exit(-1)

    start_word = sys.argv[1]
    end_word = sys.argv[2]

    answer = word_changer(start_word,end_word)
    print format_answer(answer)
