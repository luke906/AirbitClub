_Left_Side_Node_Count_List = []
_Right_Side_Node_Count_List = []

_Left_Side_Node_Support_Calc_False_List = []  # 부모를 기준으로 왼쪽 노드들의 리스트중 신규로 추가된 노드의 리스트
_Right_Side_Node_Support_Calc_False_List = [] # 부모를 기준으로 오른쪽 노드들의 리스트중 신규로 추가된 노드의 리스트


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
    parent_node_object.set_recommand_money(recommand_money)


# 매트리스 수당 계산
# 매트리스 수당은 해당 계좌 노드가 생성될때 생성된 계좌를 기준으로 바로 상위로 연결된 모든 부모 계좌 노드에게 지급된다.
def calc_matrix_money(child_node_object, matrix_bonus):
    # 인자로 전달받은 노드의 부모를 구한다.
    parent_node = child_node_object.get_parent_node()

    # 해당 부모의 매트릭스 수당을 더한다.
    parent_node.set_matrix_money(matrix_bonus)

    # 부모 노드의 번호가 0이라면 더이상 계산하지 않는다.
    if parent_node.node_number is 0:
        return

    calc_matrix_money(parent_node, matrix_bonus)


# 각 계좌별로 추천, 후원, 매트릭스 수당을 커미션 지갑으로 이동시킨다.
def deposit_commision_wallet(_last_node_key, _account_node_dic):
    for index in range(0, _last_node_key + 1):
        _account_node_dic[index].set_commision_wallet()


# 계좌를 한꺼번에 셋팅하고 후원수당을 계산하는 함수. 두번째 버전
def support_money_setting(_last_node_key, _account_node_dic):

    # 생성된 모든 계좌를 검사한다.

    # CASE 1
    # 해당 노드를 기준으로 좌우 한개씩 있는 경우
    # left_count == right_count == 1  and 좌우중 노드 하나라도 support_calc_used == FLASE 인경우
    # 소실적의 갯수가 A 라면
    # A = 1  해당 노드의 후원 수당은 80

    # CASE 2
    # 해당 노드를 기준으로 left_count or right_count > 1
    # support_calc_used == FLASE 인 갯수만큼 적용
    # 소실적의 갯수가 A 라면
    # A>=2  then  A / 2 -> ((몫 X 2) x 90 ) + (나머지 X 80) 이 해당 노드의 후원 수당이 된다.

    # 소실적 계좌 리스트
    small_side_list = []

    # 소실적 계좌 리스트의 총 개수
    small_side_list_count = 0

    # 0레벨 부터 생성계좌의 상위 레벨까지의 각각의 레벨의 모든 노드를 검사한다.
    # ( 단 자식 노드가 하나도 없을 경우 검사를 제외 한다 )
    for index in range(0, _last_node_key+1):
        # node_object = _account_node_dic[index]

        # 해당 노드의 LEFT, RIGHT 갯수 및 Left 신규노드 Right 신규노드 갯수를 구한다.
        (left_count, left_new_count, right_count, right_new_count) = calc_left_right_node_count(index,
                                                                                                _account_node_dic)

        # CASE 1
        if (left_count == 1 and right_count == 1) and (left_new_count == 1 or right_new_count == 1):
            small_side_list = _Left_Side_Node_Support_Calc_False_List

        # CASE 2
        if (left_count > 1 or right_count > 1) and (left_count != right_count):
            if left_count < right_count:
                small_side_list = _Left_Side_Node_Support_Calc_False_List
            elif left_count > right_count:
                small_side_list = _Right_Side_Node_Support_Calc_False_List

        # CASE 3
        if (left_count > 1 or right_count > 1) and (left_count == right_count):
            if _Left_Side_Node_Support_Calc_False_List > _Right_Side_Node_Support_Calc_False_List:
                small_side_list = _Left_Side_Node_Support_Calc_False_List
            elif _Left_Side_Node_Support_Calc_False_List < _Right_Side_Node_Support_Calc_False_List:
                small_side_list = _Right_Side_Node_Support_Calc_False_List


        preorder_traverse()

        small_side_list_count = len(small_side_list)

        (quotient, remainder) = divmod(small_side_list_count, 2)

        support_money = 0
        if small_side_list_count == 1:
            support_money = 80
        elif small_side_list_count >= 2:
            support_money = ((quotient * 2) * 90) + (remainder * 80)

        # 해당 노드의 s_money 를 증가 시킨다.
        # print("%d번 계좌에 셋팅될  후원 수당은 : %d" % (base_node_index, temp_s_money))
        _account_node_dic[index].set_support_money(support_money)
        _account_node_dic[index].support_calc_used = True
        small_side_list = []



# 해당 인자로 전달된 노드를 기준으로 좌측, 우측의 모든 연결된 모드들의 수를 계산한다.
def calc_left_right_node_count(base_node_index, _account_node_dic):

    global _Left_Side_Node_Count_List
    global _Right_Side_Node_Count_List

    global _Left_Side_Node_Support_Calc_False_List
    global _Right_Side_Node_Support_Calc_False_List

    # 검색 기준이 되는 키
    node_object = _account_node_dic[base_node_index]

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
    for lst in _Left_Side_Node_Support_Calc_False_List:
        try:
            w_count[lst] += 1
        except:
            w_count[lst] = 1
    left_new_count = len(w_count)


    w_count = {}
    for lst in _Right_Side_Node_Count_List:
        try:
            w_count[lst] += 1
        except:
            w_count[lst] = 1
    right_count = len(w_count)
    # print("%d번 노드 오른쪽 노드의 총 갯수:%d \n" % (base_node_index, len(w_count)))

    w_count = {}
    for lst in _Right_Side_Node_Support_Calc_False_List:
        try:
            w_count[lst] += 1
        except:
            w_count[lst] = 1
    right_new_count = len(w_count)

    return left_count, left_new_count, right_count, right_new_count


def preorder_traverse(base_node_index=-1, tree_object=None, flag=None):
    global _Left_Side_Node_Count_List
    global _Right_Side_Node_Count_List

    global _Left_Side_Node_Support_Calc_False_List
    global _Right_Side_Node_Support_Calc_False_List

    if base_node_index == -1:
        _Left_Side_Node_Count_List = []
        _Left_Side_Node_Support_Calc_False_List = []

        _Right_Side_Node_Count_List = []
        _Right_Side_Node_Support_Calc_False_List = []

    if tree_object is None:
        return

    # print(tree_object.node_number)

    if flag is "left":
        # print("%d번 노드의 LEFT 하위 노드: %d" % (base_node_index, tree_object.node_number))
        _Left_Side_Node_Count_List.append(tree_object.node_number)
        if tree_object.support_calc_used == False:
            _Left_Side_Node_Support_Calc_False_List.append(tree_object.node_number)


    elif flag is "right":
        # print("%d번 노드의 RIGHT 하위 노드: %d" % (base_node_index, tree_object.node_number))
        _Right_Side_Node_Count_List.append(tree_object.node_number)
        if tree_object.support_calc_used == False:
            _Right_Side_Node_Support_Calc_False_List.append(tree_object.node_number)

    preorder_traverse(base_node_index, tree_object.get_left_child_node(), flag)
    preorder_traverse(base_node_index, tree_object.get_right_child_node(), flag)
