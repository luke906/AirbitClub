import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

str_Chrome_Path = "../Driver/chromedriver"
str_AirBitClub_Login_URL = "https://www.bitbackoffice.com/auth/login"

id_list = []
password_list = []

with open('ID_List.txt', 'r') as f:
    for read_line in f:
        id_list.append(read_line.split('/')[0])
        password_list.append(read_line.split('/')[1][:-1])

chrome_options = Options()
chrome_options.add_argument("--disable-infobars")
browser = webdriver.Chrome(executable_path = str_Chrome_Path, chrome_options = chrome_options)
browser.implicitly_wait(1)
browser.get(str_AirBitClub_Login_URL)
# print(browser.page_source)

browser.find_element_by_name("user[username]").send_keys('lsw120300')
browser.find_element_by_name("user[password]").send_keys('lsw8954!')
browser.find_element_by_xpath('//*[@id="new_user"]/button').click()

# Move to Wallets
Wallet_Path = "https://www.bitbackoffice.com/wallets"
browser.get(Wallet_Path)

html = browser.page_source
soup = BeautifulSoup(html, 'html.parser')

# for money in soup.find_all(class_='dll-quantity dll-container'):
#    print(money.get_text())

commissions = float(soup.find_all(class_='dll-quantity dll-container')[0].get_text())
cash = float(soup.find_all(class_='dll-quantity dll-container')[1].get_text())
rewards = float(soup.find_all(class_='dll-quantity dll-container')[2].get_text())
savings = float(soup.find_all(class_='dll-quantity dll-container')[3].get_text())

print(commissions)
print(cash)
print(rewards)
print(savings)


#print(browser.page_source)


# print("Airbit Club Login Succeed!!")
# print(driver.page_source)

# client = requests.session()
# client.get("https://www.bitbackoffice.com/wallets")
# html_source = client.text
# print(html_source)

# driver.quit()
