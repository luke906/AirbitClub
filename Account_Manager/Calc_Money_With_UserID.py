
import time
import pyautogui
from multiprocessing import Value

from DB_Manager_Class import DB_Manager
from Telegram_Class import Telegram_Manager

from Gmail_Manager_Class import Gmail_Manager
from Schedule_Manager_Class import Schedule_Manager
from WebDriver_Class import WebDriver

id_list = []
password_list = []
email_list = []
gmail_secret_json = []
email_kind = []

#트랜스퍼 속도 개선을 위해서 커미션리스트를 만든다.
comissions_list_dic = {}

# 프로세스를 이용하여 다중 로그인을 할 경우 사용할 메모리 변수
# shared memory 사용 (멀티 프로세스간 변수값 공유)
commissions = Value('d', 0.0)
cash = Value('d', 0.0)
rewards = Value('d', 0.0)
savings = Value('d', 0.0)

# 트랜스퍼 하기위한 토큰 값
_REQUEST_TOKEN_VALUE = None

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

    pyautogui.click(100, 100)

    time.sleep(100)
    AirWebDriver.move_to_url(str_Wallet_URL)

    soup = AirWebDriver.get_soup_object()

    commissions.value += float(soup.find_all(class_='dll-quantity dll-container')[0].get_text())
    cash.value += float(soup.find_all(class_='dll-quantity dll-container')[1].get_text())
    rewards.value += float(soup.find_all(class_='dll-quantity dll-container')[2].get_text())
    savings.value += float(soup.find_all(class_='dll-quantity dll-container')[3].get_text())

    AirWebDriver.quit_browser()


# 각 아이디 별로 남은 리워드 지급일수, 재구매일 여부 판별
def process_browser_to_get_left_day(str_login_id, str_login_password):

    str_Chrome_Path = "../Selenium_Driver/chromedriver"
    str_AirBitClub_Login_URL = "https://www.bitbackoffice.com/auth/login"
    str_Wallet_URL = "https://www.bitbackoffice.com/wallets"

    AirWebDriver = WebDriver(str_Chrome_Path)
    AirWebDriver.move_to_url(str_AirBitClub_Login_URL)
    AirWebDriver.send_key_by_name("user[username]", str_login_id)
    AirWebDriver.send_key_by_name("user[password]", str_login_password)
    AirWebDriver.send_click_event_with_xpath('//*[@id="new_user"]/button')

    # 75일 시점에서 재구매 창이 최상단으로 POPUP 될 경우 하단의 엘리먼트로 접근이 안되기 때문에
    # 강제로 마우스 클릭을 하여 POPUP 창을 닫는다.
    pyautogui.click(100, 100)
    AirWebDriver.move_to_url(str_Wallet_URL)
    #time.sleep(100)

    soup = AirWebDriver.get_soup_object()

    potential_revenue_day = int(soup.find_all(class_='counter-container')[0].countdown)
    left_time_to_rewards  = int(soup.find_all(class_='counter-container')[1].countdown)
    remain_business_day   = int(soup.find_all(class_='counter-container')[2].countdown)
    remain_repurchase_day = int(soup.find_all(class_='counter-container')[3].countdown)

    print("remain_business_day : %d", remain_business_day)
    print("remain_repurchase_day : %d", remain_repurchase_day)







def clear_mail_box_before_transfer(secret_json_file):

    Gmail = Gmail_Manager()
    Gmail.get_credentials(secret_json_file)
    Gmail.get_unread_message()



