
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
cash        = 0
rewards     = 0
savings     = 0

browser = None

def get_id_password():
    try:
        with open('./ID_List.txt', 'r') as f:
            for read_line in f:
                id_list.append(read_line.split('/')[0])
                password_list.append(read_line.split('/')[1][:-1])

    except FileNotFoundError as e:
        print(str(e))

def open_login_browser(str_id, str_password):

    global browser
    global browser_list
    global str_AirBitClub_Login_URL

    browser = webdriver.Chrome(executable_path=str_Chrome_Path, chrome_options=chrome_options)

    browser.implicitly_wait(1)
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

    browser.implicitly_wait(1)
    browser.get(str_Wallet_URL)

    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')

    commissions += float(soup.find_all(class_='dll-quantity dll-container')[0].get_text())
    cash        += float(soup.find_all(class_='dll-quantity dll-container')[1].get_text())
    rewards     += float(soup.find_all(class_='dll-quantity dll-container')[2].get_text())
    savings     += float(soup.find_all(class_='dll-quantity dll-container')[3].get_text())

    browser.quit()


def all_browser_quit():

    """
    global browser_list

    for index in range(0, len(browser_list)):
        browser_list[index].quit()
    """

def show_all_money():
    print("COMMISSIONS : %f" % commissions)
    print("CASH : %f" % cash)
    print("REWARDS : %f" % rewards)
    print("SAVINGS : %f" % savings)


    Telegram_Mng = Telegram_Manager()

    str_commisions = "Total COMMISIONS : " + str(commissions)
    Telegram_Mng.send_message(str_commisions)

    str_cash = "Total CASH : " + str(cash)
    Telegram_Mng.send_message(str_cash)

    str_rewards = "Total REWARDS : " + str(rewards)
    Telegram_Mng.send_message(str_rewards)

    str_savings = "Total SAVINGS : " + str(savings)
    Telegram_Mng.send_message(str_savings)

    str_total = "Total Available Money : " + str(commissions+rewards)
    Telegram_Mng.send_message(str_total)



if __name__   == "__main__":

    get_id_password()

    for index in range(0, len(id_list)-1):
        open_login_browser(id_list[index], password_list[index])
        open_wallet_browser()


    show_all_money()

    # all_browser_quit()
