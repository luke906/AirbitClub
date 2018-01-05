
import time
import datetime
from multiprocessing import Value

from DB_Manager_Class import DB_Manager
from Telegram_Class import Telegram_Manager

from Gmail_Manager_Class import Gmail_Manager
from Schedule_Manager_Class import Schedule_Manager
from WebDriver_Class import WebDriver_Manager
from PDF_Manager_Class import PDF_Manager

id_list = []
repurchase_id_list = []
password_list = []
email_list = []
gmail_secret_json = []
email_kind = []

#트랜스퍼 속도 개선을 위해서 커미션리스트를 만든다.
comissions_list_dic = {}

#보고서 제출용
remaining_business_day_dic = {}
repurchase_left_list_dic = {}

#진행중 실패한 아이디 목록
login_fail_id_index_list = []

# 프로세스를 이용하여 다중 로그인을 할 경우 사용할 메모리 변수
# shared memory 사용 (멀티 프로세스간 변수값 공유)
commissions = Value('d', 0.0)
cash = Value('d', 0.0)
rewards = Value('d', 0.0)
savings = Value('d', 0.0)

# 트랜스퍼 하기위한 토큰 값
_REQUEST_TOKEN_VALUE = None

#browser_flag
browser_flag = 'firefox'

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

    DB.close_db()

    print(results[0])

# 각 아이디 별로 로그인을 하여 금액을 합산한다.
def process_browser_to_get_money_with_userid(str_login_id, str_login_password):

    str_AirBitClub_Login_URL = "https://www.bitbackoffice.com/auth/login"
    str_Wallet_URL = "https://www.bitbackoffice.com/wallets"

    print("웹 드라이버 로딩 시작")
    initialize = -1
    AirWebDriver = WebDriver_Manager(browser_flag, initialize)
    if initialize == 0:
        print('각 아이디 별로 로그인을 하여 금액을 합산 웹 드라이버 초기 로딩 실패')
        login_fail_id_index_list.append(index)
        AirWebDriver.quit_browser()

    AirWebDriver.move_to_url(str_AirBitClub_Login_URL)
    AirWebDriver.send_key_by_name("user[username]", str_login_id)
    AirWebDriver.send_key_by_name("user[password]", str_login_password)
    AirWebDriver.send_click_event_with_xpath('//*[@id="new_user"]/button')

    print('웰릿 화면 로딩 시도')
    AirWebDriver.move_to_url(str_Wallet_URL)
    print('웰릿 화면 로딩 성공 cash css로딩 대기중..')

    #div.col-md-6:nth-child(2)>div:nth-child(1)>div:nth-child(2)>p:nth-child(2)
    css_path = 'div.col-md-6:nth-child(2)>div:nth-child(1)>div:nth-child(2)>p:nth-child(2)'
    time.sleep(5)
    if (AirWebDriver.wait_until_show_element_css(css_path)) is not True:
        print('웰릿 화면 로딩 성공 cash css로딩 실패')
        AirWebDriver.quit_browser()
        return False

    print('웰릿 화면 로딩 성공 cash css로딩 성공')
    time.sleep(3)
    soup = AirWebDriver.get_soup_object()

    commissions.value += float(soup.find_all(class_='dll-quantity dll-container')[0].get_text())
    cash.value += float(soup.find_all(class_='dll-quantity dll-container')[1].get_text())
    rewards.value += float(soup.find_all(class_='dll-quantity dll-container')[2].get_text())
    savings.value += float(soup.find_all(class_='dll-quantity dll-container')[3].get_text())

    AirWebDriver.quit_browser()


