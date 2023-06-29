from time import sleep
import json
from flask import Flask, jsonify, render_template, request
import os
import stm32CLI

STATIC_PATH = 'main'
STATIC_URL_PATH = '/main'
TEMPLATE_PATH = 'main/template/'

app = Flask(__name__, template_folder=TEMPLATE_PATH, static_url_path=STATIC_URL_PATH, static_folder=STATIC_PATH)

stm32API = stm32CLI.Stm32()


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
    datalayer = {'Status': stm32API.status}
    response = app.response_class(
        response=json.dumps(datalayer),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/test', methods=['POST', 'GET'])
def test():
    for i in request.form:
        data = json.loads(i)
        if data["cmd"] == "start_flashing":
            stm32API.start_flash()
            datalayer = {'Status': stm32API.status}
        elif data["cmd"] == "get_firmware_version":
            try:
                print("Try to udpate git repository")
                print("Update was succesfull!")
            except Exception as e:
                print("Git error: ", e)
            datalayer = {'Status': stm32API.firmwareVersion, 'Tester': getVersion()}
        elif data["cmd"] == "start_test":
            sleep(3)
            test_report = stm32API.start_testing()
            datalayer = {'Status': stm32API.status, "Report": stm32API.status}

    response = app.response_class(
        response=json.dumps(datalayer),
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


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True, use_reloader=False)
