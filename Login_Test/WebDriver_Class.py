import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class WebDriver:

    def __init__(self, driver_path):
        self.DriverPath = driver_path
        self.chrome_options = Options()
        self.chrome_options.add_argument("--disable-infobars")
        self.browser = webdriver.Chrome(executable_path=self.DriverPath, chrome_options=self.chrome_options)
        self.browser.implicitly_wait(3)

    def move_to_url(self, destination_url):
        self.browser.get(destination_url)

    def send_key_by_name(self, name_key, send_value):
        self.browser.find_element_by_name(name_key).send_keys(send_value)

    def send_key_by_id(self, name_key, send_value):
        self.browser.find_element_by_id(name_key).send_keys(send_value)

    def send_click_event(self, strxpath):
        self.browser.find_element_by_xpath(strxpath).click()

    def return_browser(self):
        return self.browser

    def get_html_source(self):
        return self.browser.page_source

    def execute_javascript(self, strcommand):
        self.browser.execute_script(strcommand)

    def quit(self):
        self.browser.quit()