# 각 아이디 별로 남은 리워드 지급일수, 재구매일 여부 판별
def process_browser_to_get_left_day(str_login_id, str_login_password):

    str_AirBitClub_Login_URL = "https://www.bitbackoffice.com/auth/login"
    str_Wallet_URL = "https://www.bitbackoffice.com/wallets"

    initialize = -1
    AirWebDriver = WebDriver_Manager(browser_flag, initialize)
    AirWebDriver.move_to_url(str_AirBitClub_Login_URL)
    AirWebDriver.send_key_by_name("user[username]", str_login_id)
    AirWebDriver.send_key_by_name("user[password]", str_login_password)
    AirWebDriver.send_click_event_with_xpath('//*[@id="new_user"]/button')

    # 75일 시점에서 재구매 창이 최상단으로 POPUP 될 경우 하단의 엘리먼트로 접근이 안되기 때문에
    # 강제로 마우스 클릭을 하여 POPUP 창을 닫는다.
    #pyautogui.click(100, 100)
    #AirWebDriver.move_to_url(str_Wallet_URL)
    #time.sleep(100)

    soup = AirWebDriver.get_soup_object()

    remain_business_day   = int(soup.find_all(class_='counter-container')[2].get('countdown'))
    remain_repurchase_day = int(soup.find_all(class_='counter-container')[3].get('countdown'))

    print("remain_business_day : %d" % remain_business_day)
    print("remain_repurchase_day : %d" % remain_repurchase_day)

    # //*[@id="rew-daily-home"]


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

def transfer_all_money_to_main_account(start_index, end_index):

    global id_list
    global password_list
    global gmail_secret_json
    global comissions_list_dic

    #Telegram_Mng = Telegram_Manager()
    #start_time = time.time()

    #transfer_money_to(main_account, "lsw120302", "lsw8954!", "gmail-python-chargerunit01.json")

    # 트랜스퍼 하기전에 메일을 청소 한다.
    clear_mail_box_before_transfer("gmail-python-chargerunit01.json")
    clear_mail_box_before_transfer("gmail-python-chargerunit03.json")
    clear_mail_box_before_transfer("gmail-python-chargerunit05.json")
    clear_mail_box_before_transfer("gmail-python-chargerunit07.json")

    # 메인 계좌 다음 계좌부터 리워드만 트랜스퍼 샐행.
    for index in range(start_index, end_index):
        print("리워드 트랜스퍼 인덱스 : %d"%index)
        result = transfer_reward_money(index, id_list[0], id_list[index], password_list[index], gmail_secret_json[index])
        if result is False:
            continue


    # 메인 계좌 다음 계좌부터 커미션만 트랜스퍼 샐행.
    # 커미션이 있는 계좌만 트랜스퍼 실행 (속도 단축을 위해서)
    for index in range(start_index, end_index):
        print("커미션 트랜스퍼 시작 인덱스 : %d" % index)
        #75일 재구매 대상인 아이디는 이체를 건너뛴다.
        if id_list[index] in repurchase_id_list:
            print("%s 아이디 재구매 대상 커미션 이체 패스" % id_list[index])
            continue

        if comissions_list_dic[id_list[index]] > 0:
            print("커미션 트랜스퍼 시작  : %s" % id_list[index])
            transfer_commission_money(index, id_list[0], id_list[index], password_list[index], gmail_secret_json[index])

    # 프로세스 실패한 아이디 리스트
    for id in login_fail_id_index_list:
        print("프로세스 실패한 아이디 : %s" % id_list[id])
    #end_time = time.time()
    #strmsg = "트랜스퍼 프로세스 소요시간 : " + str(end_time - start_time)
    #Telegram_Mng.send_message(strmsg)

    #get_screent_shot_with_login_id(id_list[0], "lsw8954!")
    process_browser_to_get_money_with_userid("lsw120300", "lsw8954!")
    report_account()


