
from WebDriver_Class import WebDriver_Manager

if __name__ == "__main__":

    str_AirBitClub_Login_URL = "https://www.bitbackoffice.com/auth/login"
    AirWebDriver = WebDriver_Manager()
    AirWebDriver.move_to_url(str_AirBitClub_Login_URL)

