from config import *
from model.data.BaseData import *

class Camera(BaseData):
    __tablename__ = 'camera'
    
    route = Column(String, unique=True)
    name = Column(String, unique=False)
    connected = Column(Boolean, unique=False)
    fireIsDetected = Column(Boolean, unique=False)
    
    group_id = Column(Integer, ForeignKey('group.id', ondelete="CASCADE"), nullable=True)
    
    def __init__(self, route, name, id=None):
        super().__init__(id)
        self.route = route
        self.name = name
        self.connected = False
        self.fireIsDetected = False