def get_airbit_token_value(secret_json_file):

    print("get_airbit_token_value JOB START!")

    global _REQUEST_TOKEN_VALUE

    _REQUEST_TOKEN_VALUE = None
    Gmail = Gmail_Manager()
    Gmail.get_credentials(secret_json_file)

    unread_message_count = Gmail.get_unread_message_count()

    # 읽지 않은 메세지가 존재 한다면
    if unread_message_count > 0:
        #print(message_list[0]['Snippet'])
        #print(message_list[0]['Sender'])

        message_list = Gmail.get_unread_message()
        # 32자리 토큰을 구한다.
        # 가장 최신의 첫번째 메일의 메세지 간략 보기 내용을 스페이스로 구분하여 모두 검사한다.
        for sub in message_list[0]['Snippet'].split(' '):
            #수신 메일의 제목이 "Token for your TRANSFER" 인지 검사, 전송자가 에어비트이고 메세지 본문중 32자리 토큰 이라면
            if message_list[0]['Subject'][0:23] == "Token for your TRANSFER" and \
                     message_list[0]['Sender'] == "<servers@bitbackoffice.com>" and \
                                      len(sub) == 32:
                _REQUEST_TOKEN_VALUE = sub
                # scheduler.shutdown_schedule()
                break


def transfer_money_to(wallet, str_destination_id, str_login_id, str_login_password, str_credential_filename, index=-1):

    global _REQUEST_TOKEN_VALUE
    global comissions_list_dic

    print("start transfer %s" % str_login_id)
    str_Chrome_Path = "../Selenium_Driver/chromedriver"
    str_AirBitClub_Login_URL = "https://www.bitbackoffice.com/auth/login"
    str_Transfer_URL = "https://www.bitbackoffice.com/transfers"

    AirWebDriver = WebDriver(str_Chrome_Path)

    AirWebDriver.move_to_url(str_AirBitClub_Login_URL)
    AirWebDriver.send_key_by_name("user[username]", str_login_id)
    AirWebDriver.send_key_by_name("user[password]", str_login_password)
    AirWebDriver.send_click_event_with_xpath('//*[@id="new_user"]/button')
    AirWebDriver.move_to_url(str_Transfer_URL)

    # 현재 해당 계정의 월릿 금액을 구한다.
    soup = AirWebDriver.get_soup_object()
    _commissions = float(soup.find_all("small")[1].get_text())

    if index is not -1:
        comissions_list_dic[index] = _commissions

    _cash = float(soup.find_all("small")[2].get_text())
    _rewards = float(soup.find_all("small")[3].get_text())

    print("commissions: %f" % _commissions)
    print("cash: %f" % _cash)
    print("rewards: %f" % _rewards)

    # 만일 이체할 금액이 없다면 종료한다.
    if (_rewards + _commissions) <= 0:
        print("there is no money to transfer")
        AirWebDriver.quit_browser()
        return

    # 커미션에 금액이 있다면 커미션 이체를 한다.(0)
    # //*[@id="partition_transfer_partition_user_wallet_id"]/option[2]


    if _commissions > 0 and wallet == "commissions":

        mail_scheduler = Schedule_Manager()

        # 트랜스퍼할 아이디를 입력한다.
        AirWebDriver.send_key_by_id("search-user", str_destination_id)

        # 검색버튼을 누른다.
        AirWebDriver.send_click_event_with_xpath('//*[@id="search-btn"]')

        # 커미션 지갑 선택
        # //*[@id="partition_transfer_partition_user_wallet_id"]/option[4]
        AirWebDriver.send_click_event_with_xpath('//*[@id="partition_transfer_partition_user_wallet_id"]/option[4]')
        AirWebDriver.select_option_by_id_text("partition_transfer_partition_user_wallet_id", "commissions")
        
        # 전송할 커미션 금액 입력
        AirWebDriver.send_key_by_id('partition_transfer_partition_amount', str(_commissions))

        # 토큰 요청 버튼을 누른다.
        # //*[@id="submit-token"]
        AirWebDriver.send_click_event_with_xpath('//*[@id="submit-token"]')

        # 토큰을 요청하고 메일에서 토큰을 받아온다.
        mail_scheduler.start_scheduler_interval(get_airbit_token_value, "token_job_commissions", 3, str_credential_filename)


        # 이메일 확인 후 토큰을 얻어 올때 까지 대기
        while 1:
            if _REQUEST_TOKEN_VALUE is not None and len(_REQUEST_TOKEN_VALUE) is 32:
                mail_scheduler.kill_scheduler("token_job_commissions")
                print("Request Token for commissions is : %s" % _REQUEST_TOKEN_VALUE)
                print("get_airbit_token_value JOB STOP!")
                break

        # 토큰 입력
        # id = partition_transfer_partition_token
        AirWebDriver.send_key_by_id('partition_transfer_partition_token', str(_REQUEST_TOKEN_VALUE))
        _REQUEST_TOKEN_VALUE = None #다음번 조회를 위해서 토큰 초기화

        # 트랜스퍼 실행
        # //*[@id="submit-transfer"]
        print("send rewards money : %f" % _commissions)
        AirWebDriver.send_click_event_with_xpath('//*[@id="submit-transfer"]')

        # 트랜스퍼 실행 후 잠시 대기
        time.sleep(3)
        AirWebDriver.move_to_url(str_AirBitClub_Login_URL)

        # 종료
        AirWebDriver.quit_browser()

    # 리워드에 금액이 있다면 리워드 이체를 한다.(1)
    # //*[@id="partition_transfer_partition_user_wallet_id"]/option[3]
    if _rewards > 0 and wallet == "rewards":

        mail_scheduler = Schedule_Manager()

        # 트랜스퍼할 아이디를 입력한다.
        AirWebDriver.send_key_by_id("search-user", str_destination_id)

        # 검색버튼을 누른다.
        AirWebDriver.send_click_event_with_xpath('//*[@id="search-btn"]')

        # 리워드 지갑 선택
        # //*[@id="partition_transfer_partition_user_wallet_id"]/option[2]
        #AirWebDriver.send_click_event_with_xpath('//*[@id="partition_transfer_partition_user_wallet_id"]/option[2]')
        AirWebDriver.select_option_by_id_text("partition_transfer_partition_user_wallet_id", "rewards")

        # 전송할 리워드 금액 입력
        AirWebDriver.send_key_by_id('partition_transfer_partition_amount', str(_rewards))

        # 토큰 요청 버튼을 누른다.
        # //*[@id="submit-token"]
        AirWebDriver.send_click_event_with_xpath('//*[@id="submit-token"]')

        # 토큰을 요청하고 메일에서 토큰을 받아온다.
        mail_scheduler.start_scheduler_interval(get_airbit_token_value, "token_job_rewards", 3, str_credential_filename)

        # 이메일 확인 후 토큰을 얻어 올때 까지 대기
        while 1:
            if _REQUEST_TOKEN_VALUE is not None and len(_REQUEST_TOKEN_VALUE) is 32:
                mail_scheduler.kill_scheduler("token_job_rewards")
                print("Request Token for rewards is : %s" % _REQUEST_TOKEN_VALUE)
                print("get_airbit_token_value JOB STOP!")
                break

        # 토큰 입력
        # id = partition_transfer_partition_token
        AirWebDriver.send_key_by_id('partition_transfer_partition_token', str(_REQUEST_TOKEN_VALUE))
        _REQUEST_TOKEN_VALUE = None #다음번 조회를 위해서 토큰 초기화

        # 트랜스퍼 실행
        # //*[@id="submit-transfer"]
        print("send rewards money : %f" % _rewards )
        AirWebDriver.send_click_event_with_xpath('//*[@id="submit-transfer"]')

        # 트랜스퍼 실행 후 잠시 대기
        time.sleep(3)
        AirWebDriver.move_to_url(str_AirBitClub_Login_URL)

        # 종료
        AirWebDriver.quit_browser()

    # 종료
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

    # 집계를 마치고 변수를 초기화 한다.
    commissions.value = 0
    cash.value = 0
    rewards.value = 0
    savings.value = 0

    print(str_commisions)
    print(str_cash)
    print(str_rewards)
    print(str_savings)
    print(str_total_account)
    print(str_total)

    Telegram_Mng = Telegram_Manager()
    Telegram_Mng.send_message(str_commisions)
    Telegram_Mng.send_message(str_cash)
    Telegram_Mng.send_message(str_rewards)
    Telegram_Mng.send_message(str_savings)
    Telegram_Mng.send_message(str_total_account)
    Telegram_Mng.send_message(str_total)

