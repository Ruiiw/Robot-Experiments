import pybullet as p
import pyrosim.pyrosim as pyrosim
from sensor import SENSOR
from motor import MOTOR
from pyrosim.neuralNetwork import NEURAL_NETWORK
import os
import constants as c
import numpy as np

class ROBOT:

    def __init__(self, solutionID):
        self.solutionID = solutionID
        self.motors = dict()
        self.robotId = p.loadURDF("body" + str(self.solutionID) + ".urdf")
        pyrosim.Prepare_To_Simulate(self.robotId)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
        self.nn = NEURAL_NETWORK("brain" + str(self.solutionID) + ".nndf")
        # os.system("rm brain" + str(self.solutionID) + ".nndf")
        # os.system("rm body" + str(self.solutionID) + ".urdf")


    def Prepare_To_Sense(self):
        self.sensors = dict()
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)

    def Sense(self, i):
        for sensor in self.sensors:
            self.sensors[sensor].Get_Value(i)

    def Prepare_To_Act(self):
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)
        
    def Act(self, i):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName) * c.motorJointRange
                self.motors[jointName].Set_Value(self.robotId, desiredAngle)
                
    def Think(self):
        self.nn.Update()

    def Get_Fitness(self):
        basePositionAndOrientation = p.getBasePositionAndOrientation(self.robotId)
        basePosition = basePositionAndOrientation[0]
        xPosition = basePosition[0]
        yPosition = basePosition[1]
        dist = np.sqrt(xPosition**2 + yPosition**2)
        f = open("tmp" + str(self.solutionID) + ".txt", "w")
        f.write(str(dist))
        f.close()
        os.system("mv tmp" + str(self.solutionID) + ".txt fitness" + str(self.solutionID) + ".txt")
        