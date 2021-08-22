import requests
from pprint import pprint
from urllib.parse import urljoin
import re
from multiprocessing import Process
from bs4 import BeautifulSoup as bs
import datetime

#spider module 
class Spider:
    subdomainfilename="" 
    linksfilename=""                    
    def __init__(self) -> None:
        pass

    # function to send a get request using the requests library and return the page if it exists
    def request(self,prefix,url,):
        try:
            return  requests.get(prefix+ url)
        except requests.exceptions.ConnectionError:
            pass

    # function to find all subdomains using a word list
    def find_all_subdomains(self,url):
        ct = datetime.datetime.now()
        ts = ct.timestamp()
        timestring=str(ts)+str(ct)
        count=0
        prefix='http://'
        count1=0
        #sudbomain finder
        with open("./subdomains-wordlist.txt", "r") as wordlist_file:
            for line in wordlist_file:
                if count>4:
                    break
                if count==0 and count1>9:
                    print("limit reached")
                    with open("./subdomainscans/subdomains"+timestring,"a") as subdomain_file:
                        subdomain_file.write(prefix+url+"\n")
                        subdomain_file.close()
                    break
                count1+=1
                print(count1)
                word = line.strip()
                test_url = word + "." + url
                try:    
                    response = self.request(prefix,test_url)
                    if not response:
                        prefix='https://'
                        response = self.request(prefix,test_url)
                    if response:
                        print(test_url)
                        with open("./subdomainscans/subdomains"+timestring,"a") as subdomain_file:
                            subdomain_file.write(prefix+test_url+"\n")
                            subdomain_file.close()
                        count+=1
                    prefix='http://'
                except requests.exceptions.InvalidURL:
                    count+=1
                    pass
            wordlist_file.close()
        return timestring

    # spider function crawls the given subdomain and find all links return list of all links
    def spider(self,url,):
        
        print(url)
        reqs = requests.get(url)                               
        soup = bs(reqs.text, 'html.parser')
        print("HTML of subdomain")
        print(soup.findAll('form'))

        count=0
        links = []
        links.append(url)
        for link in soup.find_all('a'):
            if count>50:
                break
            count+=1
            urltoappend = urljoin(url,link.get('href'))
            if urltoappend not in links and url in urltoappend:
                links.append(urltoappend)
        if len(links) == 0:
            links.append(url)
        return links
        

    # main function to run the entire operation
    def executepipeline(self,target_url,):
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

        
        