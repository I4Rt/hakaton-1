from config import *
from model.data.BaseData import *
from model.tools.DBSessionMaker import *
from model.data.Camera import Camera

class Group(BaseData):
    __tablename__ = 'group'
    name = Column(String, unique=False)
    cameras = relationship('Camera', cascade="all,delete", backref='target', lazy='select')
    
    def __init__(self, name, id=None):
        super().__init__(id)
        self.name = name
        
    
    def get_cameras(self):
        with DBSessionMaker.getSession() as ses:
            res = ses.query(Camera).filter(Camera.group_id == self.id).order_by(desc(Camera.id)).all()
        return res
    
    def get_info(self):
        cams = self.get_cameras()
        return {'group_id': self.id,
                'name': self.name,
                'cameras': [{'cam_id': cam.id, 'route': cam.route, 'name':cam.name, 'status': cam.fireIsDetected} for cam in cams]}