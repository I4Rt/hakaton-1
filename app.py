from config import *

from model.data.Camera import *
from model.data.Group import *
from model.tools.streamer_tools.PermanentStreamer import *
from model.tools.detecting import *
from model.controls.detector import *

from controllers import *
# from controllers.pages import *



if __name__ == "__main__":
    print('App is running')
    with app.app_context():
        detector = StopableThread(target=check, looped=True, loop_interval=1)
        detector.start()
        
        sender = StopableThread(target=sendFire, looped=True, loop_interval=1)
        sender.start()
        Base.metadata.create_all(e)
        PermanentStreamer.init() # decoment!
        app.run(host='0.0.0.0', port=5000, debug=True)
        