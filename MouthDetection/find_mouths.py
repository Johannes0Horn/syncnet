import numpy as np
import os
import imutils
import dlib
import cv2
import imageio
from imutils import face_utils
import matplotlib.pyplot as plt
from IPython.display import Video
import random
import librosa
from moviepy.editor import *
from pytube import YouTube
from bs4 import BeautifulSoup
import json

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

def rect_to_bb(rect):
    # take a bounding predicted by dlib and convert it
    # to the format (x, y, w, h) as we would normally do
    # with OpenCV
    x = rect.left()
    y = rect.top()
    w = rect.right() - x
    h = rect.bottom() - y

    # return a tuple of (x, y, w, h)
    return (x, y, w, h)

def shape_to_np(shape, dtype="int"):
    # initialize the list of (x, y)-coordinates
    coords = np.zeros((68, 2), dtype=dtype)

    # loop over the 68 facial landmarks and convert them
    # to a 2-tuple of (x, y)-coordinates
    for i in range(0, 68):
        coords[i] = (shape.part(i).x, shape.part(i).y)

    # return the list of (x, y)-coordinates
    return coords

def find_mouths_in_video(video_path):
    cap = cv2.VideoCapture(video_path)
    mouths = dict()
    frame_count = -1
    while(cap.isOpened()):
        ret, img = cap.read()
        if ret == True:
            frame_count += 1
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            orig_width = img.shape[1]
            resize_ratio = orig_width / 500
            img = imutils.resize(img, width=500)
            rects = detector(img, 1)
            if len(rects) != 1:
                continue
            rect = rects[0]
            shape = predictor(img, rect)
            shape = shape_to_np(shape)
            xywh = list(cv2.boundingRect(np.array([shape[48:68]])))
            mouths[frame_count] = [int(x * resize_ratio) for x in xywh]
        else:
            break
    cap.release()
    return mouths

##########################################################################################

for i,filename in enumerate(os.listdir("../DATA/videos")):
    annname = filename.split(".mp4")[0] + ".json"
    if os.path.isfile("../DATA/ann/" + annname):
        continue
    print("################################\nWORKING ON " + filename + "("+str(i)+"/"+str(len(os.listdir("../DATA/videos")))+")")
    mouths = find_mouths_in_video("../DATA/videos/" + filename)
    with open('../DATA/ann/'+annname, 'w') as f:
        json.dump(mouths, f)