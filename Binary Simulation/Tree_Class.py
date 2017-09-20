class BinaryTree():
    def __init__(self, data, level_number, left_child = None, right_child = None):
        self.node_number = data
        self.Level = level_number
        self.root_node_number = None
        self.left_child = left_child
        self.right_child = right_child

    def Get_Node_Number(self):
        return self.node_number

    def Get_Left_Child_Node(self):
        return self.left_child

    def Get_Right_Child_Node(self):
        return self.right_child

    def Set_Node_Number(self, data):
        self.node_number = data

    def Append_Left_Child_Node(self, sub):
        self.left_child = sub

    def Append_right_Child_Node(self, sub):
        self.right_child = sub

    def preorder_traverse(tree):
        if tree == None: return
        print(tree.node_number)
        preorder_traverse(tree.left_child)
        preorder_traverse(tree.right_child)
