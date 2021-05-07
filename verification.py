# from Bnetwork import Bnetwork
# import numpy as np

class verification:

    def __init__(self,network):
        self.network = network

    def is_cyclic(self):
        for name, node in self.network.node_list.items():
            visited = {key: False for key, value in self.network.node_list.items()}
            if self.dfs(self.network.node_list[name], visited):
                return True
        return False

    def dfs(self, node, visited):
        if not visited[node.name]:
            visited[node.name] = True
            for child in node.children_list:
                if self.dfs(self.network.node_list[child], visited):
                    return True
            visited[node.name] = False
            return False
        else:
            return True

    def verify_data(self):
        # Check cycles
        if self.is_cyclic():
            print('Invalid data - graph is cyclic')
            quit()
        # Check probabilities
        for name, node in self.network.node_list.items():
            # sum = 0
            # if not node.parent_list:
            #     for prob_key in node.probabilities.keys():
            #         sum += node.probabilities[prob_key]
            #     if sum != 1:
            #         quit()
            #
            # else:
            no_poss_states = len(node.possible_states)
            prob_list = list(node.probabilities.values())
            while prob_list:
                sum = 0
                for i in range(no_poss_states):
                    sum += prob_list.pop()
                if sum != 1:
                    print('Invalid data - incorrect probabilities')
                    quit()

            for prob_key, prob_value in node.probabilities.items():
                if not prob_key or (not prob_value or prob_value < 0 or prob_value > 1):
                    print('Invalid data - incorrect probabilities')
                    quit()

    def check_parameters(self,network,evidence,query):
        isEvidence = isQuery =False
        isValue = True

        for key in evidence.keys():
            if key in network.node_list:
                isEvidence = True
                if evidence[key] not in network.node_list[key].possible_states:
                    isValue = False

        for q in query:
            if q in network.node_list:
                isQuery = True
        if not isEvidence or not isQuery or not isValue:
            print('Invalid Evidence or Query')
            quit()
