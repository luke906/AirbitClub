import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
#from selenium.webdriver.firefox.options import Options


class WebDriver:

    def __init__(self, driver_path):
        #display = Display(visible=1, size=(1920, 1080))
        #display.start()

        self.DriverPath = driver_path
        self.chrome_options = Options()
        self.chrome_options.add_argument("--disable-infobars")
        self.chrome_options.add_argument('--disable-extensions')
        self.chrome_options.add_argument('--ignore-certificate-errors')
        #self.chrome_options.add_argument('--profile-directory=Default')
        #self.chrome_options.add_argument("--incognito")
        #self.chrome_options.add_argument("--disable-plugins-discovery");
        #self.chrome_options.add_argument("--start-maximized")
        #self.chrome_options.add_argument("load-extension=/Users/charg/AppData/Local/Google/Chrome/User Data/Default/Extensions/fdcgdnkidjaadafnichfpabhfomcebme/6.0.5_0")
        self.browser = webdriver.Chrome(executable_path=self.DriverPath, chrome_options=self.chrome_options)

        #self.browser = webdriver.Firefox(executable_path=self.DriverPath)


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

    def save_screenshot(self, filename):
        self.browser.save_screenshot(filename)

    def close_latest_tab(self):
        driver = self.browser
        driver.switch_to.window(driver.window_handles[-1])
        driver.close()

    def quit_browser(self):
        self.browser.quit()



