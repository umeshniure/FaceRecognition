import os
import cv2 as cv
import numpy as np
from tkinter import *
import face_recognition
import pyttsx3 as pytts
from datetime import datetime
from playsound import playsound

attendance_image_path = 'AttendanceImages'
images = []
image_names = []
encode_list_known = []
image_list = os.listdir(attendance_image_path)
print('-----------------------------------------------')
<<<<<<< HEAD
print('|              Getting Started...             |')
=======
print('|               Getting Started...            |')
>>>>>>> 490f8c900fe4e982308f8f28942c177130d71fe6
print('-----------------------------------------------')
print('Loading Images...')
for image in image_list:
    current_img = cv.imread(f'{attendance_image_path}/{image}')
    images.append(current_img)
<<<<<<< HEAD
    image_names.append(os.path.splitext(image)[0].title())
=======
    image_names.append(os.path.splitext(image)[0])
>>>>>>> 490f8c900fe4e982308f8f28942c177130d71fe6


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
<<<<<<< HEAD
    window = Tk()
    window.title('Enter Image Name')
    window.geometry('350x150')
    lbl = Label(window, text="Enter Name: ", font=('Arial Bold', 10), padx=10, pady=10)
    lbl.grid(column=0, row=0)

    def clicked(event=None):
        global image_list, image_names, encode_list_known
        image_name = txt.get().title()
        if image_name != '':
            if image_name in image_names:
                updated_name = image_name
                count = 0
                while os.path.isfile(attendance_image_path + '/' + updated_name + '.jpg') \
                        or os.path.isfile(attendance_image_path + '/' + updated_name + '.png'):
                    count = count + 1
                    updated_name = image_name + ' ' + str(count)
                cv.imwrite((attendance_image_path + '/' + updated_name + '.jpg'), image)
                print('Image saved successfully.')
                image_list = os.listdir(attendance_image_path)
                image_names.append(updated_name)
                encode_list_known.append(encodeOneImage(image))
                window.destroy()
            else:
                cv.imwrite((attendance_image_path + '/' + image_name + '.jpg'), image)
                print('Image saved successfully.')
                image_list = os.listdir(attendance_image_path)
                image_names.append(image_name)
                encode_list_known.append(encodeOneImage(image))
                window.destroy()
        else:
            lbl2 = Label(window, text="Name cannot be empty!", foreground='red', font=('Arial Bold', 8))
            lbl2.grid(column=1, row=1)
=======
    global encode_list_known

    window = Tk()
    window.title('Enter Image Name')
    window.geometry('350x200')
    lbl = Label(window, text="Enter Name: ", font=('Arial Bold', 10), padx=10, pady=20)
    lbl.pack(padx=10, pady=30)
    lbl.grid(column=0, row=0)

    def clicked(event=None):
        global image_list, image_names
        if txt.get() is not None:
            image_name = txt.get()
            cv.imwrite((attendance_image_path + '/' + image_name + '.jpg'), image)
            print('Image saved successfully.')
            image_list = os.listdir(attendance_image_path)
            image_names.append(image_name)
            encode_list_known.append(encodeOneImage(image))
            window.destroy()
>>>>>>> 490f8c900fe4e982308f8f28942c177130d71fe6

    txt = Entry(window, width=20, font=('Arial 12'), bg='white')
    txt.bind('<Return>', clicked)
    txt.grid(column=1, row=0, pady=20)
    btn = Button(window, text="Save", command=clicked, height=2, width=15)
<<<<<<< HEAD
    btn.grid(column=1, row=2, pady=10)
=======
    btn.grid(column=1, row=1, pady=10)
>>>>>>> 490f8c900fe4e982308f8f28942c177130d71fe6
    window.mainloop()


# encode list of known images
encode_list_known = findEncodings(images)
print('Encoding images completed.')

print('Now, recognizing through camera....')

camera = cv.VideoCapture(0)
temp = ''
while True:
    success, frame_image = camera.read()
    cv.imshow('Camera', frame_image)

    rescaled_image = cv.resize(frame_image, (0, 0), None, 0.5, 0.5)
    rescaled_image = cv.cvtColor(rescaled_image, cv.COLOR_BGR2RGB)

    current_frame_location = face_recognition.face_locations(rescaled_image)
    encoded_current_frame = face_recognition.face_encodings(rescaled_image, current_frame_location)

    for encode_face, face_location in zip(encoded_current_frame, current_frame_location):
        matches = face_recognition.compare_faces(encode_list_known, encode_face)
        face_distance = face_recognition.face_distance(encode_list_known, encode_face)
        match_index = np.argmin(face_distance)
        if matches[match_index]:
            name = image_names[match_index]
            y1, x2, y2, x1 = face_location
            y1, x2, y2, x1 = y1 * 2, x2 * 2, y2 * 2, x1 * 2
            cv.rectangle(frame_image, (x1, y1), (x2, y2), (0, 255, 0), 3)
            cv.rectangle(frame_image, (x1 - 2, y2 + 35), (x2 + 2, y2), (0, 255, 0), cv.FILLED)
            cv.putText(frame_image, f'{name}', (x1 + 6, y2 + 25), cv.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255), 1)
            cv.imshow('Camera', frame_image)
            if markAttendance(name):
                print(f"'{name}', your attendance is registered successfully.")
                cv.rectangle(frame_image, (x1, y1), (x2, y2), (0, 255, 0), cv.FILLED)
                cv.imshow('Camera', frame_image)
                playsound('Audio/well_done.mp3')

<<<<<<< HEAD
                # engine = pytts.init()
                # engine.say(name + ', Your Attendance is completed.')
                # engine.runAndWait()
                # engine.stop()
=======
                engine = pytts.init()
                engine.say(name + ', Your Attendance is completed.')
                engine.runAndWait()
                engine.stop()
>>>>>>> 490f8c900fe4e982308f8f28942c177130d71fe6
            else:
                if temp != name:
                    cv.putText(frame_image, f'{name} (Done)', (x1 + 6, y2 + 25), cv.FONT_HERSHEY_DUPLEX, 0.5,
                               (0, 0, 255), 1)
                    cv.imshow('Camera', frame_image)
                    print(f"'{name}', your attendance is already registered.")

<<<<<<< HEAD
                    # engine = pytts.init()
                    # engine.say(name + ', Your Attendance is already registered.')
                    # engine.runAndWait()
                    # engine.stop()
=======
                    engine = pytts.init()
                    engine.say(name + ', Your Attendance is already registered.')
                    engine.runAndWait()
                    engine.stop()
>>>>>>> 490f8c900fe4e982308f8f28942c177130d71fe6

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
            cv.imshow('Camera', frame_image)

            if cv.waitKey(1) == ord("s"):
                captureUnknownFace(image_copy)
                del image_copy

    cv.imshow('Camera', frame_image)
    if cv.waitKey(1) == ord("q"):
        break

print('Face recognition is stopped.')
camera.release()
cv.destroyAllWindows()
