
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
import os
from os.path import expanduser
import pyautogui
import glob
import subprocess
import sys
import shutil
import time

from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent

class WebDriver_Manager:

    #browser_flag = chrome, firefox
    def __init__(self, browser_flag, initialize):
        user_name = os.getlogin()

        if browser_flag == 'chrome':
            user_name = os.getlogin()
            chrome_user_path_name = "user-data-dir=C:/Users/" + user_name + "/AppData/Local/Google/Chrome/User Data"
            #user_path_name = "user-data-dir=C:/Users/" + user_name + "/PycharmProjects/AirbitClub/User_Profile/GPUCache"

            #user_path_name = "../User_Profile"

            #ua = UserAgent()
            #capabilities = webdriver.DesiredCapabilities.CHROME
            #capabilities["chrome.switches"] = ["--user-agent=" + ua.chrome]

            self.DriverPath = "../Web Driver/chromedriver"
            self.chrome_options = Options()
            #canary_path = "C:/Users/lattepanda/AppData/Local/Google/Chrome SxS/Application/chrome.exe"
            #self.chrome_options.binary_location = canary_path
            #self.chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy))
            #self.chrome_options.add_argument("--start-maximized")
            #self.chrome_options.add_argument('--incognito') #시크릿모드
            prefs = {"profile.managed_default_content_settings.images": 2}
            self.chrome_options.add_experimental_option("prefs", prefs)
            self.chrome_options.add_experimental_option('prefs', {'credentials_enable_service': False})
            self.chrome_options.add_argument("--disable-infobars")
            self.chrome_options.add_argument(chrome_user_path_name)
            self.browser = webdriver.Chrome(executable_path=self.DriverPath, chrome_options=self.chrome_options)

        elif browser_flag == 'firefox':

            #firefox_capabilities = DesiredCapabilities.FIREFOX
            #firefox_capabilities['marionette'] = True

            try:
                FF_PRF_DIR_DEFAULT = ""

                if sys.platform in ['linux', 'linux2']:
                    cmd = "ls -d /home/$USER/.mozilla/firefox/*.default/"
                    p = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE)
                    FF_PRF_DIR = p.communicate()[0][0:-2]
                    FF_PRF_DIR_DEFAULT = str(FF_PRF_DIR, 'utf-8')
                elif sys.platform == 'win32':
                    user_name = os.getlogin()
                    APPDATA = os.getenv('APPDATA')
                    FF_PRF_DIR = "C:/Users/" + user_name + "/AppData/Local/Mozilla/Firefox/Profiles/"
                    PATTERN = FF_PRF_DIR + "*default*"
                    FF_PRF_DIR_DEFAULT = glob.glob(PATTERN)[0]

                firefox_user_path_name = FF_PRF_DIR_DEFAULT # "C:/Users/USER/AppData/Local/Mozilla/Firefox/Profiles/z213e3t9.default-1514972796227"
                profile = webdriver.FirefoxProfile(firefox_user_path_name)
                profile.set_preference("permissions.default.image", 2)
                profile.set_preference("http.response.timeout", 10)
                profile.set_preference("dom.max_script_run_time", 10)
                geckoPath = '../Web Driver/geckodriver.exe'
                caps = DesiredCapabilities.FIREFOX
                caps["wires"] = True

                self.browser = webdriver.Firefox(firefox_profile = profile, executable_path = geckoPath, capabilities=caps)
                #self.browser = webdriver.Firefox(executable_path=geckoPath)
                initialize = 1
            except (Exception) as detail:
                print(detail)
                print("웹 드라이버 생성 실패")
                initialize = 0


    def move_to_url(self, destination_url):

        try:
            self.browser.implicitly_wait(2)
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

    def switch_to_main_window(self):
        driver = self.browser
        main_window_handle = None
        while not main_window_handle:
            main_window_handle = driver.current_window_handle

    def wait_until_show_element_id_text(self, id_name, text_value):
        try:
            element_present = EC.text_to_be_present_in_element((By.ID, id_name), text_value)
            WebDriverWait(self.browser, 240).until(element_present)
            print("%s text 로딩 성공"%text_value)
            return True
        except TimeoutException:
            print("id text 로딩 시간초과")
            return False

    def wait_until_show_element_id(self, id_name):
        try:
            element_present = EC.presence_of_element_located((By.ID, id_name))
            WebDriverWait(self.browser, 240).until(element_present)
            print("%s id 로딩 성공"%id_name)
            return True
        except TimeoutException:
            print("id 로딩 시간초과")
            return False

    def wait_until_show_element_xpath(self, xpath):
        try:
            element_present = EC.presence_of_element_located((By.XPATH, xpath))
            WebDriverWait(self.browser, 240).until(element_present)
            print("%s xpath 로딩 성공"%xpath)
            return True
        except TimeoutException:
            print("xpath 로딩 시간초과")
            return False

    def wait_until_show_element_class(self, class_id):
        try:
            element_present = EC.presence_of_element_located((By.XPATH, class_id))
            WebDriverWait(self.browser, 240).until(element_present)
            print("%s class 로딩 성공"%class_id)
            return True
        except TimeoutException:
            print("class 로딩 시간초과")
            return False

    def wait_until_show_element_css(self, css):
        try:
            element_present = EC.presence_of_element_located((By.CSS_SELECTOR, css))
            WebDriverWait(self.browser, 240).until(element_present)
            print("%s css 로딩 성공"%css)
            return True
        except TimeoutException:
            print("css 로딩 시간초과")
            return False

    def refresh_page(self):
        self.browser.refresh()

    def mouse_click(self, xpos, ypos, delay=0):
        screenWidth, screenHeight = pyautogui.size()
        currentMouseX, currentMouseY = pyautogui.position()
        pyautogui.PAUSE = delay
        pyautogui.moveTo(xpos, ypos)
        pyautogui.click()

    def click_keyboard(self, keyvalue):
        pyautogui.press(keyvalue)

    def image_button_click(self, image_name):
        button7location = pyautogui.locateOnScreen(image_name)# returns (left, top, width, height) of matching region
        buttonx, buttony = pyautogui.center(button7location)
        pyautogui.click(buttonx, buttony)  # clicks the center of where the button was found

    def delete_firefox_temp_addon_file(self):
        import glob
        import os
        user_name = os.getlogin()
        filepath = "C:/Users/" + user_name + "/AppData/Local/Temp/tmpaddon*"
        filelist = glob.glob(filepath)
        for file in filelist:
            #print(file)
            os.remove(file)
        #for folder in os.listdir("C:/Users/" + user_name + "/AppData/Local/Temp"):
         #   if folder.find(0,3) == 'tmp':
          #      shutil.rmtree(folder)


    def quit_browser(self, flag=-1):
        try:
            self.browser.stop_client()
            if flag ==0:
                self.browser.close()
            elif flag == -1:
                self.browser.quit()
            self.delete_firefox_temp_addon_file()
        except Exception:
            pass



