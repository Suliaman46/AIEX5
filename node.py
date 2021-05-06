class Node:
    def __init__(self,name):
        self.name = name
        self.parent_list = []
        self.children_list = []
        self.probabilities ={}
    # def set_parents(self,p_list):
    #     self.parent_list = p_list
    # def set_children(self,c_list):
    #     self.children_list = c_list


    def set_value(self,value):
        self.value = value
    def get_node(self):
        return self
    def set_possible_value(self,poss_val):
        self.possible_value = poss_val
    def __repr__(self):
        return (self.name + '  Parents - '+ str(self.parent_list)+ ' Children - ' + str(self.children_list) + '\n')