def transfer_reward_money(index, str_destination_id, str_login_id, str_login_password, str_credential_filename):

    global _REQUEST_TOKEN_VALUE, _rewards
    global comissions_list_dic
    global remaining_business_day_dic
    global repurchase_left_list_dic
    global login_fail_id_list

    # 프로세스 실패 흐름 판별
    process_success_flag = 1

    print("start rewards transfer %s" % str_login_id)
    str_AirBitClub_Main = "https://www.bitbackoffice.com"
    str_AirBitClub_Home_URL = "https://www.bitbackoffice.com/#"
    str_AirBitClub_Login_URL = "https://www.bitbackoffice.com/auth/login"
    str_Transfer_URL = "https://www.bitbackoffice.com/transfers"
    str_Wallet_URL = "https://www.bitbackoffice.com/wallets"


    print("웹 드라이버 로딩 시작")
    initialize = -1
    AirWebDriver = WebDriver_Manager(browser_flag, initialize)
    if initialize == 0:
        print('리워드 이체 웹 드라이버 초기 로딩 실패')
        login_fail_id_index_list.append(index)
        AirWebDriver.quit_browser()
        return False

    print("웹 드라이버 로딩 성공")


    try:
        print("로그인 사이트 접속 시도")
        AirWebDriver.move_to_url(str_AirBitClub_Login_URL)
        print('로그인 페이지 패스워드 입력란 xpath 대기중..')
        time.sleep(2)
        AirWebDriver.wait_until_show_element_xpath('//*[@id="user_password"]')
        print("로그인 사이트 아이디 입력 ...")
        AirWebDriver.send_key_by_name("user[username]", str_login_id)
        print("로그인 사이트 패스워드 입력 ...")
        AirWebDriver.send_key_by_name("user[password]", str_login_password)
        # AirWebDriver.send_click_event_with_xpath('//*[@id="new_user"]/button')
        print("로그인 사이트 엔터키 입력 ...")
        AirWebDriver.click_keyboard('enter')
        print('로그인 후 초기화면 로딩 성공')

    except (Exception) as detail:
        print('로그인 페이지 로딩 실패')
        login_fail_id_index_list.append(index)
        AirWebDriver.quit_browser()
        print(detail)
        return False


    print('초기화면에서 비지니스데이 CSS 얻어오기 대기중..')
    # 초기화면에서 비지니스데이 데이터 CSS가 활성화 될때까지 대기한다.
    time.sleep(5)
    css_path = '.times>div:nth-child(1)>div:nth-child(1)>div:nth-child(1)>input:nth-child(2)'
    if (AirWebDriver.wait_until_show_element_css(css_path)) is not True:
        print('초기화면에서 비지니스데이 CSS 얻어오기 실패')
        login_fail_id_index_list.append(index)
        AirWebDriver.quit_browser()
        return False

    try:
        print("초기화면에서 비지니스데이 CSS 얻어오기 성공")
        print("재 구매일, 비지니스데이 잔여 일수 얻어오기 시도...")
        time.sleep(3)
        soup = AirWebDriver.get_soup_object()

        remain_business_day = int(soup.find_all(class_='counter-container')[2].get('countdown'))
        remain_repurchase_day = int(soup.find_all(class_='counter-container')[3].get('countdown'))

        remaining_business_day_dic[str_login_id] = remain_business_day
        repurchase_left_list_dic[str_login_id] = remain_repurchase_day

        print(str_login_id, " 남은 비지니스 데이 :", remain_business_day)
        print(str_login_id, " 남은 재 구매일 :", remain_repurchase_day)

        # 재구매일이 0일 경우 이체 작업을 안한다.
        if remain_repurchase_day == 0:
            print("%s 아이디 재구매일 도래 이체 중지" % str_login_id)
            # AirWebDriver.mouse_click(927, 163, 10)
            repurchase_id_list.append(str_login_id)
            AirWebDriver.quit_browser()
            return False

    except (Exception) as detail:
        #실패 경우 아이디에 -1을 기록해 놓고 추후 -1인 아이디만 재시도 한다.
        #remaining_business_day_dic[str_login_id] = -1
        #repurchase_left_list_dic[str_login_id] = -1
        #process_success_flag = -1
        login_fail_id_index_list.append(index)
        AirWebDriver.quit_browser()
        print(detail)
        return False



    print("트랜스퍼 사이트 접속 시도")
    AirWebDriver.move_to_url(str_Transfer_URL)
    print("트랜스퍼 사이트 접속 성공")

    #
    print('이체 버튼 xpath 대기중..')
    # 트랜스퍼 화면에서 이체 버튼 xapth가 활성화 될때까지 대기한다.
    time.sleep(5)
    if (AirWebDriver.wait_until_show_element_xpath('//*[@id="submit-transfer"]')) is not True:
        print('이체 버튼 로딩 실패')
        login_fail_id_index_list.append(index)
        AirWebDriver.quit_browser()
        return False

    _tmp_rewards = -1
    try:
        print('이체 버튼 로딩 성공')
        print("현재 해당 계정의 월릿 금액을 구한다.")
        # 현재 해당 계정의 커미션 금액을 구한다. (추후 커미션이 있는 계좌만 커미션 이체를 하기 위해서)
        time.sleep(3)
        soup = AirWebDriver.get_soup_object()
        _commissions = float(soup.find_all("small")[1].get_text())
        comissions_list_dic[str_login_id] = _commissions

        _rewards = float(soup.find_all("small")[3].get_text())
        #_cash = float(soup.find_all("small")[2].get_text())

        _tmp_rewards = _rewards
        print("commissions: %f" % _commissions)
        #print("cash: %f" % _cash)
        print("rewards: %f" % _rewards)

        # 만일 이체할 금액이 없다면 종료한다.
        if _rewards <= 0:
            print("이체할 리워드 잔고 없음 트랜스퍼 종료")
            # AirWebDriver.mouse_click(927, 163, 10)
            AirWebDriver.quit_browser()
            return False

    except (Exception) as detail:
        print(detail)
        # 실패 경우 아이디에 -1을 기록해 놓고 추후 -1인 아이디만 재시도 한다.
        comissions_list_dic[str_login_id] = -1
        process_success_flag = -1


    #초기 로그인후 재구매일 조회 또는 트랜스퍼창 금액 조회 실패할 경우
    #실패한 아이디의 인덱스를 저장한 후 종료
    if process_success_flag == -1:
        login_fail_id_index_list.append(index)
        AirWebDriver.quit_browser()
        return False


    # 리워드에 금액이 있다면 리워드 이체를 한다.(1)
    # //*[@id="partition_transfer_partition_user_wallet_id"]/option[3]
    if _tmp_rewards > 0 :

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
        time.sleep(5)
        if (AirWebDriver.wait_until_show_element_xpath('//*[@id="submit-transfer"]')) is True:
            #AirWebDriver.move_to_url(str_AirBitClub_Login_URL)
            # 종료
            AirWebDriver.quit_browser()
        else:
            AirWebDriver.quit_browser()


