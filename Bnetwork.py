from node import Node
import numpy as np
import random
import json
# ITERATIONS = 1000


class Bnetwork:

    def __init__(self,address,iterations):
        self.iterations = iterations
        self.node_list = {}
        self.load(address)

    def load(self,address):
        f = open(address)
        data = json.load(f)

        for key, value in data.items():
            if key == 'nodes':
                for name in value:
                    new_node = Node(name)
                    self.add(new_node, name)
            else:
                for key_n, value_n in value.items():
                    temp = self.node_list[key_n]
                    for key_node, value_node in value_n.items():
                        if key_node == 'parents':
                            temp.parent_list = value_node
                            for parent in temp.parent_list:
                                self.node_list[parent].children_list.append(temp.name)
                        else:
                            temp.probabilities = value_node
        self.init()

    def add(self, node, name):
        self.node_list[name] = node

    def init(self):
        for name, node in self.node_list.items():
            self._init_blanket(node)
            # self.normalize_prob(node)
            node.set_possible_states()

    def _init_blanket(self, node):
        self._init_markov(node)

    def _init_markov(self, node):
        node.markov_blanket.extend(node.parent_list)
        node.markov_blanket.extend(node.children_list)
        for child in node.children_list:
            for parent in self.node_list[child].parent_list:
                if parent not in node.markov_blanket and parent != node.name:
                    node.markov_blanket.append(parent)

    def print_blanket(self, name_a):
        for name, node in self.node_list.items():
            if name == name_a:
                node.print_blanket()

    def __repr__(self):
        return str(self.node_list)

    def calc_markov(self, node):
        string = ''
        for parent in node.parent_list:
            string += self.node_list[parent].state + ','
        string += node.state
        for prob_key, prob_val in node.probabilities.items():
            if prob_key == string:
                return prob_val

    def beta_markov_sampling(self,node):
        markov_sampled_list = {}
        children_product = 1
        denom_sum = 0
        for child in node.children_list:
            children_product *= self.calc_markov(self.node_list[child])

        for state in node.possible_states:
            prob_given_parents = self.beta_calc_markov(node,state)
            markov_sampled_list[state] = (prob_given_parents*children_product)
            denom_sum += markov_sampled_list[state]

        alpha = 1/(denom_sum)
        #
        for key in markov_sampled_list.keys():
            markov_sampled_list[key] = markov_sampled_list[key] * alpha
        return markov_sampled_list

    def beta_calc_markov(self,node,state):
        string = ''
        for parent in node.parent_list:
            string += self.node_list[parent].state + ','
        if state == node.state:
            string += node.state
        else:
            string += state

        for prob_key, prob_val in node.probabilities.items():
            if prob_key == string:
                return prob_val

    def beta_mcmc(self,evidence,query):
        counters = {}
        others = {}
        state_dic = {}
        for name, node in self.node_list.items():

            if name in evidence:          # set evidence
                node.set_state(evidence[name])
            else:
                # node.set_state(np.random.choice(node.possible_states))
                node.set_state(random.choice(node.possible_states))
                others.update({name: node})
            if name in query:             # set counters
                for state in node.possible_states:
                    state_dic.update({state:0})
                counters.update({node.name:state_dic})

        for i in range(self.iterations):       # random walking
            y = np.random.choice(list(others.keys()))   #Randomly choosing one of the nodes not in the evidence
            x = self.node_list[y]

            prob_dict = self.beta_markov_sampling(x)
            chosen_state = np.random.choice(list(prob_dict.keys()),p = list(prob_dict.values()))

            if isinstance(chosen_state,str):
                x.set_state(chosen_state)
            else:
                x.set_state(chosen_state[0])

            # updating the counters
            for name in query:
                val = self.node_list[name].state
                counters[name][val]+=1

        #Normalizing the counters
        for key, value in counters.items():
            for state_key,state_value in value.items():
                value.update({state_key:state_value/self.iterations})
        return counters


