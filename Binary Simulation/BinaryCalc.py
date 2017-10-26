from TreeClass import BinaryTree
import CreateAccount

import sys
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import *
from PyQt5 import uic

from math import ceil, floor

form_class = uic.loadUiType("airbitclub_simulator.ui")[0]

class ABC_Simulator_Window(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.Btn_Create_Account_Setup.clicked.connect(self.btn_clicked_Create_Account_Setup)
        self.Btn_Reset_Account.clicked.connect(self.btn_clicked_Reset_Account)
        self.Btn_Deposit_Commision.clicked.connect(self.btn_clicked_Deposit_Commision)
        self.Btn_Deposit_Commision_2.clicked.connect(self.btn_clicked_Deposit_Commision)
        self.Btn_Reward_Calc.clicked.connect(self.btn_clicked_Reward_Calc)
        self.Btn_Transfer_To_First_Account.clicked.connect(self.btn_clicked_transfer_to_first_account)
        self.Btn_Create_Additional_Account.clicked.connect(self.btn_clicked_Create_Additional_Account)

        self.Commision_Amount_To_Setup.textChanged.connect(self.commision_amount_text_change)
        self.Reward_Amount_To_Setup.textChanged.connect(self.commision_amount_text_change)

        self.Account_Info_table.setRowCount(0)
        self.Account_Info_table.setColumnCount(7)
        self.setTableWidgetData()

        self.Days = 0

    def commision_amount_text_change(self):

        m_commision = 0
        m_reward = 0

        if len(self.Commision_Amount_To_Setup.text()) > 0:
            m_commision = int(self.Commision_Amount_To_Setup.text())

        if len(self.Reward_Amount_To_Setup.text()) > 0:
            m_reward = int(self.Reward_Amount_To_Setup.text())

        count, b = divmod((m_commision+m_reward), 1000)

        self.Additional_Account_Count.setText(str(count))

    # 첫번째 계좌로 이체되어 모아진 커미션 + 리워드로 추가 계좌를 생성한다.
    def btn_clicked_Create_Additional_Account(self):

        m_commision = 0
        m_reward = 0

        if len(self.Commision_Amount_To_Setup.text()) > 0:
            m_commision = int(self.Commision_Amount_To_Setup.text())

        if len(self.Reward_Amount_To_Setup.text()) > 0:
            m_reward = int(self.Reward_Amount_To_Setup.text())

        # 추가로 생성할 계좌의 갯수
        node_count, b = divmod((m_commision + m_reward), 1000)

        CreateAccount.minus_reward_commision_money_from_first_account(m_commision, m_reward)

        for i in range(0, node_count):
            CreateAccount.create_account()

        CreateAccount.calc_support_money()


        # 생성된 계좌를 테이블에 표시한다.
        count = CreateAccount.get_last_node_key() + 1
        self.Total_Account_Number.setText(str(floor(count)))

        self.show_all_account()

        self.Days += 2
        CreateAccount.set_day_count(2)
        self.Total_Days.setText(str(self.Days))

        self.Total_Commision.setText(str(floor(CreateAccount.get_total_account_commision())))

        self.Total.setText(str(floor(CreateAccount.get_total_account_commision() + CreateAccount.get_total_reward())))


    def setTableWidgetData(self):
        self.Account_Info_table.setHorizontalHeaderLabels(['계좌명', '추천', '후원', '매트릭스', '커미션-지갑', '리워드-지갑', 'SAVING'])
        stylesheet = "::section{Background-color:rgb(211,247,252);border-radius:14px;}"
        self.Account_Info_table.horizontalHeader().setStyleSheet(stylesheet)

    # 천번째 계좌로 나머지 모든 계좌의 커미션, 리워드 금액을 이동 시킨다.
    def btn_clicked_transfer_to_first_account(self):
        CreateAccount.commision_reward_move_to_first_account()

        account_list = CreateAccount.get_Account_Node_Dic()
        total = account_list[0].get_comision_money() + account_list[0].get_reward_money()
        self.Total_Commision_Reward_First_Account.setText(str(floor(total)))

        # 생성된 계좌를 테이블에 표시한다.
        count = CreateAccount.get_last_node_key() + 1
        account_list = CreateAccount.get_Account_Node_Dic()

        self.show_all_account()


    def btn_clicked_Reward_Calc(self):

        self.Days += 1
        CreateAccount.set_day_count(1)
        self.Total_Days.setText(str(self.Days))

        CreateAccount.set_reward_wallet()


        # 생성된 계좌를 테이블에 표시한다.
        count = CreateAccount.get_last_node_key() + 1
        account_list = CreateAccount.get_Account_Node_Dic()

        for index in range(0, count):
            # 리워드
            account_reward_money = str(floor(account_list[index].get_reward_money()))
            Item = QTableWidgetItem(account_reward_money)
            self.Account_Info_table.setItem(index, 5, Item)
            Item.setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        self.Total_Reward.setText(str(floor(CreateAccount.get_total_reward())))

        self.Total.setText(str(floor(CreateAccount.get_total_account_commision() + CreateAccount.get_total_reward())))

        # account_list = CreateAccount.get_Account_Node_Dic()
        # total = account_list[0].get_comision_money() + account_list[0].get_reward_money()
        # self.Total_Commision_Reward_First_Account.setText(str(floor(total)))


    #  추천 후원 매트릭스 각각 수당을 커미션 지갑으로 이동 시킨다.
    def btn_clicked_Deposit_Commision(self):

        CreateAccount.deposit_commision_wallet()

        # 생성된 계좌를 테이블에 표시한다.
        count = CreateAccount.get_last_node_key() + 1
        account_list = CreateAccount.get_Account_Node_Dic()

        self.show_all_account()

        self.Total_Commision.setText(str(floor(CreateAccount.get_total_account_commision())))

        self.Total.setText(str(floor(CreateAccount.get_total_account_commision() + CreateAccount.get_total_reward())))

    def btn_clicked_Create_Account_Setup(self):

        # 초기 계좌 전체 셋팅
        w = QWidget()

        check = str(self.Account_Count_ToSetup.text())
        if check:
            node_count = int(self.Account_Count_ToSetup.text())
        else:
            QMessageBox.warning(w, "확인", "생성될 계좌의 갯수를 입력하십시오.")
            return

        if node_count <=0:
            QMessageBox.warning(w, "확인", "생성될 계좌의 갯수는 0보다 커야 합니다.")
            return

        for i in range(0, node_count):
            CreateAccount.create_account()

        CreateAccount.calc_support_money()

        # 생성된 계좌를 테이블에 표시한다.
        count = CreateAccount.get_last_node_key() + 1
        account_list = CreateAccount.get_Account_Node_Dic()

        self.Total_Account_Number.setText(str(floor(count)))

        self.show_all_account()

        self.Days += 2
        CreateAccount.set_day_count(2)
        self.Total_Days.setText(str(self.Days))

    def show_all_account(self):
        # 생성된 계좌를 테이블에 표시한다.
        count = CreateAccount.get_last_node_key() + 1
        account_list = CreateAccount.get_Account_Node_Dic()

        for index in range(0, count):
            self.Account_Info_table.setRowCount(CreateAccount.get_last_node_key() + 1)

            # 계좌명
            # account_name = "lsw1203" + str(index).zfill(2)
            account_name = str(index + 1) + " 번 계좌"
            Item = QTableWidgetItem(account_name)
            self.Account_Info_table.setItem(index, 0, Item)
            Item.setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

            # 추천수당
            account_r_money = str(floor(account_list[index].get_recommand_money()))
            Item = QTableWidgetItem(account_r_money)
            self.Account_Info_table.setItem(index, 1, Item)
            Item.setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

            # 후원수당
            account_s_money = str(floor(account_list[index].get_support_money()))
            Item = QTableWidgetItem(account_s_money)
            self.Account_Info_table.setItem(index, 2, Item)
            Item.setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

            # 매트릭스수당
            account_m_money = str(floor(account_list[index].get_matrix_money()))
            Item = QTableWidgetItem(account_m_money)
            self.Account_Info_table.setItem(index, 3, Item)
            Item.setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

            # 커미션(추천 + 후원 + 매트릭스)
            account_total_commision = str(floor(account_list[index].get_comision_money()))
            Item = QTableWidgetItem(account_total_commision)
            self.Account_Info_table.setItem(index, 4, Item)
            Item.setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

            # 리워드
            account_reward_money = str(floor(account_list[index].get_reward_money()))
            Item = QTableWidgetItem(account_reward_money)
            self.Account_Info_table.setItem(index, 5, Item)
            Item.setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

            # SAVING
            account_sav_money = str(floor(account_list[index].get_saving_money()))
            Item = QTableWidgetItem(account_sav_money)
            self.Account_Info_table.setItem(index, 6, Item)
            Item.setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

    def btn_clicked_Reset_Account(self):

        # 마지막으로 생성된 노드 키
        count = self.Account_Info_table.rowCount() + 1
        for index in range(0, count):
            self.Account_Info_table.setItem(index, 0, QTableWidgetItem(" "))
            self.Account_Info_table.setItem(index, 1, QTableWidgetItem(" "))
            self.Account_Info_table.setItem(index, 2, QTableWidgetItem(" "))
            self.Account_Info_table.setItem(index, 3, QTableWidgetItem(" "))
            self.Account_Info_table.setItem(index, 4, QTableWidgetItem(" "))
            self.Account_Info_table.setItem(index, 5, QTableWidgetItem(" "))
            self.Account_Info_table.setItem(index, 6, QTableWidgetItem(" "))

        CreateAccount.reset_all_account()
        self.Total_Commision.setText("0")
        self.Total_Reward.setText("0")
        self.Total_Days.setText("0")
        self.Total_Commision_Reward_First_Account.setText("0")
        self.Total_Account_Number.setText("0")
        self.Total.setText("0")
        self.Days = 0

def main():
    app = QApplication(sys.argv)
    ABC_Window = ABC_Simulator_Window()
    ABC_Window.show()
    app.exec_()

if __name__ == '__main__':
    main()