def transfer_commission_money(indedx, str_destination_id, str_login_id, str_login_password, str_credential_filename):
    global _REQUEST_TOKEN_VALUE
    global comissions_list_dic
    global remaining_business_day_dic
    global repurchase_left_list_dic
    global login_fail_id_list


    print("start commission transfer %s" % str_login_id)
    str_AirBitClub_Main = "https://www.bitbackoffice.com"
    str_AirBitClub_Home_URL = "https://www.bitbackoffice.com/#"
    str_AirBitClub_Login_URL = "https://www.bitbackoffice.com/auth/login"
    str_Transfer_URL = "https://www.bitbackoffice.com/transfers"
    str_Wallet_URL = "https://www.bitbackoffice.com/wallets"

    print("웹 드라이버 로딩 시작")
    initialize = -1
    AirWebDriver = WebDriver_Manager(browser_flag, initialize)
    if initialize == 0:
        print('리워드 이체 웹 드라이버 초기 로딩 실패')
        login_fail_id_index_list.append(index)
        AirWebDriver.quit_browser()
        return False

    try:
        print("로그인 사이트 접속 시도")
        AirWebDriver.move_to_url(str_AirBitClub_Login_URL)
        print('로그인 페이지 패스워드 입력란 xpath 대기중..')
        time.sleep(2)
        AirWebDriver.wait_until_show_element_xpath('//*[@id="user_password"]')
        print("로그인 사이트 아이디 입력 ...")
        AirWebDriver.send_key_by_name("user[username]", str_login_id)
        print("로그인 사이트 패스워드 입력 ...")
        AirWebDriver.send_key_by_name("user[password]", str_login_password)
        # AirWebDriver.send_click_event_with_xpath('//*[@id="new_user"]/button')
        print("로그인 사이트 엔터키 입력 ...")
        AirWebDriver.click_keyboard('enter')
        print('로그인 후 초기화면 로딩 성공')
    except (Exception) as detail:
        print('로그인 페이지 로딩 실패')
        login_fail_id_index_list.append(index)
        AirWebDriver.quit_browser()
        print(detail)
        return False

    print("트랜스퍼 사이트 접속 시도")
    AirWebDriver.move_to_url(str_Transfer_URL)
    print("트랜스퍼 사이트 접속 성공")

    #time.sleep(3)
    print('이체 버튼 xpath 대기중..')
    # 트랜스퍼 화면에서 이체 버튼 xapth가 활성화 될때까지 대기한다.
    time.sleep(5)
    if (AirWebDriver.wait_until_show_element_xpath('//*[@id="submit-transfer"]')) is not True:
        print('이체 버튼 로딩 실패')
        login_fail_id_index_list.append(index)
        AirWebDriver.quit_browser()

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
    commissions_money = comissions_list_dic[str_login_id]
    AirWebDriver.send_key_by_id('partition_transfer_partition_amount', str(commissions_money))

    # 토큰 요청 버튼을 누른다.
    # //*[@id="submit-token"]
    AirWebDriver.send_click_event_with_xpath('//*[@id="submit-token"]')

    # 토큰을 요청하고 메일에서 토큰을 받아온다.
    mail_scheduler.start_scheduler_interval(get_airbit_token_value, "token_job_commissions", 3,
                                                str_credential_filename)

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
    _REQUEST_TOKEN_VALUE = None  # 다음번 조회를 위해서 토큰 초기화

    # 트랜스퍼 실행
    # //*[@id="submit-transfer"]
    print("send rewards money : %f" % commissions_money)
    AirWebDriver.send_click_event_with_xpath('//*[@id="submit-transfer"]')

    # 트랜스퍼 실행 후 잠시 대기
    time.sleep(5)
    if (AirWebDriver.wait_until_show_element_xpath('//*[@id="submit-transfer"]')) is True:
        # AirWebDriver.move_to_url(str_AirBitClub_Login_URL)
        # 종료
        AirWebDriver.quit_browser()
    else:
        AirWebDriver.quit_browser()



