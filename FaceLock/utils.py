import pickle
import dlib
import keras
import os

cwd = os.getcwd()


def load_face_landmark_model():
    return dlib.shape_predictor(cwd+'/saved_models/face_landmarks_model.dat')

def load_fr_model():
    return dlib.face_recognition_model_v1(cwd+'/saved_models/fr_model.dat')

def load_face_detector():
    return dlib.get_frontal_face_detector()

def load_embeddings_model(model='svm'):
    if model == 'svm':
        return pickle.load(open(cwd+'/saved_models/svm_embeddings_model', 'rb'))
    else:
        return pickle.load(open(cwd+'/saved_models/knn_embeddings_model', 'rb'))
    
def load_embeddings():
    return pickle.load(open(cwd+'/database/saved_embeddings', 'rb'))

def load_inv_label_dictionary():
    return pickle.load(open(cwd+'/database/inv_embeddings_label_dict', 'rb'))
