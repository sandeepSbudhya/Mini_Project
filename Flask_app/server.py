from os import close
from flask import Flask,request
import Spider as spider
from flask_cors import CORS
import multiprocessing
import scanner as sc

cors_config = {
    "origins":["http://localhost:3000"]
}
z=spider.Spider()
y=sc.Scanner()
app = Flask(__name__)
CORS(app,resources={
    r"/*":cors_config
})

@app.route('/', methods = ['GET'])
def function1():
    return "root"


@app.route('/test',methods = ['POST', 'GET'])
def testpost():
    if request.method == 'POST':
        target_url=request.get_json()['url']
        z.executepipeline(target_url,)
        return "posted successfully"
    else:
        subdomains=[]
        links=[]
        with open("./subdomainscans/"+z.subdomainfilename,"r") as sdlist:
            for sd in sdlist:
                subdomains.append(sd.strip())
        with open("./linkscans/"+z.linksfilename,"r") as llist:
            for l in llist:
                links.append(l.strip())
        return {
            "subdomains":subdomains,
            "links":links
        }


@app.route('/scanner', methods = ['POST', 'GET'])
def vuln_scan():
    if request.method == 'POST':
        data=request.get_json()
        d={}
        if data:
            if data['cors'] or data['csrf']:
                return "we are currently working on scanning for cors and csrf vulnerabilities, please re-run the scan without these checked."
            if data['xss'] == True:
                d['xss'] = y.run_scanner(z.linksfilename)
                if not d['xss']:
                    d['xss']=[]
            if data['cj'] == True:
                d['clickjacking'] = y.run_clickjacking(z.linksfilename)
                if not d['clickjacking']:
                    d['clickjacking']=[]
            return d
        return "something went wrong please re-run the test"


    