def get_total_bonus_money():
    # procs = []

    global id_list
    global password_list

    Telegram_Mng = Telegram_Manager()
    start_time = time.time()

    for index in range(0, get_account_count()):
        process_browser_to_get_money_with_userid(id_list[index], password_list[index])

            # proc = Process(target=process_browser, args=(id_list[index], password_list[index])
            # procs.append(proc)
            # proc.start()

    # print processing time

    # for proc in procs:
    #   proc.join()
    report_all_money()
    end_time = time.time()
    strmsg = "전체계좌 합산 프로세스 소요시간 : " + str(end_time - start_time)
    Telegram_Mng.send_message(strmsg)

    transfer_all_money_to_main_account()

def transfer_all_money_to_main_account():

    global id_list
    global password_list
    global gmail_secret_json
    global comissions_list_dic

    Telegram_Mng = Telegram_Manager()
    start_time = time.time()

    #transfer_money_to(main_account, "lsw120302", "lsw8954!", "gmail-python-chargerunit01.json")

    # 트랜스퍼 하기전에 메일을 청소 한다.
    clear_mail_box_before_transfer("gmail-python-chargerunit01.json")
    clear_mail_box_before_transfer("gmail-python-chargerunit03.json")
    clear_mail_box_before_transfer("gmail-python-chargerunit05.json")
    clear_mail_box_before_transfer("gmail-python-chargerunit07.json")

    # 메인 계좌 다음 계좌부터 리워드만 트랜스퍼 샐행.
    for index in range(12, get_account_count()):
        transfer_money_to("rewards", id_list[0], id_list[index], password_list[index], gmail_secret_json[index], index)

    # 메인 계좌 다음 계좌부터 커미션만 트랜스퍼 샐행.
    # 커미션이 있는 계좌만 트랜스퍼 실행 (속도 단축을 위해서)
    for index in range(12, get_account_count()):
        if comissions_list_dic[index] > 0:
            transfer_money_to("commissions", id_list[0], id_list[index], password_list[index], gmail_secret_json[index])

    end_time = time.time()
    strmsg = "트랜스퍼 프로세스 소요시간 : " + str(end_time - start_time)
    Telegram_Mng.send_message(strmsg)

    get_screent_shot_with_login_id(id_list[0], "lsw8954!")


