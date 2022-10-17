import cv2 as cv
import face_recognition

imgElon = face_recognition.load_image_file('faces/Elon Musk.png')
imgElon = cv.resize(imgElon, (int(imgElon.shape[1]//2), int(imgElon.shape[0])//2), interpolation=cv.INTER_LINEAR)
imgElon = cv.cvtColor(imgElon, cv.COLOR_BGR2RGB)

imgTest = face_recognition.load_image_file('faces/Elon Musk2.png')
imgTest = cv.resize(imgTest, (int(imgTest.shape[1]//2), int(imgTest.shape[0])//2), interpolation=cv.INTER_LINEAR)
imgTest = cv.cvtColor(imgTest, cv.COLOR_BGR2RGB)

facelocation = face_recognition.face_locations(imgElon)[0]
encode_elon = face_recognition.face_encodings(imgElon)[0]
cv.rectangle(imgElon, (facelocation[3], facelocation[0]), (facelocation[1], facelocation[2]), (0, 255, 0), thickness=3)

test_face_location = face_recognition.face_locations(imgTest)[0]
encode_test_image = face_recognition.face_encodings(imgTest)[0]
cv.rectangle(imgTest, (test_face_location[3], test_face_location[0]), (test_face_location[1], test_face_location[2]), (0, 255, 0), thickness=3)

recognized = face_recognition.compare_faces([encode_elon], encode_test_image)
face_difference = face_recognition.face_distance([encode_elon], encode_test_image)
print(recognized)
print("Face difference is: ", face_difference)

cv.putText(imgTest, f'{recognized} {round(face_difference[0], 2)}', (10, 20), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
cv.imshow('Elon musk', imgElon)
cv.imshow('Elon musk test image', imgTest)

cv.waitKey(0)