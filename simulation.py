from world import WORLD
from robot import ROBOT
import pybullet as p
import pybullet_data
import time
from robot import ROBOT
from sensor import SENSOR

class SIMULATION:

    def __init__(self):

        self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0,0,-9.8)
        self.world = WORLD()
        self.robot = ROBOT()

    def __del__(self):
        p.disconnect()

    def run(self):
        for i in range(1000):
            p.stepSimulation()
            self.robot.Sense(i)
            self.robot.Think()
            self.robot.Act(i)
            time.sleep(1/1000)

    def Get_Fitness(self):
        self.robot.Get_Fitness()