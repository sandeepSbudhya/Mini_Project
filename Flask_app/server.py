from flask import Flask
import soupscript as script2

app = Flask(__name__)

@app.route("/")
def function1():
    return "route"

@app.route("/souproute")
def function2():
    y = script2.Examplesoup()
    url = "https://xss-game.appspot.com/level1/frame"
    reply = y.scan_xss(url)
    return str(reply)