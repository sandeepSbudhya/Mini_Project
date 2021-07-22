from os import close
from flask import Flask,request
import Spider as spider
from flask_cors import CORS
import multiprocessing


cors_config = {
    "origins":["http://localhost:3000"]
}
z=spider.Spider()

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
        #   print(str(scan_settings))
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


@app.route('/scan',methods = ['POST', 'GET'])
def runscanner():
        
    if request.method == 'POST':
        data = request.get_json()
        if data and data['vulnscan']['xss'] == True:
            return z.xssvulnlist
        with open("./linkscans/"+z.linksfilename,"r") as llist:
            for l in llist:
                bool = z.scan_xss(l)
                if bool:
                    z.xssvulnlist[l]=True
            llist.close()
        return "scan finished"
    
