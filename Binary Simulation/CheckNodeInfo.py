def show_node_information(node_index, account_node_dic):
    index_key = node_index
    node_object = account_node_dic[index_key]

    print("%d번 노드의 키 번호: %d \n" % (index_key, node_object.node_number))
    print("%d번 노드의 추천 수당 : %d \n" % (index_key, node_object.get_r_money()))
    print("%d번 노드의 매트릭스 수당 : %d \n" % (index_key, node_object.get_m_money()))

    if node_object.left_child_have is True:
        left_child = node_object.get_left_child_node()
        print("%d번 노드의 왼쪽 자식 번호: %d \n" % (index_key, left_child.node_number))
    else:
        print("%d번 노드의 왼쪽 자식 없음 \n" % index_key)

    if node_object.right_child_have is True:
        right_child = node_object.get_right_child_node()
        print("%d번 노드의 오른쪽 자식 번호: %d \n" % (index_key, right_child.node_number))
    else:
        print("%d번 노드의 오른쪽 자식 없음 \n" % index_key)

    if index_key != 0:
        node_object = Account_Node_Dic[index_key]
        parent_object = node_object.get_parent_node()
        print("%d번 노드의 부모번호: %d \n" % (index_key, parent_object.node_number))


def show_all_node(cur_level_value, account_level_node_key_dic):
    for index in range(0, cur_level_value ):
        if len(account_level_node_key_dic[index]) > 0:
            print("%d 대 계좌 목록" % index)
            print(account_level_node_key_dic[index])
            print("\n")

def show_node_recommand_money(node_index, account_node_dic):
    index_key = node_index
    node_object = account_node_dic[index_key]
    print("%d번 노드의 추천 수당: %d" % (node_index, node_object.get_r_money()))

def show_node_matrix_money(node_index, account_node_dic):
    index_key = node_index
    node_object = account_node_dic[index_key]
    print("%d번 노드의 매트릭스 수당: %d" % (node_index, node_object.get_m_money()))

def show_node_support_money(node_index, account_node_dic):
    index_key = node_index
    node_object = account_node_dic[index_key]
    print("%d번 노드의 후원 수당: %d" % (node_index, node_object.get_s_money()))

def show_node_saving_money(node_index, account_node_dic):
    index_key = node_index
    node_object = account_node_dic[index_key]
    print("%d번 노드의 SAVING 잔고: %d" % (node_index, node_object.get_saving_money()))
