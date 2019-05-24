from time import time, sleep
import cv2


class VideoCamera():
    def __init__(self):
        self.frames = []
        self.files = []
        self.MAX_FRAME_NUM = 10
        self.RECORD_INTERVAL = 1

        self.record()

    def get_frame(self):
        for file in self.files:
            self.frames.append(open(file, 'rb').read())
        return self.frames[int(time()) % len(self.frames)]

    def record(self):
        self.cap = cv2.VideoCapture(0)

        cnt = 0
        while True:
            print("record")
            path = 'img' + str(cnt) + '.jpg'
            ret, frame = self.cap.read()
            self.files.append(path)

            cv2.imwrite(path, frame)

            k = cv2.waitKey(1)
            if k == 27:
                break

            cnt += 1
            if cnt == self.MAX_FRAME_NUM:
                break

            sleep(self.RECORD_INTERVAL)

        self.cap.release()
        cv2.destroyAllWindows()


def main():
    camera = VideoCamera()
    camera.record()


if __name__ == '__main__':
    main()
