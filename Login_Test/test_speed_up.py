from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from Telegram_Class import Telegram_Manager

str_Chrome_Path = "../Driver/chromedriver"
str_AirBitClub_Login_URL = "https://www.bitbackoffice.com/auth/login"
str_Wallet_URL = "https://www.bitbackoffice.com/wallets"

id_list = []
password_list = []
browser_list = []

chrome_options = Options()
chrome_options.add_argument("--disable-infobars")

commissions = 0
cash = 0
rewards = 0
savings = 0

browser = webdriver.Chrome(executable_path=str_Chrome_Path, chrome_options=chrome_options)

def get_id_password():
    global id_list
    try:
        with open('./lsw_ID_List.txt', 'r') as f:
            for read_line in f:
                id_list.append(read_line.split('/')[0])
                password_list.append(read_line.split('/')[1][:-1])

    except FileNotFoundError as e:
        print(str(e))


def open_login_browser(str_id, str_password):
    global browser
    global browser_list
    global str_AirBitClub_Login_URL

    browser.implicitly_wait(3)
    browser.get(str_AirBitClub_Login_URL)
    browser.find_element_by_name("user[username]").send_keys(str_id)
    browser.find_element_by_name("user[password]").send_keys(str_password)
    browser.find_element_by_xpath('//*[@id="new_user"]/button').click()


def open_wallet_browser():
    global browser
    global commissions
    global cash
    global rewards
    global savings
    global str_Wallet_URL
    global str_AirBitClub_Login_URL

    browser.implicitly_wait(3)
    browser.get(str_Wallet_URL)

    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')

    commissions += float(soup.find_all(class_='dll-quantity dll-container')[0].get_text())
    cash += float(soup.find_all(class_='dll-quantity dll-container')[1].get_text())
    rewards += float(soup.find_all(class_='dll-quantity dll-container')[2].get_text())
    savings += float(soup.find_all(class_='dll-quantity dll-container')[3].get_text())

    browser.implicitly_wait(3)
    #browser.find_element_by_partial_link_text('Logout').click()
    #browser.find_element_by_xpath('//a[@href="/auth/logout"]').click()
    browser.execute_script("logout();")

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

    print("COMMISSIONS : %f" % commissions)
    print("CASH : %f" % cash)
    print("REWARDS : %f" % rewards)
    print("SAVINGS : %f" % savings)

    Telegram_Mng = Telegram_Manager()

    str_commisions = "전체계좌 COMMISIONS 합계 : %.2f" % commissions
    Telegram_Mng.send_message(str_commisions)

    str_cash = "전체계좌 CASH 합계 : %.2f" % cash
    Telegram_Mng.send_message(str_cash)

    str_rewards = "전체계좌 REWARDS 합계 : %.2f" % rewards
    Telegram_Mng.send_message(str_rewards)

    str_savings = "전체계좌 SAVINGS 합계 : %.2f" % savings
    Telegram_Mng.send_message(str_savings)

    str_total = "생성된 계좌의 총 갯수 : %d" % (len(id_list))
    Telegram_Mng.send_message(str_total)

    str_total = "전체 모든 계좌 총 합계(커미션 + 리워드) : %.2f" % (commissions + rewards)
    Telegram_Mng.send_message(str_total)


if __name__ == "__main__":

    get_id_password()

    account_count = get_account_count()

    for index in range(0, account_count):
        open_login_browser(id_list[index], password_list[index])
        open_wallet_browser()

    show_all_money()

    # all_browser_quit()
