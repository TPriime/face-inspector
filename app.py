#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 08:49:34 2021

@author: prime
"""

import traceback, logging
from flask import Flask, request, jsonify
from flask_cors import cross_origin
from faceinspector.classifiers import eye_detector
from faceinspector import helpers

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

      
@app.route('/', methods=['POST'])
@cross_origin()
def get_eye_status():  
    try:
        data = request.get_json() 
        app.logger.debug('{} images'.format(len(data['images'])))  
        images = data['images'] 
        if(len(images)>2): images = images[1:] 
        states = [] 

        #convert to cv2 image
        for i, img in enumerate(images): 
            images[i] = helpers.data_uri_to_cv2_img(img) 

        for index, img in enumerate(images): 
            result = eye_detector.get_avg_eye_state(img, 3.4)
            states.append(result) 

        eye_difference = eye_detector.eye_ratio_difference(images[0], images[len(images)-1])

        app.logger.debug("states: {}".format(states))
        app.logger.debug("difference: {}".format(eye_difference**2)) 

        return jsonify(
            status = True,
            states = states,
            match_score = 91.4, 
            liveness = helpers.liveness(eye_difference),
            difference = eye_difference**2)

    except: 
        traceback.print_exc()
        return jsonify(status=False)


@app.route('/hello', methods=['GET'])
def hello_world():
    app.logger.info("args from hello -> {}".format(request.args.values))
    return 'Hello, World!'


if __name__ == "__main__":
   app.run(debug=True, port=5000)