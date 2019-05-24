from iotc import IOTConnectType, IOTLogLevel
import iotc

import time
import os
from random import randint
from enum import Enum
import threading
import json
import cv2


class SimDeviceModel:
    fanSpeed = 0
    temperature = 0
    ismaint = False


class IoTClientType:
    IOTCENTRAL = 0
    IOTHUB = 1


class IoTClientHandler(object):
    simDeviceModel = None
    canSend = False

    hubType = IoTClientType.IOTCENTRAL

    client = None
    me = None

    @staticmethod
    def getInstance():
        if IoTClientHandler.me == None:
            IoTClientHandler.me = IoTClientHandler(IoTClientType.IOTCENTRAL)

        return IoTClientHandler.me

    def init_iotc(self):
        print('init_iotc')
        deviceId = os.getenv("DEVICE_ID")
        scopeId = os.getenv("SCOPE_ID")
        deviceKey = os.getenv("DEVICE_KEY")
        self.client = iotc.Device(scopeId, deviceKey, deviceId,
                                  IOTConnectType.IOTC_CONNECT_SYMM_KEY)
        self.client.setLogLevel(IOTLogLevel.IOTC_LOGGING_API_ONLY)

        self.simDeviceModel = SimDeviceModel()

    def __init__(self, type):
        if type == IoTClientType.IOTCENTRAL:
            self.hubType = type
            self.init_iotc()

    def onconnect(self, info):
        print("onConnect => status:" + str(info.getStatusCode()))
        if info.getStatusCode() == 0:
            print("connectionStatus is Good")

    def onmessagesent(self, info):
        print("onMessageSent => " + str(info.getPayload()))

    def oncommand(self, info):
        print("command name: ", info.getTag())
        print("command value: ", info.getPayload())

    def onsettingsupdated(self, info):
        print("setting name: ", info.getTag())
        print("setting value: ", info.getPayload())

        if 'fanSpeed' == info.getTag():
            val = json.loads(info.getPayload())
            print(val["value"])
            self.simDeviceModel.fanSpeed = 100

    def connect(self):
        self.client.on("ConnectionStatus", self.onconnect)
        self.client.on("MessageSent", self.onmessagesent)
        self.client.on("Command", self.oncommand)
        self.client.on("SettingsUpdated", self.onsettingsupdated)

        self.client.connect()

        if self.client.isConnected():
            print("connected")
            self.canSend = True

    def send(self):
        delta = 1
        while self.client.isConnected():
            time.sleep(2)
            if self.canSend == True:
                t = int(self.simDeviceModel.temperature)
                self.client.sendTelemetry(
                    "{\"temperature\": " + str(
                        randint(t - 5, t + 5)) + "}")
            self.simDeviceModel.temperature += delta

            if self.simDeviceModel.temperature > 0 and self.simDeviceModel.temperature < 10:
                self.client.sendState(
                    "{\"deviceState\": \"Normal\" }")
            elif self.simDeviceModel.temperature <= 0 and self.simDeviceModel.temperature > -10:
                self.client.sendState(
                    "{\"deviceState\": \"Caution\" }")
            elif self.simDeviceModel.temperature >= 10 and self.simDeviceModel.temperature < 20:
                self.client.sendState(
                    "{\"deviceState\": \"Caution\" }")
            elif abs(self.simDeviceModel.temperature) >= 30:
                if self.simDeviceModel.temperature > 0:
                    delta = -1
                else:
                    delta = 1
            else:
                self.client.sendState(
                    "{\"deviceState\": \"Danger\" }")

    def run(self):
        self.connect()
        telemetryThread = threading.Thread(target=self.send)
        telemetryThread.start()

    def setFunSpeed(self, speed):
        self.simDeviceModel.fanspeed = speed

    def setTemperature(self, temp):
        self.simDeviceModel.temperature = temp

    def sendStateMaintenance(self, ismaint):
        self.simDeviceModel.ismaint = ismaint
        self.client.sendState(
            "{\"ismaintenance\": " + ismaint + "}")

    def sendPersonCount(self):
        # cap = cv2.VideoCapture(0)
        cap = cv2.VideoCapture('face-demographics-walking.mp4')

        cascade_path = "/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml"
        cascade = cv2.CascadeClassifier(cascade_path)

        color = (255, 255, 255)

        cont = True

        while cont:
            cont, frame = cap.read()

            facerect = cascade.detectMultiScale(
                frame, scaleFactor=1.2, minNeighbors=2, minSize=(10, 10))

            if cont:
                cv2.imshow("frame", frame)

            if len(facerect) > 0:

                area = 0
                for rect in facerect:
                    # cv2.rectangle(frame, tuple(rect[0:2]), tuple(
                    #    rect[0:2]+rect[2:4]), color, thickness=2)

                    # size = tuple(rect[2:4] - rect[0:2])
                    w = rect[2]
                    h = rect[3]
                    area = area + (rect[2] * rect[3])/1000
                    # self.client.sendTelemetry(
                    #     "{\"width\": " + str(w) +
                    #     ", \"height\": " + str(h) + "}"
                    # )
                    # print(
                    #     "{\"width\": " + str(w) +
                    #     ", \"height\": " + str(h) + "}"
                    # )

                self.client.sendTelemetry(
                    "{\"numOfFace\" : " +
                    str(len(facerect)) + ", \"area\" :" + str(area) + "}"
                )
                print(
                    "{\"numOfFace\" : " +
                    str(len(facerect)) + ", \"area\" :" + str(area) + "}"
                )
            # cv2.imshow("frame", frame)

            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #    break

        cap.release()
        cv2.destroyAllWindows()


def main(type):
    # handler = IoTClientHandler(IoTClientType.IOTCENTRAL)
    handler = IoTClientHandler.getInstance()
    handler.connect()

    print(handler)

    telemetryThread = threading.Thread(target=handler.send)
    telemetryThread.start()

    handler.sendPersonCount()

    hhandler = IoTClientHandler.getInstance()

    print(hhandler)
    hhandler.sendStateMaintenance("True")


if __name__ == '__main__':
    main(IoTClientType.IOTCENTRAL)
