# Author: Umesh Niure Sharma
# Date Created: October 11, 2022
# High Tech Pioneer Pvt. Ltd.

# Reference: https://www.youtube.com/watch?v=5cg_yggtkso

import pathlib
import cv2

cascade_path = pathlib.Path(cv2.__file__).parent.absolute() / "data/haarcascade_frontalface_default.xml"
clf = cv2.CascadeClassifier(str(cascade_path))

camera = cv2.VideoCapture(0)
# camera = cv2.VideoCapture("people.mp4")

while True:
    _, frame = camera.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = clf.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=6, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
    for (x, y, width, height) in faces:
        cv2.rectangle(frame, (x, y), (x + width, y + height), (255, 255, 0), 2)
        cv2.putText(frame, "press 'q' to exit.", (0, 15), cv2.FONT_HERSHEY_TRIPLEX, 0.5,  (0, 255, 0), thickness=1)
        cv2.imshow("Faces", frame)
    if cv2.waitKey(1) == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