def get_screent_shot_with_login_id(str_login_id, str_login_password):
    str_Chrome_Path = "../Selenium_Driver/chromedriver"
    str_AirBitClub_Login_URL = "https://www.bitbackoffice.com/auth/login"
    str_Wallet_URL = "https://www.bitbackoffice.com/wallets"

    AirWebDriver = WebDriver(str_Chrome_Path)

    AirWebDriver.move_to_url(str_AirBitClub_Login_URL)
    AirWebDriver.send_key_by_name("user[username]", str_login_id)
    AirWebDriver.send_key_by_name("user[password]", str_login_password)
    AirWebDriver.send_click_event_with_xpath('//*[@id="new_user"]/button')
    AirWebDriver.move_to_url(str_Wallet_URL)

    AirWebDriver.save_screenshot("main_account.png")

    Telegram_Mng = Telegram_Manager()
    Telegram_Mng.send_image("main_account.png")


if __name__ == "__main__":

    get_id_password('이성원')
    #get_total_bonus_money()
    #process_browser_to_get_left_day("lsw120300", "lsw8954!")

    transfer_all_money_to_main_account()

    """
    scheduler = Schedule_Manager()
    #scheduler.start_scheduler_cron(transfer_all_money_to_main_account, 'mon-sat', 2, 00)
    print("start scheduler transfer")

    scheduler.start_scheduler_cron(get_total_bonus_money, 'mon-sat', 2, 0)
    print("start scheduler get_total_bonus_money")
    """























