import numpy as np
import cv2
import dlib
from utils import load_face_landmark_model, load_fr_model, load_embeddings_model, load_face_detector, load_inv_label_dictionary
from collections import Counter
import RPi.GPIO as GPIO 
import time

face_landmarks_model = load_face_landmark_model()
fr_model = load_fr_model()
face_detector = load_face_detector()
font = cv2.FONT_HERSHEY_SIMPLEX
svm = load_embeddings_model(model='svm')
inv_label_dictionary = load_inv_label_dictionary()

no_frames = 20

print("Model Loaded")
print()


def predict_face(rgb, dlib_box):
    pose = face_landmarks_model(rgb, dlib_box)
    embedding = np.array(fr_model.compute_face_descriptor(rgb, pose, 1))
    name = svm.predict_proba([embedding])[0]

    max_arg = name.argmax()

    if name[max_arg] > 0.96:
        label = inv_label_dictionary[max_arg]
        probab = round(name[max_arg]*100, 2)
    else:
        label = "Others"
        probab = 0.95
    
    return label, probab


def recognize_faces(gray, rgb):
    prediction = []
    probability = []
    
    try:
        faces = face_detector(gray, 1)
        for face_rect in faces:
            x, y, w, h = face_rect.left(), face_rect.top(), face_rect.right(), face_rect.bottom()

            dlib_box = dlib.rectangle(x, y, w, h)
            roi = gray[y:h, x:w]

            face_prediction, face_probab = predict_face(rgb, dlib_box)
            prediction.append(face_prediction)
            probability.append((face_probab))
    
    except Exception as e:
        pass
        
    return prediction, probability


def unlock(name):
    print("Unlocked")
    print(name)
    print()


while True:
    inp = input()
    if inp == 'c':
        try:
            cam = cv2.VideoCapture(0)
            face_predictions = []
            face_probab = []
            frame_pipeline = []

            ret, img = cam.read()

            while(len(frame_pipeline) < no_frames):
                frame_pipeline.append(img)

            print("Frames Captured")
            cam.release()
            for img in frame_pipeline:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                pred, probab = recognize_faces(gray, rgb)
                for i in range(len(pred)):
                    face_predictions.append(pred[i])
                    face_probab.append(probab[i])


            print(face_predictions)
            counter_dict = Counter(face_predictions)
            keys, values = list(counter_dict.keys()), list(counter_dict.values())
            max_value = max(values)
            max_value_index = values.index(max_value)
            max_pred = keys[max_value_index]

            tot_prob = 0
            for i in range(len(face_predictions)):
                if face_predictions[i] == max_pred:
                    tot_prob = tot_prob + face_probab[i]


            if tot_prob > max_value * 0.95:
                unlock(max_pred)
            else:
                print("Try Again")
                print()

            cam.release()
        except Exception as e:
            print(e)
            print("Try Again")
            print()

