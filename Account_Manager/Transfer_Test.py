
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
password_list = []
email_list = []
gmail_secret_json = []
gmail_secret_json_to_clear = []
email_kind = []
user_telegram_id_list=[]
user_name_list=[]

repurchase_id_list = []

#트랜스퍼 속도 개선을 위해서 커미션리스트를 만든다.
comissions_list_dic = {}

#보고서 제출용
remaining_business_day_dic = {}
repurchase_left_list_dic = {}

# 리워드 진행중 실패한 아이디 목록
reward_fail_id_index_list = []

# 커미션 진행중 실패한 아이디 목록
commission_fail_id_index_list = []

# 프로세스를 이용하여 다중 로그인을 할 경우 사용할 메모리 변수
# shared memory 사용 (멀티 프로세스간 변수값 공유)
commissions = Value('d', 0.0)
cash = Value('d', 0.0)
rewards = Value('d', 0.0)
savings = Value('d', 0.0)

# 트랜스퍼한 금액을 집계하기 위한 변수
transfer_rewards_total = Value('d', 0.0)
transfer_commissions_total = Value('d', 0.0)

transfer_rewards_total.value = 0
transfer_commissions_total.value = 0


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
    global user_telegram_id_list
    global user_name_list
    global gmail_secret_json_to_clear

    # 가비아 DB 접속
    DB = DB_Manager()

    # 사용자 로그인 정보를 가지고 온다.
    sql = "select * from USER_LOGIN_INFO where user_name = " + "'" + person_name + "'" + "order by user_id_index ASC"
    results = DB.get_object_execute_sql(sql)

    # SELECT한 로그인 정보를 리스트에 저장한다.
    for index in range(0, len(results)):
        id_list.append(results[index]['user_id'])
        password_list.append(results[index]['user_password'])
        email_list.append(results[index]['user_email'])
        gmail_secret_json.append(results[index]['user_gmail_secret_json'])
        email_kind.append(results[index]['user_email_kind'])
        user_telegram_id_list.append(results[index]['user_telegram_id'])
        user_name_list.append(results[index]['user_name'])

    sql = "select distinct user_gmail_secret_json from USER_LOGIN_INFO where user_name = " + "'" + person_name + "'"
    results = DB.get_object_execute_sql(sql)
    for index in range(0, len(results)):
        gmail_secret_json_to_clear.append(results[index]['user_gmail_secret_json'])

    DB.close_db()

    print(results[0])



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

    # 트랜스퍼 하기전에 메일을 청소 한다.
    try:
        for json_list in gmail_secret_json_to_clear:
            clear_mail_box_before_transfer(json_list)
    except (Exception) as detail:
        print(detail)
        print("메일인증 실패 다시 시도")
        transfer_all_money_to_main_account(start_index, end_index)

    # 메인 계좌 다음 계좌부터 리워드만 트랜스퍼 샐행.
    for index in range(start_index, end_index):
        print("트랜스퍼 인덱스 : %d" % index)
        result = transfer_reward_commission_money(id_list[index], gmail_secret_json[0])



