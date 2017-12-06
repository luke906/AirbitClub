from WebDriver_Class import WebDriver


str_Chrome_Path = "../Selenium_Driver/chromedriver"
str_AirBitClub_Login_URL = "https://www.bitbackoffice.com/auth/login"

AirWebDriver = WebDriver(str_Chrome_Path)
AirWebDriver.move_to_url(str_AirBitClub_Login_URL)
