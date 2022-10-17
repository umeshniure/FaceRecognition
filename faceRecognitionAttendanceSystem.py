import os
import cv2 as cv
import numpy as np
import face_recognition
from datetime import datetime
from playsound import playsound

attendance_image_path = 'AttendanceImages'
images = []
image_names = []
encode_list_known = []
image_list = os.listdir(attendance_image_path)

print('Getting Started...')


def loadAllImages():
    print(image_list)
    for image in image_list:
        current_img = cv.imread(f'{attendance_image_path}/{image}')
        images.append(current_img)
        image_names.append(os.path.splitext(image)[0])


loadAllImages()


def markAttendance(name):
    with open('Attendance.csv', 'r+') as attendance_file:
        my_attendance_list = attendance_file.readlines()
        attendance_name_list = []
        for line in my_attendance_list:
            first_entry = line.split(',')
            attendance_name_list.append(first_entry[0])
        if name not in attendance_name_list:
            now = datetime.now()
            time_string = now.strftime('%H:%M:%S')
            attendance_file.writelines(f'\n{name}, {time_string}')
            return True


def findEncodings(images):
    encod_list = []
    for img in images:
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encod_list.append(encode)
    return encod_list


def encodeOneImage(image):
    return face_recognition.face_encodings(image)[0]


def captureUnknownFace(image):
    global encode_list_known, image_list
    print("Enter name: ")
    image_name = input()
    cv.imwrite((attendance_image_path + '/' + image_name + '.jpg'), image)
    print('Image saved successfully.')
    image_list = os.listdir(attendance_image_path)
    loadAllImages()
    encode_list_known.append(encodeOneImage(image))
    # encode_list_known = findEncodings(images)


# encode list of known images
encode_list_known = findEncodings(images)
print('Encoding images completed.')

print('Now, recognizing through camera....')

camera = cv.VideoCapture(0)
temp = ''
while True:
    success, frame_image = camera.read()
    rescaled_image = cv.resize(frame_image, (0, 0), None, 0.5, 0.5)
    rescaled_image = cv.cvtColor(rescaled_image, cv.COLOR_BGR2RGB)

    current_frame_location = face_recognition.face_locations(rescaled_image)
    encoded_current_frame = face_recognition.face_encodings(rescaled_image, current_frame_location)

    for encode_face, face_location in zip(encoded_current_frame, current_frame_location):
        matches = face_recognition.compare_faces(encode_list_known, encode_face)
        face_distance = face_recognition.face_distance(encode_list_known, encode_face)

        match_index = np.argmin(face_distance)
        if matches[match_index]:
            name = image_names[match_index].upper()
            y1, x2, y2, x1 = face_location
            y1, x2, y2, x1 = y1 * 2, x2 * 2, y2 * 2, x1 * 2
            cv.rectangle(frame_image, (x1, y1), (x2, y2), (0, 255, 0), 3)
            cv.rectangle(frame_image, (x1 - 2, y2 + 35), (x2 + 2, y2), (0, 255, 0), cv.FILLED)
            cv.putText(frame_image, f'{name}', (x1 + 6, y2 + 25), cv.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255), 1)
            if markAttendance(name):
                print(f"'{name}', your attendance is registered successfully.")
                cv.rectangle(frame_image, (x1, y1), (x2, y2), (0, 255, 0), cv.FILLED)
                playsound('Audio/well_done.mp3', False)
            else:
                if temp != name:
                    cv.putText(frame_image, f'{name} (Done)', (x1 + 6, y2 + 25), cv.FONT_HERSHEY_DUPLEX, 0.5,
                               (0, 0, 255), 1)
                    print(f"'{name}', your attendance is already registered.")
                    temp = name
                else:
                    cv.putText(frame_image, f'{name} (Done)', (x1 + 6, y2 + 25), cv.FONT_HERSHEY_DUPLEX, 0.5,
                               (0, 0, 255), 1)

        else:
            image_copy = frame_image.copy()
            y1, x2, y2, x1 = face_location
            y1, x2, y2, x1 = y1 * 2, x2 * 2, y2 * 2, x1 * 2
            cv.rectangle(frame_image, (x1, y1), (x2, y2), (0, 255, 0), 3)
            cv.rectangle(frame_image, (x1 - 2, y2 + 35), (x2 + 2, y2), (0, 255, 0), cv.FILLED)
            cv.putText(frame_image, 'Unknown', (x1 + 6, y2 + 25), cv.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255), 1)

            if cv.waitKey(1) == ord("s"):
                captureUnknownFace(image_copy)
                del image_copy

        cv.imshow('Camera', frame_image)
    cv.imshow('Camera', frame_image)
    if cv.waitKey(1) == ord("q"):
        break

print('Face recognition is stopped.')
camera.release()
cv.destroyAllWindows()