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


def create_account():
    global Level_Complete_Flag
    global Total_Node_Count
    global Level_Node_Count
    global Account_Node_List
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


def main():
    for i in range(1, 101):
        #print(i)
        create_account()

    index = None
    for a in range(0, Cur_Level_Value+1):
        index = a

        print("%d 대 계좌 목록" % a)
        print(Account_Level_Node_Key_Dic[index])
        print("\n")


if __name__ == '__main__':
    main()