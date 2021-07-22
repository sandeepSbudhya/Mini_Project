#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import Spider

class Scanner:
    target_urls = []
    def __init__(self):
        self.session = requests.Session()


    def get_links(self, filename, ):
        with open("./linkscans/" + filename, "r") as links:
             for link in links:
                self.target_urls.append(link)



    def extract_forms(self, url):
        try:
            response = self.session.get(url)
            if response:
                parsed_html = bs(response.content, 'html.parser')
                return parsed_html.findAll("form")
            return []
        except requests.exceptions.ConnectionError:
            pass
    def submit_form(self, form, value, url):
        action = form.get("action")
        post_url = urljoin(url, action)
        method = form.get("method")
        inputs_list = form.findAll("Input")
        post_data = {}
        for input in inputs_list:
            input_name = input.get("name")
            input_type = input.get("type")
            input_value = input.get("value")
            if input_type == "text":
                input_value = value

            post_data[input_name] = input_value
        if method == "post":
            return self.session.post(post_url, data=post_data)
        return self.session.get(post_url, params=post_data)


    def run_scanner(self,filename):
        self.get_links(filename, )
        xss_vuln_list = {}
        for l in self.target_urls:
            # print("Testin in " +l)
            forms = self.extract_forms(l)
            if forms:
                for form in forms:
                    print("[+] Testing form in "+ l)
                    is_vulnerable = self.test_xss_in_form(form, l)
                    if is_vulnerable:
                        xss_vuln_list[l] = True
                        print("XSS discovered in " + l + " in the following form")
                        print(form)

            if "=" in l:
                 print("[+] testing " + l)
                 is_vuln = self.test_xss_in_link(l)
                 if is_vuln:
                     xss_vuln_list[l] = True
                     print("XSS discovered in in the following link " + l)

        return xss_vuln_list

    def test_xss_in_link(self, url):
        xss_test_script = "image src =q onerror=prompt(8)>"
        url = url.replace("=", "=" + xss_test_script)
        response = self.session.get(url)
        return xss_test_script in str(response.content)

    def test_xss_in_form(self,form,url):
        xss_test_script = "image src =q onerror=prompt(8)>"
        response = self.submit_form(form, xss_test_script, url)
        return xss_test_script in str(response.content)