def transfer_reward_commission_money(str_destination_id, str_credential_filename):

    global _REQUEST_TOKEN_VALUE, _rewards
    global comissions_list_dic
    global remaining_business_day_dic
    global repurchase_left_list_dic
    global reward_fail_id_index_list

    _rewards = -1
    _commissions = -1

    str_AirBitClub_Login_URL = "https://www.bitbackoffice.com/auth/login"
    str_Transfer_URL = "https://www.bitbackoffice.com/transfers"

    print("웹 드라이버 로딩 시작")
    initialize = -1
    AirWebDriver = WebDriver_Manager(browser_flag, initialize)
    if initialize == 0:
        print('웹 드라이버 초기 로딩 실패')
        AirWebDriver.quit_browser()
        print('처음부터 재 시도')
        transfer_reward_commission_money(str_destination_id, str_credential_filename)

    print("웹 드라이버 로딩 성공")
    AirWebDriver.mouse_click(1005, 101, 2)
    AirWebDriver.mouse_click(1005, 101, 2)

    try:
        print("로그인 사이트 접속 시도")
        AirWebDriver.move_to_url(str_AirBitClub_Login_URL)
        print('로그인 페이지 패스워드 입력란 css 대기중..')
        if (AirWebDriver.wait_until_show_element_css('#user_username')) is False:
            reward_fail_id_index_list.append(index)
            AirWebDriver.quit_browser()
            print('처음부터 재 시도')
            transfer_reward_commission_money(str_destination_id, str_credential_filename)

        time.sleep(2)
        AirWebDriver.wait_until_show_element_css('#user_username')
        print("로그인 사이트 아이디 입력 ...")
        AirWebDriver.send_key_by_name("user[username]", "lsw120300")
        print("로그인 사이트 패스워드 입력 ...")
        AirWebDriver.send_key_by_name("user[password]", "lsw8954!")

        AirWebDriver.send_click_event_with_xpath('//*[@id="new_user"]/button')
        print("로그인 사이트 엔터키 입력 ...")
        # AirWebDriver.click_keyboard('enter')
        print('로그인 후 초기화면 로딩 성공')

    except (Exception) as detail:
        print('로그인 페이지 로딩 실패')
        AirWebDriver.quit_browser()
        print('처음부터 재 시도')
        transfer_reward_commission_money(str_destination_id, str_credential_filename)
        print(detail)

    try:
        print("트랜스퍼 사이트 접속 시도")
        time.sleep(9000)
        AirWebDriver.move_to_url(str_Transfer_URL)
        print("트랜스퍼 사이트 접속 성공")
        #time.sleep(5)

        print('트랜스퍼 사이트 리딩을 위한 css 대기중..')
        if (AirWebDriver.wait_until_show_element_css('div.row:nth-child(2)>div:nth-child(2)>div:nth-child(1)>div:nth-child(1)>small:nth-child(4)')) is False:
            login_fail_id_index_list.append(index)
            AirWebDriver.quit_browser()
            print('처음부터 재 시도')
            transfer_reward_commission_money(str_destination_id, str_credential_filename)
        print('트랜스퍼 사이트 리딩을 위한 css 대기 성공')



    except (Exception) as detail:
        AirWebDriver.quit_browser()
        print(detail)
        print('처음부터 재 시도')
        transfer_reward_commission_money(str_destination_id, str_credential_filename)


    # 리워드에 금액이 있다면 리워드 이체를 한다.
    _rewards = 2
    _commissions = 2
    if _rewards > 0 :

        # 트랜스퍼할 아이디를 입력한다.
        AirWebDriver.send_key_by_id("search-user", str_destination_id)

        # 검색버튼을 누른다.
        AirWebDriver.send_click_event_with_xpath('//*[@id="search-btn"]')
        time.sleep(4)
        print('수신자 조회창 대기중..')
        AirWebDriver.wait_until_show_element_id('transfer-to')
        print('수신자 조회창 성공..')

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
        mail_scheduler = Schedule_Manager()
        mail_scheduler.start_scheduler_interval(get_airbit_token_value, "token_job_rewards", 10, str_credential_filename)

        # 이메일 확인 후 토큰을 얻어 올때 까지 대기
        while 1:
            if _REQUEST_TOKEN_VALUE is not None and len(_REQUEST_TOKEN_VALUE) is 32:
                #mail_scheduler.kill_scheduler("token_job_rewards")
                mail_scheduler.shutdown()
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
        time.sleep(10)
        if _commissions <= 0:
            #AirWebDriver.mouse_click(984, 162, 3)
            #time.sleep(10)
            #AirWebDriver.move_to_url("https://www.bitbackoffice.com/#")
            AirWebDriver.quit_browser()
            return True


    # 커미션에 금액이 있다면 리워드 이체를 한다.
    if _commissions > 0:

        transfer_commissions_total.value += _commissions

        # 트랜스퍼할 아이디를 입력한다.
        AirWebDriver.send_key_by_id("search-user", str_destination_id)

        # 검색버튼을 누른다.
        AirWebDriver.send_click_event_with_xpath('//*[@id="search-btn"]')
        time.sleep(4)
        print('수신자 조회창 대기중..')
        AirWebDriver.wait_until_show_element_id('transfer-to')
        print('수신자 조회창 성공..')

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
        mail_scheduler = Schedule_Manager()
        mail_scheduler.start_scheduler_interval(get_airbit_token_value, "token_job_commissions", 10,
                                                str_credential_filename)

        # 이메일 확인 후 토큰을 얻어 올때 까지 대기
        while 1:
            if _REQUEST_TOKEN_VALUE is not None and len(_REQUEST_TOKEN_VALUE) is 32:
                #mail_scheduler.kill_scheduler("token_job_commissions")
                mail_scheduler.shutdown()
                print("Request Token for commissions is : %s" % _REQUEST_TOKEN_VALUE)
                print("get_airbit_token_value JOB STOP!")
                break

        # 토큰 입력
        # id = partition_transfer_partition_token
        AirWebDriver.send_key_by_id('partition_transfer_partition_token', str(_REQUEST_TOKEN_VALUE))
        _REQUEST_TOKEN_VALUE = None  # 다음번 조회를 위해서 토큰 초기화

        # 트랜스퍼 실행
        # //*[@id="submit-transfer"]
        print("send commissions money : %f" % _commissions)
        AirWebDriver.send_click_event_with_xpath('//*[@id="submit-transfer"]')

    # 트랜스퍼 실행 후 잠시 대기
    #AirWebDriver.mouse_click(984, 162, 3)
    time.sleep(10)
    #AirWebDriver.move_to_url("https://www.bitbackoffice.com/#")
    AirWebDriver.quit_browser()
    return True


def get_account_count():
    return len(id_list)


