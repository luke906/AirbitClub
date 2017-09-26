_Left_Side_Node_Count_List = []
_Right_Side_Node_Count_List = []


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
# 매트리스 수당은 해당 계좌 노드가 생성될때 생성된 계좌를 기준으로 바로 상위로 연결된 모든 부모 계좌 노드에게 지급된다.
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


# 후원수당 계산
# child_node : 생성된 계좌
def calc_support_money(child_node, _last_node_key,
                       _account_level_node_key_dic,
                       _account_node_dic,
                       support_even_money,
                       support_odd_money):
    print("생성되는 노드의 번호 : %d" % child_node.node_number)

    # 현재 생성되는 노드의 레벨이 0 이라면 검사를 안한다.
    if child_node.level == 0:
        return

    # if _last_node_key < 2:
    #   return
    # 0레벨 부터 생성계좌의 상위 레벨까지의 모든 노드를 검사한다.
    # 1. 해당 검사 노드의 LEFT, RIGHT 중 소실적에 포함되는 리스트를 구한다.
    #    인자로 전달된 생성되는 계좌(child_node)가 해당 소실적 리스트에 포함이 되어 있다면
    #    해당 노드의 s_money를 증가 시킨다.
    #     - 소실적 노드의 갯수가 홀수이면 80. support_odd_money
    #     - 소실적 노드의 갯수가 짝수이면 90. support_even_money

    # 2. 인자로 전달된 생성되는 계좌(child_node)의 부모 노드가 FULL상태 이라면
    #    해당 부모 노드의 s_money를 80 증가 시킨다.

    # 생성된 계좌의 상위 레벨을 구한다.
    level = child_node.level

    # 소실적 계좌 리스트
    small_side_list = []

    # 0레벨 부터 생성계좌의 상위 레벨까지의 각각의 레벨의 모든 노드를 검사한다.
    print("0 레벨부터 %d 레벨까지 각각의 노드를 검사" % (level - 1))

    for index in range(0, level):
        # 해당 레벨안에 있는 모든 노드를 돌면서 검사한다.
        for base_node_index in _account_level_node_key_dic[index]:
            print("레벨 %d 안의  %d 노드 검사" % (index, base_node_index))
            # 해당 노드의 LEFT, RIGHT 중 소실적에 포함되는 리스트를 구한다.
            (left_count, right_count) = calc_left_right_node_count(base_node_index, _account_node_dic)
            if left_count < right_count:
                small_side_list = _Left_Side_Node_Count_List
                print("레벨 %d 안의  소실적 노드 리스트" % index)
                print(small_side_list)
            elif left_count > right_count:
                small_side_list = _Right_Side_Node_Count_List
                print("레벨 %d 안의  소실적 노드 리스트" % index)
                print(small_side_list)

            preorder_traverse()

            # 신규 생성 계좌(child_node)가 해당 소실적 리스트에 포함이 되어 있다면
            # 해당 노드의 s_money를 증가 시킨다.
            for small_list_node in small_side_list:
                if child_node.node_number == small_list_node:
                    # 해당 노드의 s_money를 증가 시킨다.
                    print("신규생성노드 %d 번이  %d번 노드의 소실적에 포함" % (child_node.node_number, base_node_index))
                    temp_s_money = _account_node_dic[base_node_index].get_s_money()
                    if (len(small_side_list) % 2) == 0:
                        temp_s_money += support_even_money
                    else:
                        temp_s_money += support_odd_money
                    print("%d번 계좌에 셋팅될  후원 수당은 : %d" % (base_node_index, temp_s_money))
                    _account_node_dic[base_node_index].set_s_money(temp_s_money)
                    small_side_list = []
                    # _account_node_dic[base_node_index] = node_object

    # 2. 인자로 전달된 생성되는 계좌(child_node)의 부모 노드가 FULL상태 이라면
    #    해당 부모 노드의 s_money를 80 증가 시킨다.
    parent_object = child_node.get_parent_node()
    if parent_object.left_child_have == True and parent_object.right_child_have == True:
        temp_s_money = parent_object.get_s_money()
        temp_s_money += support_odd_money
        print("%d번 부모 계좌에 셋팅될  후원 수당은 : %d" % (parent_object.node_number, temp_s_money))
        parent_object.set_s_money(temp_s_money)

    # 계좌를 한개씩 셋팅할때 후원수당 계산하는 함수
    def calc_support_money(child_node, _last_node_key,
                                            _account_level_node_key_dic,
                                            _account_node_dic,
                                            support_even_money,
                                            support_odd_money):
        print("생성되는 노드의 번호 : %d" % child_node.node_number)

        # 현재 생성되는 노드의 레벨이 0 이라면 검사를 안한다.
        if child_node.level == 0:
            return

        # if _last_node_key < 2:
        #   return
        # 0레벨 부터 생성계좌의 상위 레벨까지의 모든 노드를 검사한다.
        # 1. 해당 검사 노드의 LEFT, RIGHT 중 소실적에 포함되는 리스트를 구한다.
        #    인자로 전달된 생성되는 계좌(child_node)가 해당 소실적 리스트에 포함이 되어 있다면
        #    해당 노드의 s_money를 증가 시킨다.
        #     - 소실적 노드의 갯수가 홀수이면 80. support_odd_money
        #     - 소실적 노드의 갯수가 짝수이면 90. support_even_money

        # 2. 인자로 전달된 생성되는 계좌(child_node)의 부모 노드가 FULL상태 이라면
        #    해당 부모 노드의 s_money를 80 증가 시킨다.

        # 생성된 계좌의 상위 레벨을 구한다.
        level = child_node.level

        # 소실적 계좌 리스트
        small_side_list = []

        # 0레벨 부터 생성계좌의 상위 레벨까지의 각각의 레벨의 모든 노드를 검사한다.
        print("0 레벨부터 %d 레벨까지 각각의 노드를 검사" % (level - 1))

        for index in range(0, level):
            # 해당 레벨안에 있는 모든 노드를 돌면서 검사한다.
            for base_node_index in _account_level_node_key_dic[index]:
                print("레벨 %d 안의  %d 노드 검사" % (index, base_node_index))
                # 해당 노드의 LEFT, RIGHT 중 소실적에 포함되는 리스트를 구한다.
                (left_count, right_count) = calc_left_right_node_count(base_node_index, _account_node_dic)
                if left_count < right_count:
                    small_side_list = _Left_Side_Node_Count_List
                    print("레벨 %d 안의  소실적 노드 리스트" % index)
                    print(small_side_list)
                elif left_count > right_count:
                    small_side_list = _Right_Side_Node_Count_List
                    print("레벨 %d 안의  소실적 노드 리스트" % index)
                    print(small_side_list)

                preorder_traverse()

                # 신규 생성 계좌(child_node)가 해당 소실적 리스트에 포함이 되어 있다면
                # 해당 노드의 s_money를 증가 시킨다.
                for small_list_node in small_side_list:
                    if child_node.node_number == small_list_node:
                        # 해당 노드의 s_money를 증가 시킨다.
                        print("신규생성노드 %d 번이  %d번 노드의 소실적에 포함" % (child_node.node_number, base_node_index))
                        temp_s_money = _account_node_dic[base_node_index].get_s_money()
                        if (len(small_side_list) % 2) == 0:
                            temp_s_money += support_even_money
                        else:
                            temp_s_money += support_odd_money
                        print("%d번 계좌에 셋팅될  후원 수당은 : %d" % (base_node_index, temp_s_money))
                        _account_node_dic[base_node_index].set_s_money(temp_s_money)
                        small_side_list = []
                        # _account_node_dic[base_node_index] = node_object

        # 2. 인자로 전달된 생성되는 계좌(child_node)의 부모 노드가 FULL상태 이라면
        #    해당 부모 노드의 s_money를 80 증가 시킨다.
        parent_object = child_node.get_parent_node()
        if parent_object.left_child_have == True and parent_object.right_child_have == True:
            temp_s_money = parent_object.get_s_money()
            temp_s_money += support_odd_money
            print("%d번 부모 계좌에 셋팅될  후원 수당은 : %d" % (parent_object.node_number, temp_s_money))
            parent_object.set_s_money(temp_s_money)



    # 전체 계좌를 모두 생성한 후 후원수당을 계산하는 함수
    def calc_total_s_money(child_node, _last_node_key,
                                          _account_level_node_key_dic,
                                          _account_node_dic,
                                          support_even_money,
                                          support_odd_money):
            print("생성되는 노드의 번호 : %d" % child_node.node_number)

            # 현재 생성되는 노드의 레벨이 0 이라면 검사를 안한다.
            if child_node.level == 0:
                return

            # if _last_node_key < 2:
            #   return
            # 0레벨 부터 생성계좌의 상위 레벨까지의 모든 노드를 검사한다.
            # 1. 해당 검사 노드의 LEFT, RIGHT 중 소실적에 포함되는 리스트를 구한다.
            #    인자로 전달된 생성되는 계좌(child_node)가 해당 소실적 리스트에 포함이 되어 있다면
            #    해당 노드의 s_money를 증가 시킨다.
            #     - 소실적 노드의 갯수가 홀수이면 80. support_odd_money
            #     - 소실적 노드의 갯수가 짝수이면 90. support_even_money

            # 2. 인자로 전달된 생성되는 계좌(child_node)의 부모 노드가 FULL상태 이라면
            #    해당 부모 노드의 s_money를 80 증가 시킨다.

            # 생성된 계좌의 상위 레벨을 구한다.
            level = child_node.level

            # 소실적 계좌 리스트
            small_side_list = []

            # 0레벨 부터 생성계좌의 상위 레벨까지의 각각의 레벨의 모든 노드를 검사한다.
            print("0 레벨부터 %d 레벨까지 각각의 노드를 검사" % (level - 1))

            for index in range(0, level):
                # 해당 레벨안에 있는 모든 노드를 돌면서 검사한다.
                for base_node_index in _account_level_node_key_dic[index]:
                    print("레벨 %d 안의  %d 노드 검사" % (index, base_node_index))
                    # 해당 노드의 LEFT, RIGHT 중 소실적에 포함되는 리스트를 구한다.
                    (left_count, right_count) = calc_left_right_node_count(base_node_index, _account_node_dic)
                    if left_count < right_count:
                        small_side_list = _Left_Side_Node_Count_List
                        print("레벨 %d 안의  소실적 노드 리스트" % index)
                        print(small_side_list)
                    elif left_count > right_count:
                        small_side_list = _Right_Side_Node_Count_List
                        print("레벨 %d 안의  소실적 노드 리스트" % index)
                        print(small_side_list)

                    preorder_traverse()

                    # 신규 생성 계좌(child_node)가 해당 소실적 리스트에 포함이 되어 있다면
                    # 해당 노드의 s_money를 증가 시킨다.
                    for small_list_node in small_side_list:
                        if child_node.node_number == small_list_node:
                            # 해당 노드의 s_money를 증가 시킨다.
                            print("신규생성노드 %d 번이  %d번 노드의 소실적에 포함" % (child_node.node_number, base_node_index))
                            temp_s_money = _account_node_dic[base_node_index].get_s_money()
                            if (len(small_side_list) % 2) == 0:
                                temp_s_money += support_even_money
                            else:
                                temp_s_money += support_odd_money
                            print("%d번 계좌에 셋팅될  후원 수당은 : %d" % (base_node_index, temp_s_money))
                            _account_node_dic[base_node_index].set_s_money(temp_s_money)
                            small_side_list = []
                            # _account_node_dic[base_node_index] = node_object

            # 2. 인자로 전달된 생성되는 계좌(child_node)의 부모 노드가 FULL상태 이라면
            #    해당 부모 노드의 s_money를 80 증가 시킨다.
            parent_object = child_node.get_parent_node()
            if parent_object.left_child_have == True and parent_object.right_child_have == True:
                temp_s_money = parent_object.get_s_money()
                temp_s_money += support_odd_money
                print("%d번 부모 계좌에 셋팅될  후원 수당은 : %d" % (parent_object.node_number, temp_s_money))
                parent_object.set_s_money(temp_s_money)