def get_account_count():
    return len(id_list)


def report_account():
    global id_list
    global login_fail_id_index_list
    global repurchase_id_list
    global remaining_business_day_dic
    global repurchase_left_list_dic

    pdf = PDF_Manager()
    pdf.add_page()

    now = datetime.datetime.now()
    nowDate = now.strftime('%Y-%m-%d')

    # 300일 비지니스 데이 보고서 작성
    # 고객이 원하는 일수를 지정해 준다 (ex: 한달이면 30일 남겨놓고 표시)
    # remaining_business_day_dic[str_login_id] = remain_business_day
    str_remaining_business_day_list = "30일 이하 비지니스 데이 계좌 리스트\n"
    for userid, left_day in remaining_business_day_dic.items():
        if left_day <= 30:
            strtmp = userid + ": " + str(left_day) + "회 남음\n"
            str_remaining_business_day_list += strtmp

    # 75일 전산비 납부 리스트 보고서 작성
    # 고객이 원하는 일수를 지정해 준다 (ex: 7일이면 7 남겨놓고 표시)
    # repurchase_left_list_dic[str_login_id] = remain_repurchase_day
    str_repurchase_left_list = "7일 이하 전산비 납부 계좌 리스트\n"
    for userid, left_day in repurchase_left_list_dic.items():
        if left_day <= 7:
            strtmp = userid + ": " + str(left_day) + "일 남음\n"
            str_repurchase_left_list += strtmp

    #  트랜스퍼 후 메인계좌 잔고 보고서 작성
    str_main_transfer = "트랜스퍼 완료 후 메인계좌" + "(" + id_list[0] + ")" + " 잔고 현황\n"
    str_transfer_date = "트랜스퍼 날짜 : " + nowDate + "\n"
    str_total_account = "생성된 계좌의 총 갯수 : %d" % (len(id_list)) + "\n"
    str_rewards = "전체계좌 REWARDS 합계 : %.2f" % rewards.value + "$\n"
    str_commisions = "전체계좌 COMMISIONS 합계 : %.2f" % commissions.value + "$\n"
    str_cash = "전체계좌 CASH 합계 : %.2f" % cash.value  + "$\n"
    str_savings = "전체계좌 SAVINGS 합계 : %.2f" % savings.value + "$\n"
    str_total = "총 인출 가능 달러(커미션 + 리워드) : %.2f" % (commissions.value + rewards.value) + "$\n"

    str_main_transfer += str_transfer_date
    str_main_transfer += str_total_account
    str_main_transfer += str_rewards
    str_main_transfer += str_commisions
    str_main_transfer += str_cash
    str_main_transfer += str_savings
    str_main_transfer += str_total



    print(str_remaining_business_day_list)
    print(str_repurchase_left_list)
    print(str_main_transfer)

    print(login_fail_id_index_list)

    # 집계를 마치고 변수를 초기화 한다.
    commissions.value = 0
    cash.value = 0
    rewards.value = 0
    savings.value = 0
    del repurchase_id_list[:]
    del login_fail_id_index_list[:]
    remaining_business_day_dic = {}
    repurchase_left_list_dic = {}


    # 보고서 PDF  생성
    pdf.print_chapter_user('※ 300일 비지니스 데이 30일 잔여 대상 계좌 리스트 ※', str_remaining_business_day_list)
    pdf.print_chapter_user('※ 75일 전산비 납부 7일 잔여 대상 계좌 리스트 ※', str_repurchase_left_list)
    pdf.print_chapter_user('※ 트랜스퍼 완료 후 메인계좌 잔고 보고서 ※', str_main_transfer)


    rerport_filename = nowDate +  ' 계좌현황 보고서.pdf'
    pdf.output(rerport_filename, 'F')

    Telegram_Mng = Telegram_Manager()
    Telegram_Mng.send_file(rerport_filename)



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
    report_account()
    end_time = time.time()
    strmsg = "전체계좌 합산 프로세스 소요시간 : " + str(end_time - start_time)





def get_screent_shot_with_login_id(str_login_id, str_login_password):

    str_AirBitClub_Login_URL = "https://www.bitbackoffice.com/auth/login"
    str_Wallet_URL = "https://www.bitbackoffice.com/wallets"

    initialize = -1
    AirWebDriver = WebDriver_Manager(browser_flag, initialize)

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
    end_index = get_account_count()

    for index in range(0, 10):
        transfer_all_money_to_main_account(1, end_index)
        time.sleep(3)

    """
    Telegram_Mng = Telegram_Manager()
    Telegram_Mng.send_file("2018-01-05 계좌현황 보고서.pdf")
    """


    #process_browser_to_get_money_with_userid("lsw120300", "lsw8954!")

    """
    scheduler = Schedule_Manager()
    scheduler.start_scheduler_cron(transfer_all_money_to_main_account, 'mon-sat', 2, 00)
    print("start scheduler transfer")
    """

    #scheduler.start_scheduler_cron(get_total_bonus_money, 'mon-sat', 2, 0)
    #print("start scheduler get_total_bonus_money")
    























