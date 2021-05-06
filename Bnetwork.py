from node import Node

class Bnetwork:
    def __init__(self):
        self.size = 0
        self.node_list = []
    def add(self,node):
        self.node_list.append(node)
    def add_node(self,name):
        node = Node(name)
        self.node_list.append(node)
    def get_node(self,name):
        for i in self.node_list:
            if i.name == name:
                return i


    def __repr__(self):
        return str(self.node_list)
