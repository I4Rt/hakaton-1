from __future__ import annotations
from time import time, sleep
import cv2
import threading, multiprocessing
from model.tools.FileUtil import *
import config
import os
import sys
import signal
from datetime import datetime


from model.tools.Jsonifyer import Jsonifyer

from model.tools.StopableThread import StopableThread


class PermanentStreamer(Jsonifyer):
    
    # route : stream
    __streams:dict[str, Stream] = {}
    
    @classmethod
    def init(cls):
        cls.__thread = StopableThread(target=cls.releaseQueues, looped=True, loop_interval=1)
        cls.__thread.start()
        
        
    @classmethod
    def checkCreated(cls, ident):
        for res in list(cls.__streams.keys()):
            if res == ident:
                return True
        return None
    
    
    @classmethod
    def releaseQueues(cls):
        # print('release')
        try:
            for key in cls.__streams:
                # print(key, (datetime.now() - cls.__streams[key].get_refreshed_connection_time()).total_seconds() ,(datetime.now() - cls.__streams[key].get_refreshed_connection_time()).total_seconds() > 20)
                if (datetime.now() - cls.__streams[key].get_refreshed_connection_time()).total_seconds() > 20:
                    try:
                        cls.__streams[key]._release()
                    except:
                        print('release error')
                    del cls.__streams[key]
        except Exception as e:
            print(e)
        
        # try:
        #     id, route = list(cls.__queue.pop(0).items())[0] # [id, route]
        #     res = cls.initStream(route)
        #     cls.__readyStreamsList.append([id, res])
        #     cls.__readyStreamsList = cls.__readyStreamsList[-400:]
        # except IndexError:
        #     pass
        # except Exception as e:
        #     print('releasing queue error:', e)
        # finally:
        #     sleep(0.2)
       
    
    # must be single executed  (from queue only)
    @classmethod
    def initStream(cls, route):
        route = str(route)
        if str(route) in list(cls.__streams.keys()):
            if (datetime.now() - cls.__streams[str(route)].get_refreshed_connection_time()).total_seconds() < 20:
                cls.refreshStream(route)
                return True
            else:
                try:
                    print('on create release')
                    cls.__streams[str(route)]._release()
                except:
                    print('on create release error')
                    pass
                del cls.__streams[str(route)]

        stream = Stream(str(route))
        res = stream.init()
        print('init stream result', res)
        if res:
            cls.__streams[route] = stream
            return True
        try:
            print('releasing n bad init')
            stream._release()
        except:
            pass
        return False
        
    @classmethod
    def getNext(cls, route):
        try:
            if str(route) in list(cls.__streams.keys()):
                if (datetime.now() - cls.__streams[str(route)].get_refreshed_connection_time()).total_seconds() < 20:
                    return next(cls.__streams[str(route)].getStream())
                print('\n\ntimeout\n\n')
            print('\n\nroute_not_found\n\n')
            return None
        except:
            print('can not get frame from generator exception')
            return None
        
            
        
    @classmethod
    def refreshStream(cls, route):
        print(cls.__streams)
        if str(route) in list(cls.__streams.keys()):
            if (datetime.now() - cls.__streams[str(route)].get_refreshed_connection_time()).total_seconds() < 19.5:
                cls.__streams[str(route)].update_refreshed_connection_time()
                return True
        return False
        
        

class Stream(Jsonifyer):
    
    __camRoute:str|int = 0
    _streaming:cv2.VideoCapture | None = None

    def __init__(self, route:str):
        Jsonifyer.__init__(self)
        # print('initing: adding ' + str(self.__timeLimit) + 'more seconds')
        # BAD routing
        if type(route) == str:
            if route.isdigit():
                route = int(route)
        self.__camRoute = route
        self.__generator = None
        self.__lastTime = None
        self._image = None
        self.__refreshed_connection_time = datetime.now()
        
        self.getterThread = None
        # self.init()                           # TODO: check it
    
    def update_refreshed_connection_time(self):
        self.__refreshed_connection_time = datetime.now()
    
    def get_refreshed_connection_time(self):
        return self.__refreshed_connection_time
    
    def getTimeSinceUpdateFrom(self):
        if self.__lastTime:
            return (datetime.now() - self.__lastTime).total_seconds()
        return -1
    
    
        
    def init(self):
        try:
            self._connect()
        except:
            return False
        self.getterThread = StopableThread(target=self.__updateFrame, looped=True)
        self.getterThread.start()
        sleep(0.5)
        self.__generator = self.__getFrames()
        return True
    
    def _connect(self):
        try:
            if self._streaming == None:
                print('connecting', self.__camRoute)
                # print('ppid', os.getpid())
                self._streaming = cv2.VideoCapture(self.__camRoute)
        except Exception as e:
            try:
                self._release()
            except Exception as e:
                print('bad initing exception release:', e)
            raise Exception('Can not capture the video', type(e), e)
        
    '''добавить попытку получения первых кадров'''
    def __updateFrame(self):
        # while not self._checkDelete(): #TODO: test
        
        try:
            if self._streaming:
                result, frame = self._streaming.read()
                if result:
                    self.__lastTime = datetime.now()
                    self._image = frame
                    sleep(0.5)
                    return
            sleep(0.5)
            return
        except Exception as e:
            sleep(0.5)
            print('test', e)
            
            
    def __getFrames(self):
        if self._streaming == None:
            raise Exception('First try to connect the camera')
        print(f'return {self.__camRoute}')
        while True:                                                # check it
            try:
                if self._image is None:
                    # print('image is none')
                    yield None
                else:
                    # print('image exist', self._image)
                    yield self._image
            except Exception as e:
                raise e    
                 
    def getStream(self):
        return self.__generator
        
    def _release(self):
        # print('releasing')
        
        try:
            self.getterThread.stop()
            sleep(1)
            try:
                self.getterThread.join()
            except Exception as e:
                print('r1', e)
            sleep(0.5)
            del self.getterThread
            print('thread deleted')
        except Exception as e:
            print('release delete thread exception', e)
        try:
            del self._image
            print('image deleted')
        except Exception as e:
            print('release delete image exception', e)
        try:
            self._streaming.release()
            del self._streaming
        except Exception as e:
            print('releasing streaming exception', e)
            
    def __del__(self):
        try:
            self._release()
        except: 
            pass
        print("deleted stream object", self.getId())