import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
str_Chrome_Path = "../Driver/chromedriver"

# str_NaverLogin_URL = "https://nid.naver.com/nidlogin.login"
str_AirBitClub_Login_URL = "https://www.bitbackoffice.com/auth/login"

chrome_options = Options()
chrome_options.add_argument("--disable-infobars")
browser = webdriver.Chrome(executable_path = str_Chrome_Path, chrome_options = chrome_options)
browser.implicitly_wait(3)

# driver = webdriver.Chrome(str_Chrome_Path)
# driver = webdriver.PhantomJS(str_Phantom_Path)
# driver.set_window_size(1120, 550)

browser.get(str_AirBitClub_Login_URL)
print(browser.page_source)

# browser.implicitly_wait(3)
# driver.get(str_NaverLogin_URL)
# driver.find_element_by_name('id').send_keys('luke906')
# driver.find_element_by_name('pw').send_keys('newlife8661!')

# driver.implicitly_wait(3)

browser.find_element_by_name("user[username]").send_keys('lsw120300')
browser.find_element_by_name("user[password]").send_keys('lsw8954!')
browser.find_element_by_xpath('//*[@id="new_user"]/button').click()

# Move to Wallets
Wallet_Path = "https://www.bitbackoffice.com/wallets"
browser.get(Wallet_Path)
#print(browser.page_source)


# print("Airbit Club Login Succeed!!")
# print(driver.page_source)

# client = requests.session()
# client.get("https://www.bitbackoffice.com/wallets")
# html_source = client.text
# print(html_source)

# driver.quit()
