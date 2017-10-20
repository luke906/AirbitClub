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


def show_all_node(Account_Info_table, node_count, _Account_Node_Dic):
    Account_Info_table.setItem(0, 0, QTableWidgetItem("lsw120300"))
    #for index in range(0, node_count ):
        # self.Account_Info_table.setItem(0, 0, QTableWidgetItem("1"))
        # '계좌명', '추천수당', '후원수당', '매트릭스수당', ' SAVING', '전체커미션(SAVING 제외)'

        # 계좌명
        # account_name = "lsw1203" + str(index).zfill(2)
        # Account_Info_table.setItem(index, 0, QTableWidgetItem(account_name))



def show_node_recommand_money(node_index, account_node_dic):
    index_key = node_index
    node_object = account_node_dic[index_key]
    print("%d번 노드의 추천 수당: %d" % (node_index, node_object.get_recommand_money()))

def show_node_matrix_money(node_index, account_node_dic):
    index_key = node_index
    node_object = account_node_dic[index_key]
    print("%d번 노드의 매트릭스 수당: %d" % (node_index, node_object.get_matrix_money()))

def show_node_support_money(node_index, account_node_dic):
    index_key = node_index
    node_object = account_node_dic[index_key]
    print("%d번 노드의 후원 수당: %d" % (node_index, node_object.get_support_money()))

def show_node_saving_money(node_index, account_node_dic):
    index_key = node_index
    node_object = account_node_dic[index_key]
    print("%d번 노드의 SAVING 잔고: %d" % (node_index, node_object.get_saving_money()))
