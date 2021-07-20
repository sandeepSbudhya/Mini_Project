import requests
from pprint import pprint
from urllib.parse import urljoin
import re
from multiprocessing import Process
from bs4 import BeautifulSoup as bs
import datetime
        
class Spider:

    def __init__(self) -> None:
        pass

    def request(self,url):
        try:
            return  requests.get("https://" + url)
        except requests.exceptions.ConnectionError:
            pass

    def find_all_subdomains(self,url):
        ct = datetime.datetime.now()
        ts = ct.timestamp()
        ts+=ct
        count=0
        #sudbomain finder
        try:
            with open("./subdomains-wordlist.txt", "r") as wordlist_file:
                for line in wordlist_file:
                    word = line.strip()
                    test_url = word + "." + url
                    response = self.request(test_url)
                    if response:
                        print(test_url)
                        urlstring = "http://"+test_url
                        with open("./subdomainscans/subdomains"+ts,"a") as subdomain_file:
                            subdomain_file.write(urlstring+"\n")
                            subdomain_file.close()
                        count+=1
                    if count>50:
                        break
                wordlist_file.close()
        except requests.exceptions.InvalidURL:
            pass
        return ts

    def spider(self,url,):
        soup = bs(self.request(url).content, "lxml")
        links = []
        for link in soup.findAll('a'):
            links.append(link.get('href'))
        print(links)
        return links

    def executepipeline(self,target_url,scan_settings):
        line_pointer=0
        p1=Process(target=self.find_all_subdomains,args=(target_url,))
        p1.start()
        p1.join()
        return 0

        
        