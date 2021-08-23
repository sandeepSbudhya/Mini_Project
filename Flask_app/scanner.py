import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin

from requests.sessions import InvalidSchema


#scanner module
class Scanner:
    target_urls = []   #class variable availiable throughout class holds all links
    def __init__(self):
        self.session = requests.Session()

    # reads all links from links file and returns list
    def get_links(self, filename, ):
        with open("./linkscans/" + filename, "r") as links:
             for link in links:
                self.target_urls.append(link)


    # extracts all the forms in given link
    def extract_forms(self, url):
        try:
            response = self.session.get(url)
            if response:
                parsed_html = bs(response.text, 'html.parser')
                return parsed_html.findAll('form')
            return []
        except requests.exceptions.InvalidSchema:
            pass

    # submits form with given javascript payload
    def submit_form(self, form, value, url):
        action = form.get("action")
        post_url = urljoin(url, action)
        method = form.get("method")
        inputs_list = form.findAll("input")
        post_data = {}
        for input in inputs_list:
            input_name = input.get("name")
            input_type = input.get("type")
            input_value = input.get("value")
            if input_type == "text":
                input_value = value

            post_data[input_name] = input_value

        if method == "post":
            return requests.post(post_url, data=post_data)
        return requests.get(post_url, params=post_data)

    # test for xss vulnerability in link 
    def test_xss_in_link(self, url):
        xss_test_script = "<script>alert(1)</script>"
        url = url.replace("=", "=" + xss_test_script)
        try:
            response = requests.get(url)
            return xss_test_script in str(response.content)
        except requests.exceptions.InvalidSchema:
            pass
    # test for xss vulnerability in form 
    def test_xss_in_form(self,form,url):
        xss_test_script = "<script>alert(1)</script>"
        try:
            response = self.submit_form(form, xss_test_script, url)
            return xss_test_script in str(response.content)
        except requests.exceptions.InvalidSchema:
            pass


    # main function to run the entire operation returns dict of all vulnerabilities as key value pairs
    def run_scanner(self, filename):
        self.target_urls=[]
        self.get_links(filename, )
        xss_vuln_list = []
        
        for l in self.target_urls:
            print("Testing in " + l)
            forms = self.extract_forms(l.strip())
            if forms:
                for form in forms:
                    print("[+] Testing form in " + l)
                    is_vulnerable = self.test_xss_in_form(form, l)
                    if is_vulnerable:
                        xss_vuln_list.append(l)
                        print("XSS discovered in " + l + " in the following form")
                        print(form)

            if "=" in l:
                print("[+] testing " + l)
                is_vuln = self.test_xss_in_link(l)
                if is_vuln:
                    if l not in xss_vuln_list:
                        xss_vuln_list.append(l)
                    print("XSS discovered in the following link " + l)
    

        return xss_vuln_list


    def run_clickjacking(self,filename):
        cjlist=[]
        if not self.target_urls:
            self.get_links(filename, )
        for l in self.target_urls:
            res=requests.get(l.strip())
            cj = res.headers.get('X-Frame-Options')
            if not cj:
                print(l+" may be vulnerable to click-jacking")
                cjlist.append(l)
        return cjlist
        






