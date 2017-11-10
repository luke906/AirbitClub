import os
import time
from Telegram_Class import Telegram_Manager
from multiprocessing import Process, Value
from WebDriver_Class import WebDriver
from bs4 import BeautifulSoup

BASE_DIR = os.path.abspath('.')
TARGET_DIR = os.path.join(BASE_DIR, "DB")
TARGET_FILE = 'test.db'
TARGET_FILE_FULL_PATH = os.path.join(TARGET_DIR, TARGET_FILE)

id_list = []
password_list = []
browser_list = []

# shared memory 사용 (멀티 프로세스간 변수값 공유)
commissions = Value('d', 0.0)
cash = Value('d', 0.0)
rewards = Value('d', 0.0)
savings = Value('d', 0.0)

browser = None


def get_id_password():
    global id_list
    global password_list

    try:
        f = open("./ID_List.txt", 'r')
        read_line = f.readlines()

        for line in read_line:
            if len(line) > 0 and line != '\n':
                id_list.append(line.split('/')[0])
                password_list.append(line.split('/')[1].rstrip('\n'))

        f.close()

    except FileNotFoundError as e:
        print(str(e))


def process_browser_to_get_money_with_userid(str_id, str_password, commissions, cash, rewards, savings):
    global browser
    global browser_list
    global str_AirBitClub_Login_URL
    global str_Wallet_URL

    str_Chrome_Path = "../Driver/chromedriver"
    str_AirBitClub_Login_URL = "https://www.bitbackoffice.com/auth/login"
    str_Wallet_URL = "https://www.bitbackoffice.com/wallets"

    AirWebDriver = WebDriver(str_Chrome_Path)

    AirWebDriver.move_to_url((str_AirBitClub_Login_URL))
    AirWebDriver.send_key_by_name("user[username]", str_id)
    AirWebDriver.send_key_by_name("user[password]", str_password)
    AirWebDriver.send_click_event_with_xpath('//*[@id="new_user"]/button')
    AirWebDriver.move_to_url(str_Wallet_URL)

    soup = AirWebDriver.get_soup_object()

    commissions.value += float(soup.find_all(class_='dll-quantity dll-container')[0].get_text())
    cash.value += float(soup.find_all(class_='dll-quantity dll-container')[1].get_text())
    rewards.value += float(soup.find_all(class_='dll-quantity dll-container')[2].get_text())
    savings.value += float(soup.find_all(class_='dll-quantity dll-container')[3].get_text())

#    AirWebDriver.quit_browser()



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

    get_id_password()
    get_total_commission_rewards_money()
    show_all_money()




