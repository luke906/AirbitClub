import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
str_Chrome_Path = "../Driver/chromedriver"

# str_NaverLogin_URL = "https://nid.naver.com/nidlogin.login"
# str_AirBitClub_Login_URL = "https://www.bitbackoffice.com/auth/login"
str_AirBitClub_Login_URL = "https://www.naver.com"

chrome_options = Options()

chrome_options.add_argument('headless')
chrome_options.add_argument('window-size=1920x1080')
chrome_options.add_argument("disable-gpu")
# chrome_options.add_argument("--disable-infobars")

browser = webdriver.Chrome(executable_path = str_Chrome_Path, chrome_options = chrome_options)

browser.get(str_AirBitClub_Login_URL)
browser.implicitly_wait(3)
print(browser.page_source)



browser.find_element_by_name("user[username]").send_keys('lsw120300')
browser.find_element_by_name("user[password]").send_keys('lsw8954!')
browser.find_element_by_xpath('//*[@id="new_user"]/button').click()

# Move to Wallets
Wallet_Path = "https://www.bitbackoffice.com/wallets"
browser.get(Wallet_Path)
browser.implicitly_wait(3)
print(browser.page_source)


# print("Airbit Club Login Succeed!!")
# print(driver.page_source)

# client = requests.session()
# client.get("https://www.bitbackoffice.com/wallets")
# html_source = client.text
# print(html_source)

# driver.quit()
