import time
import os
import queue
import threading
import json
import cv2


class MyTimer:
    delta = 0
    isReady = False


def wakeup():
    print("Zzzz...")
    time.sleep(mt.delta)
    mt.isReady = True
    print("Wake up")


def sendPersonCount():
    cap = cv2.VideoCapture(0)
    cascade_path = "/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml"
    cascade = cv2.CascadeClassifier(cascade_path)

    color = (255, 255, 255)

    cont = True

    q = queue.Queue()
    while cont:
        cont, frame = cap.read()

        if cont:
            q.put(frame)
            facerect = cascade.detectMultiScale(
                frame, scaleFactor=1.2, minNeighbors=2, minSize=(10, 10))

            if len(facerect) > 0:
                for rect in facerect:
                    cv2.rectangle(frame, tuple(rect[0:2]), tuple(
                        rect[0:2]+rect[2:4]), color, thickness=2)

            if mt.isReady:
                cv2.imshow("frame", q.get())
                q.task_done()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':

    mt = MyTimer()
    mt.delta = 5
    th = threading.Thread(target=wakeup)
    th.start()
    sendPersonCount()
