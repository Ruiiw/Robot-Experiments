import numpy
import constants
import pyrosim.pyrosim as pyrosim
import pybullet as p
import time

class MOTOR:

    def __init__(self, jointName):
        self.jointName = jointName

    def Set_Value(self, robotId, desiredAngles):
        pyrosim.Set_Motor_For_Joint(
        bodyIndex = robotId,
        jointName = self.jointName,
        controlMode = p.POSITION_CONTROL,
        targetPosition = desiredAngles,
        maxForce = 70)
