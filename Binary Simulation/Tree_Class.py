class binarytree(object):
    def __init__(self, data, level_number, left_child = None, right_child = None):
        self.node_number      = data
        self.Level            = level_number
        self.root_node_number = None
        self.left_child       = left_child
        self.right_child      = right_child

    def Set_Node_Number(self, data):
        self.node_number = data

    def Get_Node_Number(self):
        return self.node_number


    def Set_Left_Child_Node(self, sub):
        self.left_child = sub

    def Get_Left_Child_Node(self):
        return self.left_child


    def Set_right_Child_Node(self, sub):
        self.right_child = sub

    def Get_Right_Child_Node(self):
        return self.right_child


def preorder_traverse(tree, action):
    if tree == None:
        return

    action(tree.node_number)
    preorder_traverse(tree.Get_Left_Child_Node(), action)
    preorder_traverse(tree.Get_Right_Child_Node(), action)

def ShowIntData(data):
    print(data)


