from node import Node
import numpy as np
from numpy import random

class Bnetwork:
    def __init__(self):
        self.size = 0
        self.node_list = {}
    def add(self,node,name):
        self.node_list[name] = node

    def init(self):
        for name, node in self.node_list.items():
            self._init_blanket(node)
            self.normalize_prob(node)
            node.set_possible_states()

    def normalize_prob(self,node):

        if node.parent_list:
            sum_p = sum(node.probabilities.values())
           # for prob_key,prob_value in node.probabilities.items():
           #     prob_value = prob_value/sum
            node.normalized_probabilities = {key:value/sum_p for key,value in node.probabilities.items()}
        else:
            node.normalized_probabilities = node.probabilities
    def _init_blanket(self,node):
        self._init_markov(node)


    def _init_markov(self, node):
        node.markov_blanket.extend(node.parent_list)
        node.markov_blanket.extend(node.children_list)
        for child in node.children_list:
            for parent in self.node_list[child].parent_list:
                if parent not in node.markov_blanket and parent != node.name:
                    node.markov_blanket.append(parent)


    def print_blanket(self,name_a):
        for name,node in self.node_list.items():
            if name == name_a:
                node.print_blanket()
                return
    def __repr__(self):
        return str(self.node_list)

    def test(self,name_a):
        for name,node in self.node_list.items():
            if name == name_a:
                node.set_possible_states()
                return
    def mcmc(self,evidence):
        pas
        # # #Setting the evidence
        for name,node in self.node_list.items():
            if name in evidence:
                node.set_value(evidence[name])
            else:
                prob_T = 0
                prob_F = 0
                for prob_state,prob_val in node.normalized_probabilities.items():
                    if prob_state[len(prob_state)-1] =='T':
                        prob_T += prob_val
                    else:
                        prob_F += prob_val

                prob_ar = [prob_T,prob_F]
                node.set_value(np.random.choice(node.possible_states,p=prob_ar))

        count_T =0
        count_F = 0

        



