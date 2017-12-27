
import datetime
from PDF_Manager_Class import PDF_Manager
from Telegram_Class import Telegram_Manager

def test():
    pdf = PDF_Manager()
    pdf.add_page()

    # 75일 전산비 납부 리스트 보고서 작성
    str_repurchase_list = "75일 도래 전산비 납부 대상 계좌 리스트\n"
    str_repurchase_list += ("lsw120301" + "\n\n\n")

    #  트랜스퍼 후 메인계좌 잔고 보고서 작성
    str_main_transfer = "트랜스퍼 완료 후 메인계좌 현황\n"
    str_rewards = "전체계좌 REWARDS 합계 : %.2f" % 16.3 + "$\n"
    str_commisions = "전체계좌 COMMISIONS 합계 : %.2f" % 34.9 + "$\n"
    str_cash = "전체계좌 CASH 합계 : %.2f" % 0  + "$\n"
    str_savings = "전체계좌 SAVINGS 합계 : %.2f" % 20.9 + "$\n"
    str_total_account = "생성된 계좌의 총 갯수 : %d" % 30 + "$\n"
    str_total = "총 인출 가능 달러(커미션 + 리워드) : %.2f" % 52.2 + "$\n"

    str_main_transfer += str_total_account
    str_main_transfer += str_rewards
    str_main_transfer += str_commisions
    str_main_transfer += str_cash
    str_main_transfer += str_savings
    str_main_transfer += str_total

    print(str_repurchase_list)
    print(str_main_transfer)

    # 보고서 PDF  생성
    #pdf.add_page()
    pdf.print_chapter_user('※ 75일 전산비 납부 대상 계좌 리스트 ※', str_repurchase_list)
    pdf.print_chapter_user('※ 트랜스퍼 완료 후 메인계좌 잔고 보고서 ※', str_main_transfer)

    now = datetime.datetime.now()
    nowDate = now.strftime('%Y-%m-%d')
    rerport_filename = nowDate + ' 계좌현황 보고서.pdf'
    pdf.output(rerport_filename, 'F')

    Telegram_Mng = Telegram_Manager()
    Telegram_Mng.send_file(rerport_filename)



if __name__ == "__main__":
    #test()

    Telegram_Mng = Telegram_Manager()
    updates = Telegram_Mng.get_update_object()
    for u in updates:
        print(u.message)

