import requests
from bs4 import BeautifulSoup

class Examplesoup:
    def __init__(self) -> None:
        pass

    def printgooglefunc(self):
        URL = "https://www.google.com"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content,'lxml')
        return str(soup)
