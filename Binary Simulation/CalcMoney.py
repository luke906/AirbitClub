def show_all_money(account_node_dic, last_node_key):
    total_r_money = 0
    total_s_money = 0
    total_m_money = 0
    for account in range(0, last_node_key):
        node_object = account_node_dic[account]
        total_r_money += node_object.get_r_money()
        total_s_money += node_object.get_s_money()
        total_m_money += node_object.get_m_money()
    print("전체 노드의 모든 추천 수당의 합계 : %d \n" % total_r_money)
    print("전체 노드의 모든 후원 수당의 합계 : %d \n" % total_s_money)
    print("전체 노드의 모든 매트릭스 수당의 합계 : %d \n" % total_m_money)


# 추천수당 계산
# 추천수당은 바로 아래 본인 직계 노드가 생성될때만 받는다.
def calc_recommand_money(parent_node_object, recommand_money):
    cur_r_money = parent_node_object.get_r_money()
    cur_r_money += recommand_money
    parent_node_object.set_r_money(cur_r_money)


# 매트리스 수당 계산
# 매트리스 수당은 해당 계좌 노드가 생성될때 생성된 계좌를 기준으로 바로 상위로 연결된 모든 부모 계좌 노드에세 지급된다.
def calc_matrix_money(child_node_object, matrix_bonus):
    # 인자로 전달받은 노드의 부모를 구한다.
    parent_node = child_node_object.get_parent_node()

    # 해당 부모의 매트릭스 수당을 더한다.
    cur_m_money = parent_node.get_m_money()
    cur_m_money += matrix_bonus
    parent_node.set_m_money(cur_m_money)

    # 부모 노드의 번호가 0이라면 더이상 계산하지 않는다.
    if parent_node.node_number is 0:
        return

    calc_matrix_money(parent_node, matrix_bonus)