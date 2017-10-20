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
        self.Account_Info_table.setRowCount(0)
        self.Account_Info_table.setColumnCount(7)
        self.setTableWidgetData()

    def setTableWidgetData(self):
        self.Account_Info_table.setHorizontalHeaderLabels(['계좌명', '리워드수당', '추천수당', '후원수당', '매트릭스수당', ' SAVING', '전체커미션(SAVING 제외)'])

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

        total_commision = 0

        for index in range(0, count):
            # '계좌명', '추천수당', '후원수당', '매트릭스수당', ' SAVING', '전체커미션(SAVING 제외)'

            self.Account_Info_table.setRowCount(CreateAccount.get_last_node_key() + 1)

            # 계좌명
            account_name = "lsw1203" + str(index).zfill(2)
            Item = QTableWidgetItem(account_name)
            self.Account_Info_table.setItem(index, 0, Item)
            Item.setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

            # 추천수당
            account_r_money = str(floor(account_list[index].get_recommand_money()))
            Item = QTableWidgetItem(account_r_money)
            self.Account_Info_table.setItem(index, 2, Item)
            Item.setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

            # 후원수당
            account_s_money = str(floor(account_list[index].get_support_money()))
            Item = QTableWidgetItem(account_s_money)
            self.Account_Info_table.setItem(index, 3, Item)
            Item.setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

            # 매트릭스수당
            account_m_money = str(floor(account_list[index].get_matrix_money()))
            Item = QTableWidgetItem(account_m_money)
            self.Account_Info_table.setItem(index, 4, Item)
            Item.setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

            # SAVING
            account_sav_money = str(floor(account_list[index].get_saving_money()))
            Item = QTableWidgetItem(account_sav_money)
            self.Account_Info_table.setItem(index, 5, Item)
            Item.setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

            # SAVING 을 제외한 전체 합산
            total_commision += floor(account_list[index].get_total_comision())
            account_total_money = str(floor(account_list[index].get_total_comision()))
            Item = QTableWidgetItem(account_total_money)
            self.Account_Info_table.setItem(index, 6, Item)
            Item.setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        self.Total_Commision.setText(str(total_commision))

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

        CreateAccount.reset_all_account()
        self.Total_Commision.setText("0")

def main():
    app = QApplication(sys.argv)
    ABC_Window = ABC_Simulator_Window()
    ABC_Window.show()
    app.exec_()

if __name__ == '__main__':
    main()
