from model.data.Camera import *
from model.data.Group import *

from model.tools.StopableThread import *
from model.tools.streamer_tools.StreamInterface import *

from model.tools.detecting import *

import time
import serial
import serial.tools.list_ports

def send_fire_uart():
    try:
        # ports = serial.tools.list_ports.comports()
        # port = next((p.device for p in ports), None)
        # if port is None:
        #     raise ValueError("No COM")
        
        # mySerial = serial.Serial(port, baudrate=9600, rtscts=False)
        mySerial = serial.Serial(port="COM5", baudrate=9600, rtscts=False)
        dataToSend = bytes.fromhex('FF')
        mySerial.setRTS(True)
        mySerial.write(dataToSend)

        mySerial.setRTS(False)


    except ValueError as ve:
        print("Error: ",str(ve))

    except serial.SerialException as se:
        print("Serial port error: ", str(se))

    except Exception as e:
        print("An error occurred: ", str(e))


def check():
    try:
        cam_list:list[Camera] = Camera.getAll()
        for cam in cam_list:
            sleep(1)
            try:
                res = StreamInterface.initStream(cam.route)
                if res:
                    frame = StreamInterface.getFrame(cam.route)
                    frame, classes_count = give_result(frame)
                    if classes_count > 0:
                        cam.fireIsDetected = True
                        cam.save()
                        print('\n\n\n\n\nDETECTED\n\n\n\n\n')
                    else:
                        cam.fireIsDetected = False
                        cam.save()
            except Exception as e:
                print(e)
                    
            
                
    except Exception as e:
        print('p2', e)
        
def sendFire():
    try:
        cam_list:list[Camera] = Camera.getAll()
        for cam in cam_list:
            try:
                if cam.fireIsDetected:
                    send_fire_uart() 
            except Exception as e:
                print(e)
    except Exception as e:
        print('p2', e)
