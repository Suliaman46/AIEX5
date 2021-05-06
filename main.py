import json
from node import Node
from Bnetwork import Bnetwork
from collections.abc import Iterable

f = open('alarm.json')
data = json.load(f)

network = Bnetwork()

# for i in data:
#     if i =='relations':
#         for j in data[i]:
#             network.add_node(j)
    # else:
    #     for key,value in data[i].items():
    #         if isinstance(value,dict):
    #             print('hi')



for key,value in data.items():
    if key == 'nodes':
        pass
        # for i in value:
        #     network.add_node(i)
    else:
        if isinstance(value,dict):
            for key_n,value_n in value.items():
                # print(key_n)
                # print(value_n)
                # print('next')
                new_node = Node(key_n)
                for key_node,value_node in value_n.items():
                    # print(key_new)
                    # print(value_new)
                    # print('next')
                    if key_node == 'parents':
                        if value_node:
                            new_node.parent_list = value_node
                    else:
                        # for key_prob, value_prob in value_node.items():
                            # print(key_prob)
                            # print(value_prob)
                            # print('next')
                        new_node.probabilities = value_node
                network.add(new_node)
                # print(type(value_n))

for node in network:
    if  node.parent_list:
        for parent in node.parent_list:
            network.get_node(parent).children.append(node)

print(network)


