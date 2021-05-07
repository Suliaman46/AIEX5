class Node:
    def __init__(self, name):
        self.name = name
        self.parent_list = []
        self.children_list = []
        self.probabilities = {}
        self.markov_blanket = []
        self.possible_states = []
        self.state = None

    def print_blanket(self):
        print(self.markov_blanket)

    def set_state(self, state):
        self.state = state

    def get_node(self):
        return self

    def set_possible_states(self):
        for key, val in self.probabilities.items():
            string = key.split(',')
            if not string[-1] in self.possible_states:
                self.possible_states.append(string[-1])

    def __repr__(self):
        # return '  Parents - ' + str(self.parent_list) + ' Children - ' + str(self.children_list) + '\n'
        return (self.name +' - ' + self.state + '\n')
        # final_string = self.name
        # final_string += ' Parent List ->  '
        # for node in self.parent_list:
        #     final_string+= (' '+ node.name + ' ')
        # final_string += '\n'
        # final_string += ' Children List ->  '
        # for node in self.children_list:
        #     final_string+= (' '+ node.name + ' ')
        # final_string += '\n'
        # return final_string
