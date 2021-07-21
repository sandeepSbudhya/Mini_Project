import requests
from pprint import pprint
from urllib.parse import urljoin
import re
from multiprocessing import Process
from bs4 import BeautifulSoup as bs
import datetime
        
class Spider:
    subdomainfilename=""
    linksfilename=""
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
        timestring=str(ts)+str(ct)
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
                        with open("./subdomainscans/subdomains"+timestring,"a") as subdomain_file:
                            subdomain_file.write(urlstring+"\n")
                            subdomain_file.close()
                        count+=1
                    if count>4:
                        break
                wordlist_file.close()
        except requests.exceptions.InvalidURL:
            pass
        return timestring

    def spider(self,url,):
        print(url)
        reqs = requests.get(url)
        soup = bs(reqs.text, 'html.parser')
        count=0
        links = []
        for link in soup.find_all('a'):
            # print(link.get('href'))
            if count>20:
                break
            count+=1
            links.append(link.get('href'))
        return links
    def executepipeline(self,target_url,scan_settings):
        allsubdomainstimestring=self.find_all_subdomains(target_url)
        self.subdomainfilename="subdomains"+allsubdomainstimestring
        with open("./subdomainscans/subdomains"+allsubdomainstimestring,"r") as url_list:
            ct = datetime.datetime.now()
            ts = ct.timestamp()
            timestring=str(ts)+str(ct)
            for line in url_list:
                links=self.spider(line.strip())
                with open("./linkscans/links"+timestring,"a") as linkfile:
                    self.linksfilename="links"+timestring
                    for link in links:
                        linkfile.write(link+"\n")
                    linkfile.close()
            url_list.close()
        return 0

        
        