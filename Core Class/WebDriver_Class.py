
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
#from browsermobproxy import Server
#from fake_useragent import UserAgent

class WebDriver:

    def __init__(self, driver_path):
        """
        server = Server("../browsermob-proxy/bin/browsermob-proxy")
        server.start()
        proxy = server.create_proxy()
        proxy.selenium_proxy()
        capabilities = DesiredCapabilities.CHROME
        proxy.add_to_capabilities(capabilities)
        """
        #ua = UserAgent()
        #capabilities = webdriver.DesiredCapabilities.CHROME
        #capabilities["chrome.switches"] = ["--user-agent=" + ua.chrome]

        self.DriverPath = driver_path
        self.chrome_options = Options()
        #self.chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy))
        self.chrome_options.add_argument("--start-maximized")
        self.chrome_options.add_argument("--disable-infobars")
        self.browser = webdriver.Chrome(executable_path=self.DriverPath, chrome_options=self.chrome_options)


    def move_to_url(self, destination_url):

        try:
            self.browser.implicitly_wait(3)
            self.browser.get(destination_url)
        except Exception:
            self.browser.quit()


    def send_key_by_name(self, name_key, send_value):
        self.browser.find_element_by_name(name_key).send_keys(send_value)

    def send_key_by_id(self, name_key, send_value):
        self.browser.find_element_by_id(name_key).send_keys(send_value)

    def send_click_event_with_xpath(self, strxpath):
        self.browser.find_element_by_xpath(strxpath).click()

    def get_object_by_xpath(self, strxpath):
        return Select(self.browser.find_element_by_xpath(strxpath))

    def select_option_by_id_text(self, id, text):
        el = self.browser.find_element_by_id(id)
        for option in el.find_elements_by_tag_name('option'):
            if text == "commissions":
                #print(option.text[0:11])
                if option.text[0:11] == text:
                    option.click()  # select() in earlier versions of webdriver
                    break
            elif text == "rewards":
                #print(option.text[0:7])
                if option.text[0:7] == text:
                    option.click()  # select() in earlier versions of webdriver
                    break

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
        try:
            self.browser.quit()
        except Exception:
            pass


