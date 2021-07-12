from flask import Flask
import example_script as script1
import soupscript as script2

app = Flask(__name__)

@app.route("/")
def function1():
    x = script1.Example_class("sandeep","Jayanagar")
    y=x.function1()
    print(y)
    reply={
        "name":x.name,
        "address":x.fromLoc
    }
    return reply

@app.route("/souproute")
def function2():
    y = script2.Examplesoup()
    reply = y.printgooglefunc()
    return reply