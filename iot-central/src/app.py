from flask import Flask, render_template, request
import os
from datetime import datetime
from client import IoTClientHandler, IoTClientType

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/init')
def init():
    print("init")
    #handler = IoTClientHandler(IoTClientType.IOTCENTRAL)
    handler = IoTClientHandler.getInstance()
    handler.run()
    return render_template("device.html", fanspeed=0)


@app.route('/telemetry', methods=['POST', 'GET'])
def sendTelemetry():
    temp = request.form["temperature"]
    handler = IoTClientHandler.getInstance()
    handler.setTemperature(temp)
    return render_template("device.html")


@app.route('/maintenance', methods=['POST', 'GET'])
def setMaintenanceMode():
    print("maint" + request.form["ismaintenance"])
    isMaint = request.form["ismaintenance"]
    handler = IoTClientHandler.getInstance()
    handler.sendStateMaintenance(isMaint)
    return render_template("device.html", fanspeed=10)


@app.route('/fanspeed', methods=['GET'])
def getFanspeed():
    handler = IoTClientHandler.getInstance()
    speed = handler.simDeviceModel.fanSpeed
    return render_template("device.html", fanspeed=speed)
