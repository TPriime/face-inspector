#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 16:56:10 2021

@author: prime
"""

import cv2, dlib, math
import logging, traceback
import os, sys

BLINK_RATIO_THRESHOLD = 3.35 #5.7

logger = logging.getLogger()
landmarks_file = os.path.join(os.path.dirname(__file__), '..', 'assets', 'shape_predictor_68_face_landmarks.dat')

face_detector = dlib.get_frontal_face_detector()

def midpoint(point1 ,point2):
    return (point1.x + point2.x)/2,(point1.y + point2.y)/2

def euclidean_distance(point1 , point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)


def get_blink_ratio(eye_points, facial_landmarks):
    #loading all the required points
    corner_left  = (facial_landmarks.part(eye_points[0]).x, 
                    facial_landmarks.part(eye_points[0]).y)
    corner_right = (facial_landmarks.part(eye_points[3]).x, 
                    facial_landmarks.part(eye_points[3]).y)
    
    center_top    = midpoint(facial_landmarks.part(eye_points[1]), 
                             facial_landmarks.part(eye_points[2]))
    center_bottom = midpoint(facial_landmarks.part(eye_points[5]), 
                             facial_landmarks.part(eye_points[4]))

    #calculating distance
    horizontal_length = euclidean_distance(corner_left,corner_right)
    vertical_length = euclidean_distance(center_top,center_bottom)

    ratio = horizontal_length / vertical_length

    return ratio


"""
@retrun None on error
"""
def get_avg_eye_ratio(img):
    # detect eyes using landmarks in dlib
    shape_predictor = dlib.shape_predictor(landmarks_file)
    left_eye_landmarks  = [36, 37, 38, 39, 40, 41]
    right_eye_landmarks = [42, 43, 44, 45, 46, 47]

    #-----Step 2: converting image to grayscale-----
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #-----Step 3: Face detection with dlib-----
    #detecting faces in the frame 
    faces,_,_ = face_detector.run(image = img_gray, upsample_num_times = 0, adjust_threshold = 0.0)

    for face in faces:
        # detect eyes
        landmarks = shape_predictor(img_gray, face)

        # calculating average blink ratio for both eyes
        left_eye_ratio  = get_blink_ratio(left_eye_landmarks, landmarks)
        right_eye_ratio = get_blink_ratio(right_eye_landmarks, landmarks)
        avg_eye_ratio     = (left_eye_ratio + right_eye_ratio) / 2
        logger.debug("left_ratio: {}, right_ratio: {}".format(left_eye_ratio, right_eye_ratio))

        return (avg_eye_ratio, left_eye_ratio, right_eye_ratio)
    
    # return None if no face is found
    return None
    

'''
    @return 0 on error
'''
def eye_ratio_difference(img1, img2):
    try:
        return abs(get_avg_eye_ratio(img1)[0] - get_avg_eye_ratio(img2)[0])
    except:
        traceback.print_exc()
        return 0

def get_avg_eye_state(img, blinkRatioThreshold=BLINK_RATIO_THRESHOLD):
    try:
        avg_blink_ratio = get_avg_eye_ratio(img)[0]

        if avg_blink_ratio > blinkRatioThreshold:
            return 0
        else: return 1
    except:
        traceback.print_exc()
        return -1