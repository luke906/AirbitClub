import Tree_Class

# 마지막으로 생성된 노드 키
Last_Node_Key = -1

# 각 레벨에서 생성될 노드 카운트
Level_Node_Count = 0

# 각각 생성된 계좌 노드를 저장할 딕셔너리
Account_Node_Dic = {}

# 각 레벨별 생성된 계좌 노드 키를 저장할 딕셔너리, 임시 리스트
Account_Level_Node_Key_Dic = {}
Account_Level_Node_List = []

# 현재 생성할 레벨
Cur_Level_Value = 0

# 각 생성된 레벨의 완성여부 딕셔너리
Level_Complete_Flag = {}


# 계좌 생성 함수
# 호출시 자동으로 레벨을 계산하며 순차적으로 배치가 된다.
def create_account():
    global Level_Complete_Flag
    global Total_Node_Count
    global Last_Node_Key
    global Cur_Level_Value
    global Account_Node_Dic
    global Account_Level_Node_Key_Dic
    global Account_Level_Node_List
    global Level_Node_Count

    # 생성될 노드키
    Last_Node_Key += 1

    # 현재 레벨에서 생성된 노드의 갯수 증가
    Level_Node_Count += 1

    # 신규 계좌 생성
    new_node_account = Tree_Class.binarytree(Last_Node_Key, Cur_Level_Value)

    # 생성된 계좌 저장
    Account_Node_Dic[Last_Node_Key] = new_node_account

    # 현재 레벨에서 생성된 계좌를 레벨별로 저장
    Account_Level_Node_List.append(Last_Node_Key)
    Account_Level_Node_Key_Dic[Cur_Level_Value] = Account_Level_Node_List



    # 현재의 레벨에 노드가 FULL 인지 검사
    if Level_Node_Count == (2 ** Cur_Level_Value):
        Level_Node_Count = 0
        Level_Complete_Flag[Cur_Level_Value] = True
        Account_Level_Node_List = []
        Cur_Level_Value += 1


def connect_node_account():

    # 자식으로 추가될 계좌 노드를 구한다.
    child_node_key = Last_Node_Key
    child_node = Account_Node_Dic[child_node_key]

    if child_node.node_number == 0:
        return

    # 전달된 현재 레벨의 상위 단계 레벨안에 들어 있는 노드의 총 갯수를 구한다.
    index = Cur_Level_Value - 1
    node_count_in_level = len(Account_Level_Node_Key_Dic[index])

    for i in range(0, node_count_in_level):

        # 구할 보모 노드의 키를 구한다.
        parent_node_key = Account_Level_Node_Key_Dic[index][i]

        # 부모 노드를 구한다.
        parent_node = Account_Node_Dic[parent_node_key]

        # 해당 부모의 왼쪽에 노드가 있는지 검사하고 없다면 부모 노드의 left로 셋팅한다.
        if parent_node.left_child == None:
            parent_node.Set_Left_Child_Node(child_node)
            Account_Node_Dic[parent_node_key] = parent_node

            child_node.Set_Parent_Node(parent_node)
            Account_Node_Dic[child_node_key] = child_node
            return

        # 해당 부모의 오른쪽에 노드가 있는지 검사하고 없다면 부모 노드의 right로 셋팅한다.
        elif parent_node.right_child == None:
            parent_node.Set_right_Child_Node(child_node)
            Account_Node_Dic[parent_node_key] = parent_node

            child_node.Set_Parent_Node(parent_node)
            Account_Node_Dic[child_node_key] = child_node
            return


def main():
    for i in range(0, 100):
        # print(i)
        create_account()
        connect_node_account()

    for index in range(0, Cur_Level_Value + 1):
        print("%d 대 계좌 목록" % index)
        print(Account_Level_Node_Key_Dic[index])
        print("\n")


if __name__ == '__main__':
    main()
