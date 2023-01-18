import numpy
import constants
import pyrosim.pyrosim as pyrosim
import pybullet as p
import time

class MOTOR:

    def __init__(self, jointName):
        self.jointName = jointName
        self.Prepare_To_Act()

    def Prepare_To_Act(self):
        self.amplitude = constants.backLeg_amplitude
        if self.jointName == "Torso_BackLeg":
            self.frequency = constants.backLeg_frequency/2
        else:
            self.frequency = constants.backLeg_frequency
        self.offset = constants.backLeg_phaseOffset
        self.rad = numpy.linspace(0, 2*numpy.pi, 1000)
        self.motorValues = self.amplitude * numpy.sin(self.frequency * self.rad + self.offset)

    def Set_Value(self, robotId, i):
        pyrosim.Set_Motor_For_Joint(
        bodyIndex = robotId,
        jointName = self.jointName,
        controlMode = p.POSITION_CONTROL,
        targetPosition = self.motorValues[i],
        maxForce = 60)
        time.sleep(1/240)