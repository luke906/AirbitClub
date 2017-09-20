class binarytree(object):
    def __init__(self, data, level_number, left_child = None, right_child = None, parent = None):
        self.node_number      = data
        self.level            = level_number
        self.root_node_number = None
        self.left_child       = left_child
        self.right_child      = right_child
        self.parent_node      = parent

    # R:추천수당  S:후원수당  M:매트릭스 보너스

    def Set_Parent_Node(self, node):
        self.parent_node = node

    def Get_Parent_Node(self, node):
        return self.parent_node

    def Set_R_Money(self, money):
        self.r_money = money

    def Set_S_Money(self, money):
        self.s_money = money

    def Set_M_Money(self, money):
        self.m_money = money

    def Get_R_Money(self, money):
        return self.r_money

    def Get_S_Money(self, money):
        return self.s_money

    def Get_M_Money(self, money):
        return self.m_money

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


