import pybullet as p

class WORLD:

    def __init__(self, physicsClient):
        
        self.planeId = p.loadURDF("plane.urdf")
        # self.robotId = p.loadURDF("body.urdf")
        