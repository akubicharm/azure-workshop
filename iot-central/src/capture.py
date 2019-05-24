import cv2

if __name__ == "__main__":

    cap = cv2.VideoCapture(0)

    cascade_path = "/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml"
    cascade = cv2.CascadeClassifier(cascade_path)

    color = (255, 255, 255)

    while True:

        ret, frame = cap.read()

        facerect = cascade.detectMultiScale(
            frame, scaleFactor=1.2, minNeighbors=2, minSize=(10, 10))

        if len(facerect) > 0:
            for rect in facerect:
                cv2.rectangle(frame, tuple(rect[0:2]), tuple(
                    rect[0:2]+rect[2:4]), color, thickness=2)

        cv2.imshow("frame", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
