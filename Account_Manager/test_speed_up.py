from __future__ import print_function
from incapsula import IncapSession
from bs4 import BeautifulSoup

str_AirBitClub_Login_URL = "https://www.bitbackoffice.com/auth/login"

session = IncapSession()

session.cookies.set('cookie-key', 'cookie-value')

response = session.get('http://example.com', headers={'Referer': str_AirBitClub_Login_URL})
soup = BeautifulSoup(response, "html.parser")
print(session.cookies)