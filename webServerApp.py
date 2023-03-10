from time import time,sleep
import json
from typing import IO
from flask import Flask, jsonify, render_template, request
from flask.wrappers import Request
import os
from sys import getsizeof
from gitCLI import Git
import stm32CLI
import JlinkCLI

STATIC_PATH = 'main'
STATIC_URL_PATH = '/main'
TEMPLATE_PATH = 'main/template/'

app = Flask(__name__,template_folder=TEMPLATE_PATH,static_url_path=STATIC_URL_PATH,static_folder=STATIC_PATH)

stm32API = stm32CLI.Stm32()
'''zde mozno otestovat pripojeni a flashnuti - nezapomenout napajet externe pokud JLink neumi!!'''
#stm32API = JlinkCLI.JlinkFlasher() 
#stm32API.testJlinkConnection()
#stm32API.flashMCU() 

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/overview')
def overview():
    return render_template('overview.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/updateData')
def updateData():
    datalayer = {'Status':stm32API.status}
    response = app.response_class(
        response =json.dumps(datalayer),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/test',methods = ['POST','GET'])
def test():
    for i in request.form:
        data = json.loads(i)
        if data["cmd"] == "start_flashing":
            stm32API.start_flash()
            datalayer = {'Status':stm32API.status}
        elif data["cmd"] == "get_firmware_version":
            try:
                print("Try to udpate git repository")
                #git_repo = Git()
                #$git_repo.pull()
                print("Update was succesfull!")
            except Exception as e:
                print("Git error: ",e)
            datalayer = {'Status':stm32API.firmwareVersion,'Tester':getVersion()}
        elif data["cmd"] == "start_test":
            test_report = stm32API.start_testing()
            datalayer = {'Status':stm32API.status,"Report":test_report}

    response = app.response_class(
        response =json.dumps(datalayer),
        status=200,
        mimetype='application/json'
    )
    return response

def getVersion():
    arr = os.listdir()
    for i in arr:
        if i[:3] == "rev":
            version = i[3:]
            version = version.split("_")
            return version[1]
    return "0.0.0"

if __name__ =='__main__':
    app.run(host="0.0.0.0",port=8000,debug=True,use_reloader=False)
    #loop = asyncio.get_event_loop

