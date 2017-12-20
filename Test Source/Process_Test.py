


import time
from multiprocessing import Value
from multiprocessing import Process
from DB_Manager_Class import DB_Manager
from WebDriver_Class import WebDriver

id_list = []
password_list = []
email_list = []
gmail_secret_json = []
email_kind = []


# 프로세스를 이용하여 다중 로그인을 할 경우 사용할 메모리 변수
# shared memory 사용 (멀티 프로세스간 변수값 공유)
commissions = Value('d', 0.0)
cash = Value('d', 0.0)
rewards = Value('d', 0.0)
savings = Value('d', 0.0)


def get_id_password(person_name):
    global id_list
    global password_list
    global email_list
    global gmail_secret_json
    global email_kind

    # 가비아 DB 접속
    DB = DB_Manager()

    # 사용자 로그인 정보를 가지고 온다.
    sql = "select * from USER_LOGIN_INFO where user_name = " + "'" + person_name + "'"
    results = DB.get_object_execute_sql(sql)

    # SELECT한 로그인 정보를 리스트에 저장한다.
    for index in range(0, len(results)):
        id_list.append(results[index]['user_id'])
        password_list.append(results[index]['user_password'])
        email_list.append(results[index]['user_email'])
        gmail_secret_json.append(results[index]['user_gmail_secret_json'])
        email_kind.append(results[index]['user_email_kind'])

    print(results[0])


# 각 아이디 별로 로그인을 하여 금액을 합산한다.
def process_browser_to_get_money_with_userid(str_login_id, str_login_password):
    str_Chrome_Path = "../Selenium_Driver/chromedriver"
    str_AirBitClub_Login_URL = "https://www.bitbackoffice.com/auth/login"
    str_Wallet_URL = "https://www.bitbackoffice.com/wallets"

    AirWebDriver = WebDriver(str_Chrome_Path)

    AirWebDriver.move_to_url(str_AirBitClub_Login_URL)
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


def get_account_count():
    return len(id_list)


def report_all_money():
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

    # 집계를 마치고 변수를 초기화 한다.
    commissions.value = 0
    cash.value = 0
    rewards.value = 0
    savings.value = 0


def get_total_bonus_money():

    procs = []

    global id_list
    global password_list

    start_time = time.time()

    for index in range(0, 5):
        #process_browser_to_get_money_with_userid(id_list[index], password_list[index])

        proc = Process(target=process_browser_to_get_money_with_userid, args=(id_list[index], password_list[index]))
        procs.append(proc)
        proc.start()

    # print processing time

    for proc in procs:
        proc.join()

    report_all_money()
    end_time = time.time()
    strmsg = "전체계좌 합산 프로세스 소요시간 : " + str(end_time - start_time)
    print(strmsg)



if __name__ == "__main__":

    get_id_password('이성원')
    get_total_bonus_money()



















