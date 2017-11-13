import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

class WebDriver:

    def __init__(self, driver_path):
        self.DriverPath = driver_path
        self.chrome_options = Options()
        self.chrome_options.add_argument("--disable-infobars")
        self.browser = webdriver.Chrome(executable_path=self.DriverPath, chrome_options=self.chrome_options)


    def move_to_url(self, destination_url):
        self.browser.implicitly_wait(3)
        self.browser.get(destination_url)

    def send_key_by_name(self, name_key, send_value):
        self.browser.find_element_by_name(name_key).send_keys(send_value)

    def send_key_by_id(self, name_key, send_value):
        self.browser.find_element_by_id(name_key).send_keys(send_value)

    def send_click_event_with_xpath(self, strxpath):
        self.browser.find_element_by_xpath(strxpath).click()

    def get_object_by_xpath(self, strxpath):
        return Select(self.browser.find_element_by_xpath(strxpath))

    def select_option_by_index(self, select, index):
        select.select_by_index(index)

    def return_browser(self):
        return self.browser

    def get_html_source(self):
        return self.browser.page_source

    def get_soup_object(self):
        return BeautifulSoup(self.browser.page_source, 'html.parser')

    def execute_javascript(self, strcommand):
        self.browser.execute_script(strcommand)

    def quit_browser(self):
        self.browser.quit()



