import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from Telegram_Class import Telegram_Manager
from multiprocessing import Process, Value


str_Chrome_Path = "../Driver/chromedriver"
str_AirBitClub_Login_URL = "https://www.bitbackoffice.com/auth/login"
str_Wallet_URL = "https://www.bitbackoffice.com/wallets"


chrome_options = Options()
chrome_options.add_argument("--disable-infobars")
prefs = {'safebrowsing.enabled': 'true'}
chrome_options.add_experimental_option("prefs", prefs)


def process_browser(str_id, str_password):

    global browser
    global str_AirBitClub_Login_URL
    global str_Wallet_URL
    global chrome_options
    global str_Chrome_Path

    browser = webdriver.Chrome(executable_path=str_Chrome_Path, chrome_options=chrome_options)

    browser.implicitly_wait(2)
    browser.get(str_AirBitClub_Login_URL)
    browser.find_element_by_name("user[username]").send_keys(str_id)
    browser.find_element_by_name("user[password]").send_keys(str_password)
    browser.find_element_by_xpath('//*[@id="new_user"]/button').click()

    browser.implicitly_wait(2)
    browser.get(str_Wallet_URL)

    browser.implicitly_wait(2)

    browser.find_element_by_xpath('html/body/div[3]/div/div[2]/div/div[2]/div[3]/div[1]/a').click()


if __name__   == "__main__":

    process_browser("lsw120300", "lsw8954!")