# 해당 인자로 전달된 노드를 기준으로 좌측, 우측의 모든 연결된 모드들의 수를 계산한다.
def calc_left_right_node_count(base_node_index, _account_node_dic):
    index = base_node_index

    # 검색 기준이 되는 키
    node_object = _account_node_dic[index]

    # 검색 기준이 되는 키의 좌측 모든 노드 갯수를 구한다.
    left_node_object = node_object.get_left_child_node()
    preorder_traverse(base_node_index, left_node_object, "left")

    # 검색 기준이 되는 키의 우측 모든 노드 갯수를 구한다.
    right_node_object = node_object.get_right_child_node()
    preorder_traverse(base_node_index, right_node_object, "right")

    w_count = {}
    for lst in _Left_Side_Node_Count_List:
        try:
            w_count[lst] += 1
        except:
            w_count[lst] = 1
    left_count = len(w_count)
    # print("%d번 노드 왼쪽 노드의 총 갯수:%d " % (base_node_index, len(w_count)))

    w_count = {}
    for lst in _Right_Side_Node_Count_List:
        try:
            w_count[lst] += 1
        except:
            w_count[lst] = 1
    right_count = len(w_count)
    # print("%d번 노드 오른쪽 노드의 총 갯수:%d \n" % (base_node_index, len(w_count)))

    return left_count, right_count


def preorder_traverse(base_node_index=-1, tree_object=None, flag=None):
    global _Left_Side_Node_Count_List
    global _Right_Side_Node_Count_List

    if base_node_index == -1:
        _Left_Side_Node_Count_List = []
        _Right_Side_Node_Count_List = []

    if tree_object is None:
        return

    # print(tree_object.node_number)

    if flag is "left":
        # print("%d번 노드의 LEFT 하위 노드: %d" % (base_node_index, tree_object.node_number))
        _Left_Side_Node_Count_List.append(tree_object.node_number)

    elif flag is "right":
        # print("%d번 노드의 RIGHT 하위 노드: %d" % (base_node_index, tree_object.node_number))
        _Right_Side_Node_Count_List.append(tree_object.node_number)

    preorder_traverse(base_node_index, tree_object.get_left_child_node(), flag)
    preorder_traverse(base_node_index, tree_object.get_right_child_node(), flag)
