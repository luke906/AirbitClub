import requests
from bs4 import BeautifulSoup

strURL = "https://www.acmicpc.net/ranklist"

req = requests.get(strURL)
html = req.text

soup = BeautifulSoup(html, 'html.parser')

table = soup.find(id='ranklist')

trs = table.tbody.find_all('tr')

for tr in trs[:10]:
        tds = tr.find_all('td')
        rank      = tds[0].string
        user_id = tds[1].string
        print(rank, user_id)

