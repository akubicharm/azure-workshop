from iotc import IOTConnectType, IOTLogLevel
import iotc

import time
import os
from random import randint
from enum import Enum
import threading
import json
import cv2
import tkinter


class SimDeviceModel:
    fanSpeed = 0
    temperature = 0
    delta = 1


class IoTClientHandler(object):
    simDeviceModel = None
    canSend = False
    waitForExit = False

    client = None

    def __init__(self):
        print('init_iotc')
        deviceId = os.getenv("DEVICE_ID")
        scopeId = os.getenv("SCOPE_ID")
        deviceKey = os.getenv("DEVICE_KEY")
        self.client = iotc.Device(scopeId, deviceKey, deviceId,
                                  IOTConnectType.IOTC_CONNECT_SYMM_KEY)
        self.client.setLogLevel(IOTLogLevel.IOTC_LOGGING_API_ONLY)
        self.simDeviceModel = SimDeviceModel()

    def onconnect(self, info):
        print("onConnect => status:" + str(info.getStatusCode()))
        if info.getStatusCode() == 0:
            print("connectionStatus is Good")

    def onmessagesent(self, info):
        print("onMessageSent => " + str(info.getPayload()))

    def oncommand(self, info):
        print("command name: ", info.getTag())
        print("command value: ", info.getPayload())
        if 'beep' == info.getTag():
            print("\007")

    def onsettingsupdated(self, info):
        print("setting name: ", info.getTag())
        print("setting value: ", info.getPayload())

        if 'fanSpeed' == info.getTag():
            val = json.loads(info.getPayload())
            newSpeed = val["value"]
            print(str(self.simDeviceModel.fanSpeed) + ", " + str(newSpeed))
            if self.simDeviceModel.fanSpeed > newSpeed:
                self.simDeviceModel.delta = 2
            else:
                self.simDeviceModel.delta = -2
            self.simDeviceModel.fanSpeed = newSpeed

    def connect(self):
        self.client.on("ConnectionStatus", self.onconnect)
        self.client.on("MessageSent", self.onmessagesent)
        self.client.on("Command", self.oncommand)
        self.client.on("SettingsUpdated", self.onsettingsupdated)

        self.client.connect()

        if self.client.isConnected():
            print("connected")
            self.canSend = True
            self.client.sendProperty(json.dumps(
                {'dieNumber': 1}
            ))

    def send(self):
        while self.client.isConnected():
            if self.waitForExit:
                break
            time.sleep(2)
            if self.canSend == True:
                t = int(self.simDeviceModel.temperature)
                self.client.sendTelemetry(json.dumps(
                    {'temperature': randint(t - 5, t + 5)}
                ))

                self.simDeviceModel.temperature += self.simDeviceModel.delta

                if self.simDeviceModel.temperature > 0 and self.simDeviceModel.temperature < 10:
                    self.client.sendState(json.dumps(
                        {'deviceState': 'Normal'}
                    ))
                elif self.simDeviceModel.temperature <= 0 and self.simDeviceModel.temperature > -10:
                    self.client.sendState(json.dumps(
                        {'deviceState': 'Caution'}
                    ))
                elif self.simDeviceModel.temperature >= 10 and self.simDeviceModel.temperature < 20:
                    self.client.sendState(json.dumps(
                        {'deviceState': 'Caution'}
                    ))
                elif abs(self.simDeviceModel.temperature) >= 30:
                    self.client.sendState(json.dumps(
                        {'deviceState': 'Danger'}
                    ))
                    self.simDeviceModel.delta = 0
                else:
                    self.client.sendState(json.dumps(
                        {'deviceState': 'Caution'}
                    ))

    def sendPersonCount(self):
        # cap = cv2.VideoCapture(0)
        cap = cv2.VideoCapture('face-demographics-walking.mp4')
        #cascade_path = "/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml"
        cascade_path = "haarcascade_frontalface_alt.xml"
        # cap = cv2.VideoCapture('car-detection.mp4')
        # cascade_path = "cars.xml"
        cascade = cv2.CascadeClassifier(cascade_path)

        color = (255, 255, 255)

        wname = 'frame'
        cv2.namedWindow(wname)
        cv2.setMouseCallback(wname, self.mouseClicked)

        cont = True
        while cont:
            cont, frame = cap.read()

            if cont:
                facerect = cascade.detectMultiScale(
                    frame, scaleFactor=1.2, minNeighbors=2, minSize=(10, 10))

                if len(facerect) > 0:
                    list = []
                    numOfFace = len(facerect)

                    for rect in facerect:
                        cv2.rectangle(frame, tuple(rect[0:2]), tuple(
                            rect[0:2]+rect[2:4]), color, thickness=2)

                    self.client.sendTelemetry(json.dumps(
                        {'numOfFace': numOfFace}
                    ))

                    cv2.imshow("frame", frame)
            else:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                cont = True

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        self.waitForExit = True

    def mouseClicked(self, event, x, y, flags, param):
        if event in {cv2.EVENT_LBUTTONDOWN, cv2.EVENT_MBUTTONDOWN, cv2.EVENT_RBUTTONDOWN}:
            print(event)
            self.client.sendEvent(json.dumps(
                {'button1': 'click'}
            ))


def main():
    handler = IoTClientHandler()
    handler.connect()

    # telemetryThread = threading.Thread(target=handler.send)
    # telemetryThread.start()

    handler.sendPersonCount()


if __name__ == '__main__':
    main()
