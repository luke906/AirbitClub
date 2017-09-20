import Tree_Class

# 각 생성된 레벨의 완성여부 딕셔너리
Level_Complete_Flag = {}

# 생성된 노드의 총 갯수
Total_Node_Count = 0

# 각 레벨에서 생성될 노드 카운트
Level_Node_Count = 0

# 각각 생성된 계좌를 저장할 리스트
Account_Node_List = []

# 현재 생성할 레벨
Cur_Level_Value = 0


def create_account():
    global Level_Complete_Flag
    global Total_Node_Count
    global Level_Node_Count
    global Account_Node_List
    global Cur_Level_Value

    new_node_account = None

    # 만일 현재 레벨이 0 이라면 루트 계좌 생성
    if Cur_Level_Value == 0:
        new_node_account = Tree_Class.BinaryTree(0, Cur_Level_Value)

    # 만일 현재 레엘이 0보다 크다면 자식 노드 생성
    elif Cur_Level_Value > 0:
        new_node_account = Tree_Class.BinaryTree(Total_Node_Count, Cur_Level_Value)

    # 생성된 계좌 리스트에 저장
    Account_Node_List.append(new_node_account)

    # 총 노드 갯수 증가
    Total_Node_Count += 1

    # 현재 레벨에서 생성된 노드의 갯수 증가
    Level_Node_Count += 1

    # 현재의 레벨에 노드가 FULL 인지 검사
    if Level_Node_Count == (2 ** Cur_Level_Value):
        Level_Node_Count = 0
        Level_Complete_Flag[Cur_Level_Value] = True
        Cur_Level_Value += 1


def main():
    for i in range(1, 100):
        create_account()

        # 사용자가 원하는 생성할 계좌의 갯수가 모두 생성 되었다면 종료


if __name__ == '__main__':
    main()