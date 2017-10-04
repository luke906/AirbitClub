class BinaryTree(object):
    def __init__(self, node_number,
                        node_create_index,
                        node_level_number,
                        parent_node_number=None,
                        parent=None,
                        left_child=None,
                        right_child=None):
        self.node_number = node_number
        self.create_index = node_create_index
        self.level = node_level_number
        self.parent_node = parent
        self.parent_node_number = parent_node_number

        self.left_child = left_child
        self.left_child_have = False

        self.right_child = right_child
        self.right_child_have = False

        self.daily_money = 0
        self.r_money     = 0
        self.s_money     = 0
        self.m_money     = 0

    # R:추천수당  S:후원수당  M:매트릭스 보너스

    def set_parent_node(self, node):
        self.parent_node = node

    def get_parent_node(self):
        return self.parent_node

    def set_daily_money(self, money):
        self.daily_money = money

    def set_r_money(self, money):
        self.r_money = money

    def set_s_money(self, money):
        self.s_money = money

    def set_m_money(self, money):
        self.m_money = money

    def get_daily_money(self):
        return self.daily_money

    def get_r_money(self):
        return self.r_money

    def get_s_money(self):
        return self.s_money

    def get_m_money(self):
        return self.m_money

    def set_node_number(self, data):
        self.node_number = data

    def get_node_number(self):
        return self.node_number

    def set_left_child_node(self, sub):
        self.left_child = sub
        self.left_child_have = True

    def get_left_child_node(self):
        return self.left_child

    def set_right_child_node(self, sub):
        self.right_child = sub
        self.right_child_have = True

    def get_right_child_node(self):
        return self.right_child

    def preorder_traverse(self, tree, action):
        if tree == None:
            return
        action(tree.node_number)
        preorder_traverse(tree.Get_Left_Child_Node(), action)
        preorder_traverse(tree.Get_Right_Child_Node(), action)

    def showintdata(self, data):
        print(data)