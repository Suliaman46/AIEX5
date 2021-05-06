from node import Node
import numpy as np

ITERATIONS = 1000


class Bnetwork:

    def __init__(self):
        self.size = 0
        self.node_list = {}

    def add(self, node, name):
        self.node_list[name] = node

    def init(self):
        for name, node in self.node_list.items():
            self._init_blanket(node)
            self.normalize_prob(node)
            node.set_possible_states()

    def normalize_prob(self, node):
        if node.parent_list:
            sum_p = sum(node.probabilities.values())
           # for prob_key,prob_value in node.probabilities.items():
           #     prob_value = prob_value/sum
            node.normalized_probabilities = {key: value/sum_p for key, value in node.probabilities.items()}
        else:
            node.normalized_probabilities = node.probabilities

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

    def test(self, name_a):
        for name, node in self.node_list.items():
            if name == name_a:
                node.set_possible_states()

    def mcmc(self, evidence, query):
        counters = {}
        others = {}
        for name, node in self.node_list.items():

            if name in evidence:          # set evidence
                node.set_state(evidence[name])
            else:
                node.set_state(np.random.choice(node.possible_states))
                others.update({name: node})
            if name in query:             # set counters
                counters.update({node.name: {'F':0,'T':0}})
                # counters.update({node.name:0})

        for i in range(ITERATIONS):       # random walking
            y = np.random.choice(list(others.keys()))
            x = self.node_list[y]
            prob = self.markov_sampling(x)
            if np.random.rand() < prob:
                for state in x.possible_states:
                    if state != x.state:
                        x.set_state(state)
                        break

            for name in query:
                val = self.node_list[name].state
                # if val == 'T':
                counters[name][val]+=1
                    # counters[name]+=1
            #
            # if x.name in query:
            #     if x.state == 'T':
            #         counters[x.name] += 1
            # else:


        # TEST
        # for name, node in self.node_list.items():
        #     print(node.name + ': ' + node.state)
        # print(others)
        # print(counters)

        for key, value in counters.items():
            # counters.update({key: value / ITERATIONS})
            for state_key,state_value in value.items():
                value.update({state_key:state_value/ITERATIONS})
        return counters

    def markov_sampling(self, node):
        product = self.calc_markov(node)
        sum = 0
        for child in node.children_list:
            sum += self.calc_markov(self.node_list[child])
        if sum == 0:
            return product
        else:
            return product * sum

    def calc_markov(self, node):
        string = ''
        for parent in node.parent_list:
            string += self.node_list[parent].state + ','
        string += node.state
        for prob_key, prob_val in node.normalized_probabilities.items():
            if prob_key == string:
                return prob_val
