def show_all_money(Account_Node_Dic, Last_Node_Key):
    total_r_money = 0
    total_s_money = 0
    total_m_money = 0
    for account in range(0, Last_Node_Key):
        node_object = Account_Node_Dic[account]
        total_r_money += node_object.get_r_money()
        total_s_money += node_object.get_s_money()
        total_m_money += node_object.get_m_money()
    print("전체 노드의 모든 추천 수당의 합계 : %d \n" % total_r_money)
    print("전체 노드의 모든 후원 수당의 합계 : %d \n" % total_s_money)
    print("전체 노드의 모든 매트릭스 수당의 합계 : %d \n" % total_m_money)
