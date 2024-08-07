from flask import jsonify, render_template, flash, redirect, url_for, make_response, Response, request
from config import *
from controllers.wrapler import *
from model.data import *



@cross_origin
@app.route('/addCamera', methods=['POST']) 
@exception_processing
def add_camera():
    print('here')
    route = str(request.json['route'])
    name = request.json['name']
    
    camera = Camera(route, name)
    camera.save()
    return {request.path: True}

@cross_origin
@app.route('/getCameras', methods=['GET'])
@exception_processing
def get_cameras():
    cameras = Camera.getAll()
    return {request.path: True, 'answer': {'camera_list': [{'cam_id': cam.id, 'route': cam.route} for cam in cameras]}}


@cross_origin
@app.route('/addGroup', methods=['POST'])
@exception_processing
def add_group():
    route = request.json['name']
    gr = Group(route)
    gr.save()
    return {request.path: True}

@cross_origin
@app.route('/getGroups', methods=['GET'])
@exception_processing
def get_groups():
    gr_list:list[Group] = Group.getAll()
    res = []
    for gr in gr_list:
        res.append(gr.get_info())
    return {request.path: True, 'answer': {'group_list': res}}

@cross_origin
@app.route('/addCameraToGroup', methods=['POST'])
@exception_processing
def add_camera_to_group():
    cam_id = request.json['cam_id']
    group_id = request.json['group_id']
    cam = Camera.getByID(cam_id)
    cam.group_id = group_id
    cam.save()
    return {request.path: True}

@cross_origin
@app.route('/separateCamera', methods=['POST'])
@exception_processing
def separate_camera():
    cam_id = request.json['cam_id']
    cam = Camera.getByID(cam_id)
    cam.group_id = None
    cam.save()
    return {request.path: True}


    
    
    