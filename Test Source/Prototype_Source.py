from multiprocessing import Process

from WebDriver_Class import WebDriver_Manager

import time
def process_browser_login():

    str_AirBitClub_Login_URL = "https://www.bitbackoffice.com/auth/login"

    AirWebDriver = WebDriver_Manager()
    AirWebDriver.move_to_url((str_AirBitClub_Login_URL))
    AirWebDriver.send_key_by_name("user[username]", "lsw120300")
    AirWebDriver.send_key_by_name("user[password]", "lsw8954!")
    AirWebDriver.mouse_click(258, 525, 3)

    AirWebDriver.mouse_click(927, 163, 5)

def get_total_bonus_money():

    procs = []

    # 로그인 할수 있는 사이트를 동시에 10개 로딩
    for index in range(0, 10):
        #process_browser_login()
        proc = Process(target=process_browser_login)
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()


if __name__ == "__main__":

    #get_total_bonus_money()
    process_browser_login()
    time.sleep(500)






