from model.tools.streamer_tools.PermanentStreamer import PermanentStreamer
from time import sleep, time
class StreamInterface:
    '''
    в случае попадания в интервал финиш - удаление, 
    производится принудительное закрытие и удаление стрима,
    далее создание нового
    '''
    
    @classmethod
    def initStream(cls, route, timeLimit = 120):
        res = PermanentStreamer.initStream(route)
        return bool(res)
        
    
        
    '''route будет приведен к строке'''
    @classmethod
    def getFrame(cls, route:str|int):
        return PermanentStreamer.getNext(route)

        
    @classmethod
    def refreshStream(cls, route:str):
        return PermanentStreamer.refreshStream(route)
    