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


@app.route('/testpost',methods = ['POST', 'GET'])
def testpost():
    if request.method == 'POST':
        target_url=request.get_json()['url']
        scan_settings=request.get_json()['vulnerabilities']
        #   print(str(scan_settings))
        z.executepipeline(target_url,scan_settings,)
        return "posted successfully"
    else:
        return str(z.target_link_list)

