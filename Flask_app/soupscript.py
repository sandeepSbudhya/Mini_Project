import requests
from bs4 import BeautifulSoup

class Examplesoup:
    def __init__(self) -> None:
        pass

    def printgooglefunc(self):
        URL = "https://www.facebook.com"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content,'lxml')
        mydivs = soup.find_all("div", {"class": "_8esn"})
        return str(mydivs)
