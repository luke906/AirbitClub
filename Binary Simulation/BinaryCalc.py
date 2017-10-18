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

SAVING_RATIO = 0.2
RECOMMAND_MONEY = 200
MATRIX_BONUS = 10
SUPPORT_ODD_MONEY = 80
SUPPORT_EVEN_MONEY = 90


# 계좌 생성 함수
# 호출시 자동으로 레벨을 계산하며 순차적으로 배치가 된다.
def create_account(create_flag=0, create_index=0):
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

    #최초 생성되는 계좌의 번호가 0 첫번째 계좌라면 노드 연결 과정을 생략한다.
    if child_node.node_number == 0:
        return

    # 마지막으로 생성된 노드 레벨의 상위 단계 레벨안에 들어 있는 노드의 총 갯수를 구한다.
    index = child_node.level - 1
    node_count_in_level = len(_Account_Level_Node_Key_Dic[index])

    for i in range(0, node_count_in_level):

        # 구할 부모 노드의 키를 구한다.
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


def main():

    # 초기 계좌 전체 셋팅
    node_count = 3
    for i in range(0, node_count):
        create_account()

    #생성된 계좌를 레벨별로 표시한다.
    object = _Account_Node_Dic[_Last_Node_Key]
    level = object.level + 1
    CheckNodeInfo.show_all_node(level, _Account_Level_Node_Key_Dic)

    # 전체 계좌 셋팅이 끝난 후 후원수당을 마지막으로 계산한다.
    CalcMoney.support_money_setting(_Last_Node_Key,
                                    _Account_Node_Dic)

    print("\n")
    print("\n")
    for i in range(0, node_count):
        CheckNodeInfo.show_node_recommand_money(i, _Account_Node_Dic)
        CheckNodeInfo.show_node_matrix_money(i, _Account_Node_Dic)
        CheckNodeInfo.show_node_support_money(i, _Account_Node_Dic)
        CheckNodeInfo.show_node_saving_money(i, _Account_Node_Dic)
        print("\n")



    """"""
    # 초기 계좌 전체 셋팅
    node_count = 2
    for i in range(0, node_count):
        create_account()

    # 생성된 계좌를 레벨별로 표시한다.
    object = _Account_Node_Dic[_Last_Node_Key]
    level = object.level + 1
    CheckNodeInfo.show_all_node(level, _Account_Level_Node_Key_Dic)

    # 전체 계좌 셋팅이 끝난 후 후원수당을 마지막으로 계산한다.
    CalcMoney.support_money_setting(_Last_Node_Key,
                                    _Account_Node_Dic)

    print("\n")
    print("\n")
    for i in range(1, 2):
        CheckNodeInfo.show_node_recommand_money(i, _Account_Node_Dic)
        CheckNodeInfo.show_node_matrix_money(i, _Account_Node_Dic)
        CheckNodeInfo.show_node_support_money(i, _Account_Node_Dic)
        CheckNodeInfo.show_node_saving_money(i, _Account_Node_Dic)
        print("\n")

    # CheckNodeInfo.show_all_node(_Cur_Level_Value, _Account_Level_Node_Key_Dic)
    # (left_count, right_count) = calc_left_right_node_count(0)
    # print("0번 노드의 왼쪽 노드의 총 갯수: %d" % left_count)
    # print("0번 노드의 오른쪽 노드의 총 갯수: %d" % right_count)

    # CheckNodeInfo.show_node_information(0, _Account_Node_Dic)
    # CalcMoney.show_all_money(_Account_Node_Dic, _Last_Node_Key)

    total = 0
    ttt = 0
    for i in range(0, node_count):
        object = _Account_Node_Dic[i]
        total = object.get_s_money() + object.get_r_money() + object.get_m_money()
        ttt += total
    print("총 수익 : %d" % ttt)



if __name__ == '__main__':
    main()
