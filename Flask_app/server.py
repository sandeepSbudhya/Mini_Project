from flask import Flask,request
import soupscript as script2
from flask_cors import CORS

cors_config = {
    "origins":["http://localhost:3000"]
}

app = Flask(__name__)
CORS(app,resources={
    r"/*"
})

@app.route('/', methods = ['GET'])
def function1():
    return "root"

@app.route("/souproute")
def function2():
    y = script2.Examplesoup()
    url = "https://xss-game.appspot.com/level1/frame"
    reply = y.scan_xss(url)
    return str(reply)

@app.route('/testpost',methods = ['POST', 'GET'])
def testpost():
   if request.method == 'POST':
      z=script2.Examplesoup()
    #   print(request.data)
      target_url=request.get_json()['url']
    #   print(str(target_url))
      print(target_url)
      target_links=[]
      z.crawl(target_url,target_url,target_links)
      return "posted successfully"
   else:
      return "geted"