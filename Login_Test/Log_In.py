
import WebDriver_Class
from bs4 import BeautifulSoup

str_Chrome_Path = "C:/Users/charg/Selenium_Driver/chromedriver_win32/chromedriver"

str_AirBitClub_Login_URL = "https://www.bitbackoffice.com/auth/login"
Wallet_Path = "https://www.bitbackoffice.com/wallets"

"""
Browser_Class = []
for index in range(1,5):
    class_name = "Browser" + str(index)
    print(class_name)
    class_name = WebDriver_Class.WebDriver(str_Chrome_Path)
    Browser_Class[].append(class_name)
    class_name.move_to_url(str_AirBitClub_Login_URL)
"""




Browser1 = WebDriver_Class.WebDriver(str_Chrome_Path)
Browser1.move_to_url(str_AirBitClub_Login_URL)

Browser1.send_key_by_name("user[username]", "lsw120300")
Browser1.send_key_by_name("user[password]", "lsw8954!")
Browser1.send_click_event('//*[@id="new_user"]/button')
Browser1.move_to_url(Wallet_Path)


"""
wallet_html_source = Browser1.get_html_source()
soup = BeautifulSoup(wallet_html_source, 'html.parser')
print(soup.find_all('p', {'class':'result btc-container'}))
"""