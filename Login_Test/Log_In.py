import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from Telegram_Class import Telegram_Manager
from multiprocessing import Process, Value


BASE_DIR = os.path.abspath('.')
TARGET_DIR = os.path.join(BASE_DIR, "DB")
TARGET_FILE = 'test.db'
TARGET_FILE_FULL_PATH = os.path.join(TARGET_DIR, TARGET_FILE)



str_Chrome_Path = "../Driver/chromedriver"
str_AirBitClub_Login_URL = "https://www.bitbackoffice.com/auth/login"
str_Wallet_URL = "https://www.bitbackoffice.com/wallets"

id_list = []
password_list = []
browser_list = []

chrome_options = Options()
chrome_options.add_argument("--disable-infobars")
#chrome_options.add_argument("--ignore-ssl-errors=true")
#chrome_options.add_argument("--ssl-protocol=TLSv1")
#chrome_options.add_argument('--ignore-certificate-errors')

prefs = {'safebrowsing.enabled': 'true'}
chrome_options.add_experimental_option("prefs", prefs)
#chrome_options.add_argument("--window-size=10x10")


commissions = Value('d', 0.0)
cash        = Value('d', 0.0)
rewards     = Value('d', 0.0)
savings     = Value('d', 0.0)

browser = None

def get_id_password():

    global id_list
    global password_list


    try:
        f = open("./lsw_ID_List.txt", 'r')
        read_line = f.readlines()

        for line in read_line:
            if len(line) > 0 and line != '\n':
                id_list.append(line.split('/')[0])
                password_list.append(line.split('/')[1].rstrip('\n'))

        f.close()

    except FileNotFoundError as e:
        print(str(e))


def process_browser(str_id, str_password, commissions, cash, rewards, savings):

    global browser
    global browser_list
    global str_AirBitClub_Login_URL
    global str_Wallet_URL
    global chrome_options
    global str_Chrome_Path

    browser = webdriver.Chrome(executable_path=str_Chrome_Path, chrome_options=chrome_options)
    #browser.set_window_size(10, 10)
    #browser.set_window_position(-10000, 0)

    browser.implicitly_wait(2)
    browser.get(str_AirBitClub_Login_URL)
    browser.find_element_by_name("user[username]").send_keys(str_id)
    browser.find_element_by_name("user[password]").send_keys(str_password)
    browser.find_element_by_xpath('//*[@id="new_user"]/button').click()
    #browser.find_element_by_xpath('// *[ @ id = "login"] / div[2] / div / div[2] / form / button').click()

    browser.implicitly_wait(2)
    browser.get(str_Wallet_URL)

    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')


    commissions.value += float(soup.find_all(class_='dll-quantity dll-container')[0].get_text())
    cash.value += float(soup.find_all(class_='dll-quantity dll-container')[1].get_text())
    rewards.value += float(soup.find_all(class_='dll-quantity dll-container')[2].get_text())
    savings.value += float(soup.find_all(class_='dll-quantity dll-container')[3].get_text())

    browser.quit()


def get_account_count():
    return len(id_list)

def all_browser_quit():

    """
    global browser_list

    for index in range(0, len(browser_list)):
        browser_list[index].quit()
    """

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

if __name__   == "__main__":

    start_time = time.time()

    procs = []

    get_id_password()

    account_count = get_account_count()
    for i in range(0,50):
        for index in range(0, account_count):
            process_browser(id_list[index], password_list[index], commissions, cash, rewards, savings)

        #proc = Process(target=process_browser, args=(id_list[index], password_list[index], commissions, cash, rewards, savings))
        #procs.append(proc)
        #proc.start()

    end_time = time.time()

    # print processing time

    print(end_time - start_time)
    #for proc in procs:
    #   proc.join()


    show_all_money()




