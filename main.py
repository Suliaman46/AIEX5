import json
from node import Node
from Bnetwork import Bnetwork
import numpy as np

from collections.abc import Iterable


def verify_data(network):
    # Check Probabilities
    for name, node in network.node_list.items():
        sum = 0
        if not node.normalized_probabilities:
            print("Invalid Data")
            # Do something exityyy
        for prob_key, prob_value in node.normalized_probabilities.items():
            if not prob_key and (not prob_value or prob_value < 0 or prob_value > 1):
                print('Invalid Data')
                # Do something exityyy
            sum += prob_value
        if sum != 1:
            print('Invalid Data')
            # Do something exityyy


f = open('alarm.json')
# f = open('flower.json')
data = json.load(f)

network = Bnetwork()

for key,value in data.items():
    if key == 'nodes':
        for name in value:
            new_node = Node(name)
            network.add(new_node,name)
    else:
        for key_n,value_n in value.items():
            temp = network.node_list[key_n]
            for key_node,value_node in value_n.items():
                if key_node == 'parents':
                    temp.parent_list = value_node
                    for parent in temp.parent_list:
                        network.node_list[parent].children_list.append(temp.name)
                else:
                    temp.probabilities = value_node

network.init()
# network.print_blanket('earthquake')
# verify_data(network)
#network.test('flower_species')
# network.mcmc({"color":"red"})
answer = network.mcmc(evidence={"burglary":"T"}, query=["John_calls"])
print(answer)
answer = network.mcmc(evidence={"burglary":"T", "alarm": "T"},query=["earthquake"])
print(answer)