def report_account():
    global id_list
    global login_fail_id_index_list
    global repurchase_id_list
    global remaining_business_day_dic
    global repurchase_left_list_dic
    global user_telegram_id_list

    pdf = PDF_Manager()
    pdf.add_page()

    now = datetime.datetime.now()
    nowDate = now.strftime('%Y-%m-%d')

    # 300일 비지니스 데이 보고서 작성
    # 고객이 원하는 일수를 지정해 준다 (ex: 한달이면 30일 남겨놓고 표시)
    # remaining_business_day_dic[str_login_id] = remain_business_day
    str_remaining_business_day_list = "300회 리워드 보너스중 30회 남은 계좌 리스트\n"
    for userid, left_day in remaining_business_day_dic.items():
        if left_day <= 30:
            strtmp = userid + ": " + str(left_day) + "회 남음\n"
            str_remaining_business_day_list += strtmp

    # 75일 전산비 납부 리스트 보고서 작성
    # 고객이 원하는 일수를 지정해 준다 (ex: 7일이면 7 남겨놓고 표시)
    # repurchase_left_list_dic[str_login_id] = remain_repurchase_day
    str_repurchase_left_list = "75일 마다 전산비 납부하는 계좌중 7일 남은 계좌 리스트\n"
    for userid, left_day in repurchase_left_list_dic.items():
        if left_day <= 7:
            strtmp = userid + ": " + str(left_day) + "일 남음\n"
            str_repurchase_left_list += strtmp

    #  트랜스퍼 후 메인계좌 잔고 보고서 작성
    str_report = ""
    str_transfer_date = "트랜스퍼 날짜 : " + nowDate + "\n"
    str_today_rewards = "금일 트랜스퍼 REWARDS 총금액 : %.2f" % transfer_rewards_total.value + "$\n"
    str_today_commisions = "금일 트랜스퍼 COMMISIONS 총금액 : %.2f" % transfer_commissions_total.value + "$\n\n"

    str_total_account = "현재 계좌의 총 갯수 : %d" % (len(id_list)) + "개" + "\n"
    str_main_transfer = "트랜스퍼 완료 후 현재 메인계좌" + "(" + id_list[0] + ")" + " 잔고 현황\n"

    str_rewards = "메인계좌 REWARDS : %.2f" % rewards.value + "$\n"
    str_commisions = "메인계좌 COMMISIONS : %.2f" % commissions.value + "$\n"
    str_cash = "메인계좌 CASH : %.2f" % cash.value  + "$\n"
    str_savings = "메인계좌 SAVINGS : %.2f" % savings.value + "$\n"
    str_total = "메인계좌 인출 가능 달러(커미션 + 리워드) : %.2f" % (commissions.value + rewards.value) + "$\n"

    str_report += str_transfer_date
    str_report += str_today_rewards
    str_report += str_today_commisions

    str_report += str_total_account
    str_report += str_main_transfer

    str_report += str_rewards
    str_report += str_commisions
    str_report += str_cash
    str_report += str_savings
    str_report += str_total

    print(str_remaining_business_day_list)
    print(str_repurchase_left_list)
    print(str_report)



    # 보고서 PDF  생성
    if len(str_remaining_business_day_list) <= 0:
        pdf.print_chapter_user('※ 300일 리워드 지급일 : 30일 전 계좌 리스트 ※', "없음")
    else:
        pdf.print_chapter_user('※ 300일 리워드 지급일 : 30일 전 계좌 리스트 ※', str_remaining_business_day_list)

    if len(str_repurchase_left_list) <= 0:
        pdf.print_chapter_user('※ 75일 도래 전산비 납부 : 7일 전 계좌 리스트 ※', "없음")
    else:
        pdf.print_chapter_user('※ 75일 도래 전산비 납부 : 7일 전 계좌 리스트 ※', str_repurchase_left_list)

    pdf.print_chapter_user('※ 트랜스퍼 완료 후 메인계좌 잔고 보고서 ※', str_report)

    rerport_filename = nowDate +  " " + user_name_list[0] +' 계좌현황 보고서.pdf'

    pdf.output(rerport_filename, 'F')

    Telegram_Mng = Telegram_Manager(user_telegram_id_list[0])
    Telegram_Mng.send_file(rerport_filename)

    # 집계를 마치고 변수를 초기화 한다.
    commissions.value = 0
    cash.value = 0
    rewards.value = 0
    savings.value = 0
    transfer_rewards_total.value = 0
    transfer_commissions_total.value = 0

    del repurchase_id_list[:]
    del reward_fail_id_index_list[:]
    del commission_fail_id_index_list[:]
    remaining_business_day_dic = {}
    repurchase_left_list_dic = {}

    del id_list[:]
    del password_list[:]
    del email_list[:]
    del gmail_secret_json[:]
    del gmail_secret_json_to_clear[:]
    del email_kind[:]
    del user_telegram_id_list[:]
    del user_name_list[:]


if __name__ == "__main__":

    get_id_password('이성원')
    end_index = get_account_count()
    transfer_all_money_to_main_account(1, 30)























