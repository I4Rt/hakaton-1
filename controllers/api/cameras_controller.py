from flask import jsonify, render_template, flash, redirect, url_for, make_response, Response, request
from config import *

import json

import cv2
from time import time

from model.tools.streamer_tools.StreamInterface import StreamInterface

from datetime import datetime
from random import randint
from model.tools.FileUtil import *

from model.tools.streamer_tools.LastTimeRunnerHolder import LastTimeRunnerHolder as ltrh


@cross_origin
@app.route('/getFrame')
def getFrame():
    ltrh.setLastTime(datetime.now())
    print('outside: ', ltrh.getTimeInterval())
    try:
        route = request.args.get('route')
    except:
        return json.dumps({"frame":None, 'answer': 'Add params correctly'})
    try:
        frame = StreamInterface.getFrame(route)
        print('type of frame is', type(frame) )   
        imgBytes = FileUtil.convertImageToBytes(frame)
        return json.dumps({"route": route, "frame": imgBytes})
    except Exception as e:
        print('get framer error in controller ', e)
        return json.dumps({"route": route, "frame": None})

                    
    
@cross_origin
@app.route('/refreshVideo')
def refreshVideo():
    ltrh.setLastTime(datetime.now())
    try:
        route = str(request.args.get('route'))
        result = StreamInterface.refreshStream(route)
        return json.dumps({'refresh': result})
    except:
        return json.dumps({'refresh': False, 'answer': 'Add params correctly'})

@cross_origin
@app.route('/initVideo')
def initVideo():
    print('init request')
    ltrh.setLastTime(datetime.now())
    try:
        b = time()
        route = request.args.get('route')
        StreamInterface.initStream(str(route))
    except Exception as e:
        print('Exception here is ' + str(e))
        print('work t', time() - b)
        return json.dumps({'init': False, 'answer':'Add params correctly'})
    print('work t', time() - b)
    return json.dumps({'init': True})
    
