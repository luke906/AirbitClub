from TreeClass import BinaryTree
import CalcMoney
import CheckNodeInfo

# 마지막으로 생성된 노드 키
_Last_Node_Key = -1

# 각 레벨에서 생성될 노드 카운트
_Level_Node_Count = 0

# 각각 생성된 계좌 노드를 저장할 딕셔너리
_Account_Node_Dic = {}

# 각 레벨별 생성된 계좌 노드 키를 저장할 딕셔너리, 임시 리스트
_Account_Level_Node_Key_Dic = {}
_Account_Level_Node_List = []

# 현재 생성할 레벨
_Cur_Level_Value = 0

# 각 생성된 레벨의 완성여부 딕셔너리
_Level_Complete_Flag = {}

_Left_Side_Node_Count_List = []
_Right_Side_Node_Count_List = []

SAVING_RATIO = 0.2
RECOMMAND_MONEY = 200
MATRIX_BONUS = 10
SUPPORT_ODD_MONEY = 80
SUPPORT_EVEN_MONEY = 90


# 계좌 생성 함수
# 호출시 자동으로 레벨을 계산하며 순차적으로 배치가 된다.
def create_account():
    global _Level_Complete_Flag
    global _Last_Node_Key
    global _Cur_Level_Value
    global _Account_Node_Dic
    global _Account_Level_Node_Key_Dic
    global _Account_Level_Node_List
    global _Level_Node_Count

    # 생성될 노드키
    _Last_Node_Key += 1

    # 현재 레벨에서 생성된 노드의 갯수 증가
    _Level_Node_Count += 1

    # 신규 계좌 생성
    new_node_account = BinaryTree(_Last_Node_Key, _Cur_Level_Value)

    # 생성된 계좌 저장
    _Account_Node_Dic[_Last_Node_Key] = new_node_account

    # 현재 레벨에서 생성된 계좌를 레벨별로 저장
    _Account_Level_Node_List.append(_Last_Node_Key)
    _Account_Level_Node_Key_Dic[_Cur_Level_Value] = _Account_Level_Node_List

    # 현재의 레벨에 노드가 FULL 인지 검사
    if _Level_Node_Count == (2 ** _Cur_Level_Value):
        _Level_Complete_Flag[_Cur_Level_Value] = True
        _Level_Node_Count = 0
        _Cur_Level_Value += 1

        # 새로운 레벨 생성시 참조 에러가 나기 때문에 빈 데이터를 셋팅한다.
        _Account_Level_Node_List = []
        _Account_Level_Node_Key_Dic[_Cur_Level_Value] = _Account_Level_Node_List

    connect_node_account()


def connect_node_account():
    # 자식으로 추가될 계좌 노드를 구한다.
    child_node_key = _Last_Node_Key
    child_node = _Account_Node_Dic[child_node_key]

    if child_node.node_number == 0:
        return

    # 마지막으로 생성된 노드 레벨의 상위 단계 레벨안에 들어 있는 노드의 총 갯수를 구한다.
    index = child_node.level - 1
    node_count_in_level = len(_Account_Level_Node_Key_Dic[index])

    for i in range(0, node_count_in_level):

        # 구할 보모 노드의 키를 구한다.
        parent_node_key = _Account_Level_Node_Key_Dic[index][i]

        # 부모 노드를 구한다.
        parent_node = _Account_Node_Dic[parent_node_key]

        # 해당 부모의 왼쪽에 노드가 있는지 검사하고 없다면 부모 노드의 left로 셋팅한다.
        if not parent_node.left_child_have:
            parent_node.set_left_child_node(child_node)
            _Account_Node_Dic[parent_node_key] = parent_node

            child_node.set_parent_node(parent_node)
            _Account_Node_Dic[child_node_key] = child_node

            # 추천수당 계산
            CalcMoney.calc_recommand_money(parent_node, RECOMMAND_MONEY)

            # 매트리스 수당 계산
            CalcMoney.calc_matrix_money(child_node, MATRIX_BONUS)
            return

        # 해당 부모의 오른쪽에 노드가 있는지 검사하고 없다면 부모 노드의 right로 셋팅한다.
        if not parent_node.right_child_have:
            parent_node.set_right_child_node(child_node)
            _Account_Node_Dic[parent_node_key] = parent_node

            child_node.set_parent_node(parent_node)
            _Account_Node_Dic[child_node_key] = child_node

            # 추천수당 계산
            CalcMoney.calc_recommand_money(parent_node, RECOMMAND_MONEY)

            # 매트리스 수당 계산
            CalcMoney.calc_matrix_money(child_node, MATRIX_BONUS)
            return


