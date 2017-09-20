import Tree_Class

# 각 생성된 레벨의 완성여부 딕셔너리
Level_Complete_Flag = {}

# 생성된 노드의 총 갯수
Total_Node_Count = 0

# 각 레벨에서 생성될 노드 카운트
Level_Node_Count = 0

# 각각 생성된 계좌 노드를 저장할 딕셔너리
Account_Node_Dic = {}

# 각 레벨별 생성된 계좌 노드 키를 저장할 딕셔너리, 임시 리스트
Account_Level_Node_Key_Dic = {}
Account_Level_Node_List = []

# 현재 생성할 레벨
Cur_Level_Value = 0


# 계좌 생성 함수
# 호출시 자동으로 레벨을 계산하며 순차적으로 배치가 된다.
def create_account():
    global Level_Complete_Flag
    global Total_Node_Count
    global Level_Node_Count
    global Cur_Level_Value
    global Account_Node_Dic
    global Account_Level_Node_Key_Dic
    global Account_Level_Node_List

    new_node_account = None

    # 총 노드 갯수 증가
    Total_Node_Count += 1

    # 현재 레벨에서 생성된 노드의 갯수 증가
    Level_Node_Count += 1

    # 신규 계좌 생성
    new_node_account = Tree_Class.binarytree(Total_Node_Count, Cur_Level_Value)

    # 생성된 계좌 저장
    Account_Node_Dic[Total_Node_Count] = new_node_account

    # 현재 레벨에서 생성된 계좌를 레벨별로 저장
    Account_Level_Node_List.append(Total_Node_Count)
    Account_Level_Node_Key_Dic[Cur_Level_Value] = Account_Level_Node_List

    # 현재의 레벨에 노드가 FULL 인지 검사
    if Level_Node_Count == (2 ** Cur_Level_Value):
        Level_Node_Count = 0
        Level_Complete_Flag[Cur_Level_Value] = True
        Account_Level_Node_List = []
        Cur_Level_Value += 1




def connect_node_account():

    if Cur_Level_Value == 0:
        pass

    # 마지막으로 생성된 키는 현재 작업할 노드의 키이다.
    node_key = Total_Node_Count

    # 자식으로 추가될 계좌 노드를 구한다.
    child_node = Account_Node_Dic[node_key]

    # 전달된 현재 레벨의 상위 단계 레벨안에 들어 있는 노드의 총 갯수를 구한다.
    index = Cur_Level_Value-1
    node_count_in_level = len(Account_Level_Node_Key_Dic[index])

    for i in range(0, node_count_in_level+1):

        # 구할 보모 노드의 키를 구한다.
        node_key = Account_Level_Node_Key_Dic[index][i]

        # 부모 노드를 구한다.
        parent_node = Account_Node_Dic[node_key]

        # 해당 부모의 왼쪽에 노드가 있는지 검사하고 없다면 부모 노드의 left로 셋팅한다.
        if parent_node.left_child != None:
            parent_node.Set_Left_Child_Node(child_node)
            Account_Node_Dic[node_key] = parent_node
            break

        # 해당 부모의 오른쪽에 노드가 있는지 검사하고 없다면 부모 노드의 right로 셋팅한다.
        elif parent_node.right_child != None:
            parent_node.Set_right_Child_Node(child_node)
            Account_Node_Dic[node_key] = parent_node
            break




def main():
    for i in range(1, 8):
        #print(i)
        create_account()
        connect_node_account()


    index = None
    for a in range(0, Cur_Level_Value):
        index = a

        print("%d 대 계좌 목록" % a)
        print(Account_Level_Node_Key_Dic[index])
        print("\n")




if __name__ == '__main__':
    main()