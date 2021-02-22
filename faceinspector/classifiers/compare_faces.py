#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 07:30:15 2021

@author: prime
"""

import requests

#GET Request
#r = requests.get('https://api.github.com/events')

#POST Request
#r = requests.post('http://httpbin.org/post', data = {
#        'key':'value',
#    })


def match(image1, image2):     
    # facePlusPlus = "https://api-us.faceplusplus.com/facepp/v3/compare"
    # params = {
    #     'image_base64_1', image1,
    #     'image_base64_2', image2#,
    #     #'api_key', "cgirJZT9-EnjJqck4Oh2UXdU-PutfP7s",
    #     #'api_secret', "RauT-QuBtAZHIL7foIPewy5s0wFCwM2w"
    # }
    # r = requests.post(facePlusPlus, data = params)
    # return r
    r = requests.post('http://httpbin.org/post', data = {
        'key':'value',
    })
    return r

