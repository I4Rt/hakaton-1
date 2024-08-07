from datetime import datetime
from flask import request, json, jsonify, make_response, Response, render_template,redirect
from config import *

from model.data import *


@app.route('/', methods=['GET', 'POST', 'OPTIONS'])
def redirectMain(): 
    return redirect('/main')


@app.route('/main', methods=['get'])
@cross_origin()
def main():
    return render_template('main.html', camera_list = [{'cam_id': cam.id, 'route': cam.route, 'name': cam.name, 'status': cam.fireIsDetected} for cam in Camera.getAll()], room_list=[gr.get_info() for gr in Group.getAll()])

@app.route('/addCameraPage', methods=['GET'])
def get_add_camera_page(): 
    return render_template('add_camera.html')

@app.route('/addGroupPage', methods=['GET'])
def get_add_group_page(): 
    return render_template('add_sector.html')

@app.route('/cameraPage', methods=['GET'])
def get_camera(): 
    id = int(request.args['id'])
    return render_template('camera_page.html', camera=Camera.getByID(id))

@app.route('/groupPage', methods=['GET'])
def get_room(): 
    id = int(request.args['id'])
    return render_template('group_page.html', camera_list = [{'cam_id': cam.id, 'route': cam.route, 'name': cam.name, 'status': cam.fireIsDetected} for cam in Camera.getAll()], room_info=Group.getByID(id).get_info())