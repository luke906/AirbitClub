class BinaryTree(object):
    def __init__(self,
                 node_number,
                 node_level_number,
                 parent_node_number=None,
                 parent=None,
                 left_child=None,
                 right_child=None):

        self.node_number = node_number
        self.level = node_level_number
        self.parent_node = parent
        self.parent_node_number = parent_node_number

        self.left_child = left_child
        self.left_child_have = False

        self.right_child = right_child
        self.right_child_have = False

        self.commision_wallet = 0  # 커미션 월릿
        self.reward_wallet = 0     # 데일리 보너스
        self.saving_wallet = 0     # 추천 후원 매트릭스 수당 발생시 20%가 차감되어 SAVING에 적립

        self.r_money          = 0  # 추천 수당
        self.s_money          = 0  # 후원 수당
        self.m_money          = 0  # 매트릭스 수당

        self.day_count = 0  # 수당을 지급하기위한 계좌 생성일 계산 (7부터 리워드 지급)

        # 후원수당 계산 적용 여부
        # 후원수당 계산시 한번 적용 되었던 노드는 다음번 계산시 적용을 시키지 않는다.
        self.support_calc_used = False

    # R:추천수당  S:후원수당  M:매트릭스 보너스

    def set_parent_node(self, node):
        self.parent_node = node

    def get_parent_node(self):
        return self.parent_node

    def set_day_count(self, day):
        self.day_count += day

    # 추천 후원 매트릭스 모든 수당을 commsion wallet으로 이동시킨다.
    def set_commision_wallet(self):
        self.commision_wallet += (self.r_money + self.s_money + self.m_money)

        self.r_money = 0
        self.s_money = 0
        self.m_money = 0

    def get_comision_money(self):  #saving 제외
        return self.commision_wallet
        # return (self.r_money + self.s_money + self.m_money)

    def set_reward_wallet(self, money=7):
        if self.day_count >= 7:
            self.reward_wallet += money

    def reset_reward_commision(self):
        self.commision_wallet = 0  # 커미션 월릿
        self.reward_wallet = 0  # 데일리 보너스

    def add_commision_wallet(self, money):
        self.commision_wallet += money

    def add_reward_wallet(self, money):
        self.reward_wallet += money

    def set_recommand_money(self, money):

        if money is not 0:
            # 20퍼센트 감소된 금액을 셋팅
            result = money - (money * 0.2)
            self.r_money += result

            # 20프로를 SAVING에 적립
            self.saving_wallet += (money * 0.2)

    def set_support_money(self, money):

        if money is not 0:
            # 20퍼센트 감소된 금액을 셋팅
            result = money - (money * 0.2)
            self.s_money += result

            # 20프로를 SAVING에 적립
            self.saving_wallet += (money * 0.2)

    def set_matrix_money(self, money):

        if money is not 0:
            # 20퍼센트 감소된 금액을 셋팅
            result = money - (money * 0.2)
            self.m_money += result

            # 20프로를 SAVING에 적립
            self.saving_wallet += (money * 0.2)



    def get_saving_money(self):
        return self.saving_wallet

    def get_reward_money(self):
        return self.reward_wallet

    def get_recommand_money(self):
        return self.r_money

    def get_support_money(self):
        return self.s_money

    def get_matrix_money(self):
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