# 후원수당 계산
def calc_support_money(child_node):
    # 현재 생성된 마지막 노드를 제외한 모든 모드를 검사한다.
    child_node_object = _Account_Node_Dic[_Last_Node_Key]
    current_level = child_node_object.level

    if current_level == 0:
        return

    if _Last_Node_Key < 2:
        return
    # 0레벨 부터 생성계좌의 상위 레벨까지의 모든 노드를 검사한다.
    # 1. 해당 검사 노드의 LEFT, RIGHT 중 소실적에 포함되는 리스트를 구한다.
    #    인자로 전달된 생성되는 계좌(child_node)가 해당 소실적 리스트에 포함이 되어 있다면
    #    해당 노드의 s_money를 증가 시킨다.
    #     - 소실적 노드의 갯수가 홀수이면 80. SUPPORT_ODD_MONEY
    #     - 소실적 노드의 갯수가 짝수이면 90. SUPPORT_EVEN_MONEY

    # 2. 인자로 전달된 생성되는 계좌(child_node)의 부모 노드가 FULL상태 이라면
    #    해당 부모 노드의 s_money를 80 증가 시킨다.

    # 생성된 계좌의 상위 레벨을 구한다.
    level = child_node.level

    # 소실적 계좌 리스트
    small_side_list = []

    # 0레벨 부터 생성계좌의 상위 레벨까지의 모든 노드를 검사한다.
    for index in range(0, level):
        # 해당 레벨안에 있는 노드의 갯수를 구한다.
        for base_node_index in range(0, len(_Account_Level_Node_Key_Dic[index])):
            # 해당 검사 노드의 LEFT, RIGHT 중 소실적에 포함되는 리스트를 구한다.
            (left_count, right_count) = calc_left_right_node_count(base_node_index)
            if left_count < right_count:
                small_side_list = _Left_Side_Node_Count_List
            elif left_count > right_count:
                small_side_list = _Right_Side_Node_Count_List

            preorder_traverse()

            # 인자로 전달된 생성되는 계좌(child_node)가 해당 소실적 리스트에 포함이 되어 있다면
            # 해당 노드의 s_money를 증가 시킨다.
            for small_list_node in small_side_list:
                if child_node.node_number == small_list_node:
                    # 해당 노드의 s_money를 증가 시킨다.
                    node_object = _Account_Node_Dic[base_node_index]
                    temp_s_money = node_object.get_s_money()
                    if (len(small_side_list)%2) == 0:
                        temp_s_money += SUPPORT_EVEN_MONEY
                    else:
                        temp_s_money += SUPPORT_ODD_MONEY
                    node_object.set_s_money(temp_s_money)
                    _Account_Node_Dic[base_node_index] = node_object

    # 2. 인자로 전달된 생성되는 계좌(child_node)의 부모 노드가 FULL상태 이라면
    #    해당 부모 노드의 s_money를 80 증가 시킨다.
    parent_object = child_node.get_parent_node()
    if parent_object.left_child_have == True and parent_object.right_child_have == True:
        temp_s_money = parent_object.get_s_money()
        if (len(small_side_list) % 2) == 0:
            temp_s_money += SUPPORT_EVEN_MONEY
        else:
            temp_s_money += SUPPORT_ODD_MONEY
        parent_object.set_s_money(temp_s_money)


# 해당 인자로 전달된 노드를 기준으로 좌측, 우측의 모든 연결된 모드들의 수를 계산한다.
def calc_left_right_node_count(base_node_index):
    index = base_node_index

    # 검색 기준이 되는 키
    node_object = _Account_Node_Dic[index]

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
        print("%d번 노드의 LEFT 하위 노드: %d" % (base_node_index, tree_object.node_number))
        _Left_Side_Node_Count_List.append(tree_object.node_number)

    elif flag is "right":
        print("%d번 노드의 RIGHT 하위 노드: %d" % (base_node_index, tree_object.node_number))
        _Right_Side_Node_Count_List.append(tree_object.node_number)

    preorder_traverse(base_node_index, tree_object.get_left_child_node(), flag)
    preorder_traverse(base_node_index, tree_object.get_right_child_node(), flag)


def main():
    """
    for i in range(0, 15):
        # print(i)
        create_account()
        connect_node_account()
    """
    create_account()
    create_account()
    create_account()
    print("\n")
    CheckNodeInfo.show_all_node(_Cur_Level_Value, _Account_Level_Node_Key_Dic)
    (left_count, right_count) = calc_left_right_node_count(0)
    print("0번 노드의 왼쪽 노드의 총 갯수: %d" % left_count)
    print("0번 노드의 오른쪽 노드의 총 갯수: %d" % right_count)

    create_account()
    create_account()
    print("\n")
    CheckNodeInfo.show_all_node(_Cur_Level_Value, _Account_Level_Node_Key_Dic)
    (left_count, right_count) = calc_left_right_node_count(0)
    print("0번 노드의 왼쪽 노드의 총 갯수: %d" % left_count)
    print("0번 노드의 오른쪽 노드의 총 갯수: %d" % right_count)
    # CheckNodeInfo.show_node_information(0, _Account_Node_Dic)
    # CalcMoney.show_all_money(_Account_Node_Dic, _Last_Node_Key)


if __name__ == '__main__':
    main()
