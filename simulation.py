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
        self.world = WORLD(self.physicsClient)
        self.robot = ROBOT()

    def __del__(self):
        p.disconnect()

    def run(self):
        for i in range(1000):
            print(i)
            p.stepSimulation()
            self.robot.Sense(i)
            time.sleep(1/240)
            # pyrosim.Set_Motor_For_Joint(
            # bodyIndex = robotId,
            # jointName = "Torso_BackLeg",
            # controlMode = p.POSITION_CONTROL,
            # #targetPosition = random.uniform(-numpy.pi/4, numpy.pi/4),
            # targetPosition = backLeg_targetAngles[i],
            # maxForce = 60)

            # pyrosim.Set_Motor_For_Joint(
            # bodyIndex = robotId,
            # jointName = "Torso_FrontLeg",
            # controlMode = p.POSITION_CONTROL,
            # #targetPosition = random.uniform(-numpy.pi/4, numpy.pi/4),
            # targetPosition = frontLeg_targetAngles[i],
            # maxForce = 60)
            # time.sleep(1/240)

