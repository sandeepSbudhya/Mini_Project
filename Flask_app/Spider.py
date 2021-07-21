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
    xssvulnlist={}
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
        count1=0
        #sudbomain finder
        try:
            with open("./subdomains-wordlist.txt", "r") as wordlist_file:
                for line in wordlist_file:
                    count1+=1
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
                    if count1>100:
                        if count==0:
                            with open("./subdomainscans/subdomains"+timestring,"a") as subdomain_file:
                                subdomain_file.write("http://"+url+"\n")
                                subdomain_file.close()
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
            if count>50:
                break
            count+=1
            urltoappend = urljoin(url,link.get('href'))
            if urltoappend not in links:
                links.append(urltoappend)
        return links

    def get_all_forms(self,url):
        soup = bs(requests.get(url).content, "html.parser")
        return soup.find_all("form")

    def get_form_details(self,form):
        details = {}
        # get the form action (target url)
        action = form.attrs.get("action").lower()
        # get the form method (POST, GET, etc.)
        method = form.attrs.get("method", "get").lower()
        # get all the input details such as type and name
        inputs = []
        for input_tag in form.find_all("input"):
            input_type = input_tag.attrs.get("type", "text")
            input_name = input_tag.attrs.get("name")
            inputs.append({"type": input_type, "name": input_name})
        # put everything to the resulting dictionary
        details["action"] = action
        details["method"] = method
        details["inputs"] = inputs
        return details

    def submit_form(self,form_details, url, value):
    
    # Submits a form given in `form_details`
    # Params:
    #     form_details (list): a dictionary that contain form information
    #     url (str): the original URL that contain that form
    #     value (str): this will be replaced to all text and search inputs
    # Returns the HTTP Response after form submission
    # construct the full URL (if the url provided in action is relative)
        target_url = urljoin(url, form_details["action"])
        # get the inputs
        inputs = form_details["inputs"]
        data = {}
        for input in inputs:
            # replace all text and search values with `value`
            if input["type"] == "text" or input["type"] == "search":
                input["value"] = value
            input_name = input.get("name")
            input_value = input.get("value")
            if input_name and input_value:
                # if input name and value are not None, 
                # then add them to the data of form submission
                data[input_name] = input_value

        if form_details["method"] == "post":
            return requests.post(target_url, data=data)
        else:
            # GET request
            return requests.get(target_url, params=data)

    def scan_xss(self,url):
    #
    # Given a `url`, it prints all XSS vulnerable forms and 
    # returns True if any is vulnerable, False otherwise
    # 
    # get all the forms from the URL
        forms = self.get_all_forms(url)
        print(f"[+] Detected {len(forms)} forms on {url}.")
        js_script = "<script>alert('hi')</script>"
        # returning value
        is_vulnerable = False
        # iterate over all forms
        for form in forms:
            form_details = self.get_form_details(form)
            content = self.submit_form(form_details, url, js_script).content.decode()
            if js_script in content:
                print(f"[+] XSS Detected on {url}")
                print(f"[*] Form details:")
                pprint(form_details)
                is_vulnerable = True
                # won't break because we want to print available vulnerable forms
        return is_vulnerable

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

        
        