import os, sys
import cv2
from context import eye_detector
from context import data


def getImagePath(_class, name):
    assert _class in ['open', 'close']
    return os.path.abspath(os.path.join(
            os.path.dirname(__file__), 
            '..', 
            'data', 
            'open_eyes' if _class=='open' else 'closed_eyes',
            '{}.jpg'.format(name)
            ))


def test_difference_from_images():
    img1 = cv2.imread(getImagePath('open', 8))
    img2 = cv2.imread(getImagePath('close', 7))
    diff = eye_detector.eye_ratio_difference(img1, img2)
    print(diff**2)


def test_eye_state():
    open_eyes = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    closed_eyes = ['1', '2', '3', '4', '5', '6', '7', '8']
    result = {}

    for file_name in open_eyes:
        img = cv2.imread(getImagePath('open', file_name))
        try:
            eye_state = eye_detector.get_avg_eye_state(img)
            result['open_{}'.format(file_name)] = eye_state
        except: 
            print("open_{} has no face".format(file_name))

    for file_name in closed_eyes:
        img = cv2.imread(getImagePath('close', file_name))
        try:
            eye_state = eye_detector.get_avg_eye_state(img)
            result['closed_{}'.format(file_name)] = eye_state
        except: 
            print("closed_{} has no face".format(file_name))

    for name, eye_state in result.items():
        print('{} is {}'.format(name, 'opened' if eye_state==1 else 'closed' if eye_state==0 else 'undefined'))

    # img = cv2.imread(getImagePath('open', 8))
    # eye_state = eye_detector.get_avg_eye_state(img)
    # print('eye is {}'.format('opened' if eye_state==1 else 'closed'))


if __name__ == '__main__':
    test_eye_state()
    test_difference_from_images()
