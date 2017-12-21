"""
from WebDriver_Class import WebDriver_Manager

if __name__ == "__main__":

    str_AirBitClub_Login_URL = "http://www.bitbackoffice.com"
    AirWebDriver = WebDriver_Manager()
    AirWebDriver.move_to_url(str_AirBitClub_Login_URL)
"""

from twill import get_browser
b = get_browser()

from twill.commands import *
go("http://www.python.org/")
b.showforms()
