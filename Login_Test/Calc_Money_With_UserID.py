import os
import time
from Telegram_Class import Telegram_Manager
from multiprocessing import Process, Value
from WebDriver_Class import WebDriver
from DB_Manager_Class import DB_Manager
from bs4 import BeautifulSoup

BASE_DIR = os.path.abspath('.')
TARGET_DIR = os.path.join(BASE_DIR, "DB")
TARGET_FILE = 'test.db'
TARGET_FILE_FULL_PATH = os.path.join(TARGET_DIR, TARGET_FILE)

id_list = []
password_list = []
email_list = []

# shared memory 사용 (멀티 프로세스간 변수값 공유)
commissions = Value('d', 0.0)
cash = Value('d', 0.0)
rewards = Value('d', 0.0)
savings = Value('d', 0.0)


def get_id_password():

    """
    global id_list
    global password_list

    try:
        f = open("./ID_List.txt", 'r')
        read_line = f.readlines()

        for line in read_line:
            if len(line) > 0 and line != '\n':
                id_list.append(line.split('/')[0])
                password_list.append(line.split('/')[1])
                email_list.append(line.split('/')[2].rstrip('\n'))

        f.close()

    except FileNotFoundError as e:
        print(str(e))
    """
    DB = DB_Manager()

    sql = "select * from USER_LOGIN_INFO"
    DB.execute_sql(sql)
    results = DB.get_db_result()

    for index in range(0, len(results)):
        id_list.append(results[index]['user_id'])
        password_list.append(results[index]['user_password'])
        email_list.append(results[index]['user_email'])

    #print(results[0])


def process_browser_to_get_money_with_userid(str_login_id, str_login_password, commissions, cash, rewards, savings):

    str_Chrome_Path = "../Driver/chromedriver"
    str_AirBitClub_Login_URL = "https://www.bitbackoffice.com/auth/login"
    str_Wallet_URL = "https://www.bitbackoffice.com/wallets"

    AirWebDriver = WebDriver(str_Chrome_Path)

    AirWebDriver.move_to_url((str_AirBitClub_Login_URL))
    AirWebDriver.send_key_by_name("user[username]", str_login_id)
    AirWebDriver.send_key_by_name("user[password]", str_login_password)
    AirWebDriver.send_click_event_with_xpath('//*[@id="new_user"]/button')
    AirWebDriver.move_to_url(str_Wallet_URL)

    soup = AirWebDriver.get_soup_object()

    commissions.value += float(soup.find_all(class_='dll-quantity dll-container')[0].get_text())
    cash.value += float(soup.find_all(class_='dll-quantity dll-container')[1].get_text())
    rewards.value += float(soup.find_all(class_='dll-quantity dll-container')[2].get_text())
    savings.value += float(soup.find_all(class_='dll-quantity dll-container')[3].get_text())

    AirWebDriver.quit_browser()

def transfer_money_to(str_login_id, str_login_password, str_destination_id):
    str_Chrome_Path = "../Driver/chromedriver"
    str_AirBitClub_Login_URL = "https://www.bitbackoffice.com/auth/login"
    str_Transfer_URL = "https://www.bitbackoffice.com/transfers"

    AirWebDriver = WebDriver(str_Chrome_Path)

    AirWebDriver.move_to_url((str_AirBitClub_Login_URL))
    AirWebDriver.send_key_by_name("user[username]", str_login_id)
    AirWebDriver.send_key_by_name("user[password]", str_login_password)
    AirWebDriver.send_click_event_with_xpath('//*[@id="new_user"]/button')
    AirWebDriver.move_to_url(str_Transfer_URL)

    # 트랜스퍼할 아이디를 입력한다.
    AirWebDriver.send_key_by_id("search-user", str_destination_id)

    # 검색버튼을 누른다.
    AirWebDriver.send_click_event_with_xpath('//*[@id="search-btn"]')

    # 현재 해당 계정의 월릿 금액을 구한다.
    soup = AirWebDriver.get_soup_object()
    commissions = float(soup.find_all("small")[1].get_text())
    rewards = float(soup.find_all("small")[3].get_text())
    cash = float(soup.find_all("small")[2].get_text())


    print("commissions: %f" % commissions)
    print("cash: %f" % cash)
    print("rewards: %f" % rewards)

    # 커미션에 금액이 있다면 커미션 이체를 한다.(0)
    # //*[@id="partition_transfer_partition_user_wallet_id"]/option[2]
    if commissions > 0:
        # 커미션 지갑 선택
        AirWebDriver.send_click_event_with_xpath('//*[@id="partition_transfer_partition_user_wallet_id"]/option[2]')
        # 전송할 커미션 입력
        AirWebDriver.send_key_by_id('partition_transfer_partition_amount', str(commissions))

    # 리워드에 금액이 있다면 리워드 이체를 한다.(1)
    # //*[@id="partition_transfer_partition_user_wallet_id"]/option[3]
    if rewards > 0:
        # 커미션 지갑 선택
        AirWebDriver.send_click_event_with_xpath('//*[@id="partition_transfer_partition_user_wallet_id"]/option[3]')
        # 전송할 커미션 입력
        AirWebDriver.send_key_by_id('partition_transfer_partition_amount', str(rewards))

def get_account_count():
    return len(id_list)


def show_all_money():
    global id_list

    str_commisions = "전체계좌 COMMISIONS 합계 : %.2f" % commissions.value
    str_cash = "전체계좌 CASH 합계 : %.2f" % cash.value
    str_rewards = "전체계좌 REWARDS 합계 : %.2f" % rewards.value
    str_savings = "전체계좌 SAVINGS 합계 : %.2f" % savings.value
    str_total_account = "생성된 계좌의 총 갯수 : %d" % (len(id_list))
    str_total = "전체 모든 계좌 총 합계(커미션 + 리워드) : %.2f" % (commissions.value + rewards.value)

    print(str_commisions)
    print(str_cash)
    print(str_rewards)
    print(str_savings)
    print(str_total_account)
    print(str_total)

    """
    Telegram_Mng = Telegram_Manager()
    Telegram_Mng.send_message(str_commisions)
    Telegram_Mng.send_message(str_cash)
    Telegram_Mng.send_message(str_rewards)
    Telegram_Mng.send_message(str_savings)
    Telegram_Mng.send_message(str_total_account)
    Telegram_Mng.send_message(str_total)
    """


def get_total_commission_rewards_money():
    # procs = []

    start_time = time.time()

    for index in range(0, get_account_count()):
        process_browser_to_get_money_with_userid(id_list[index],
                                                 password_list[index],
                                                 commissions,
                                                 cash,
                                                 rewards,
                                                 savings)

            # proc = Process(target=process_browser, args=(id_list[index], password_list[index], commissions, cash, rewards, savings))
            # procs.append(proc)
            # proc.start()

    end_time = time.time()

    # print processing time

    print(end_time - start_time)
    # for proc in procs:
    #   proc.join()


if __name__ == "__main__":

    """
    get_id_password()
    get_total_commission_rewards_money()
    show_all_money()
    """
    
    transfer_money_to("lsw120301", "lsw8954!", "lsw120300")

    time.sleep(600)




