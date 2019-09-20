import os
import cv2
import dlib
import time
import numpy as np

face_detector = dlib.get_frontal_face_detector()
font = cv2.FONT_HERSHEY_SIMPLEX

def save_img(name, dataset_path, num_images=200):
    
    train_path = dataset_path + "\\train"
    test_path = dataset_path + "\\test"
    
    if not os.path.exists(train_path + "\\" + name):
        os.mkdir(train_path + "\\" + name)
        
    if not os.path.exists(test_path + "\\" + name):
        os.mkdir(test_path + "\\" + name)
        
    num_train_images = len(os.listdir(train_path + "\\" + name))
    num_test_images = len(os.listdir(test_path + "\\" + name))
    
    cam = cv2.VideoCapture(0)
    
    time.sleep(2)
    
    while num_train_images != num_images:
        ret, frame = cam.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detector(gray, 1)
    
        for face_rect in faces:
            x, y, w, h = face_rect.left(), face_rect.top(), face_rect.right(), face_rect.bottom()
            roi = frame[y:h, x:w]
            
            if num_train_images % 25 == 0:
                cv2.imwrite(test_path + "\\" + name + "\\" + str(num_test_images) + '.jpg', roi)
                num_test_images = num_test_images + 1
            else:
                cv2.imwrite(train_path + "\\" + name + "\\" + str(num_train_images) + '.jpg', roi)
            
            num_train_images = num_train_images + 1
            
            cv2.rectangle(frame,(x, y),(w, h),(0,255,0),2)
            txt = str(num_train_images) + " frames captured"
            cv2.putText(frame,txt,(x-10,y-10), font, 1, (0,0,255), 1, cv2.LINE_AA)
            
            print('{0} frames captured\r'.format(num_train_images), end = '')
    
        cv2.imshow('frame', frame)
        
        if cv2.waitKey(1) == ord('q'):
            break
    
    cam.release()
    cv2.destroyAllWindows()