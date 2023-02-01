import numpy
import pyrosim.pyrosim as pyrosim
import random
import os
import time
import constants as c

class SOLUTION:

    def __init__(self, nextAvailableID):
        self.weights = numpy.random.rand(c.numSensorneurons, c.numMotorneurons) * 2 -1
        self.myID = nextAvailableID


    # def Evaluate(self, directOrGUI):
    #     self.Create_World()
    #     self.Create_Body()
    #     self.Create_Brain()
    #     os.system("python3 simulate.py" + directOrGUI + " " + str(self.myID) + " &")
    #     while not os.path.exists("fitness" + str(self.myID) + ".txt"):
    #         time.sleep(0.01)
    #     f = open("fitness" + str(self.myID) + ".txt", "r")
    #     self.fitness = float(f.read())
    #     print(self.fitness)
    #     f.close()

    def Start_Simulation(self, directOrGUI):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        os.system("python3 simulate.py" + directOrGUI + " " + str(self.myID) + " &")

    def Wait_For_Simulation_To_End(self):
        while not os.path.exists("fitness" + str(self.myID) + ".txt"):
            time.sleep(0.01)
        f = open("fitness" + str(self.myID) + ".txt", "r")
        fitVal = f.read()
        self.fitness = float(fitVal)
        f.close()
        os.system("rm fitness" + str(self.myID) + ".txt")

    def Create_World(self):
        pyrosim.Start_URDF("box.urdf")
        pyrosim.Send_Cube(name="box", pos=[-20, 20, 0.5] , size=[1, 1, 1])
        pyrosim.End()

    def Create_Body(self):
        pyrosim.Start_URDF("body.urdf")
        length = 1
        width = 1
        height = 1
        pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1] , size=[length, width, height])
        pyrosim.Send_Joint(name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [0, -0.5, 1], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="BackLeg", pos=[0, -0.5, 0] , size=[0.2, 1, 0.2])
        pyrosim.Send_Joint(name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [0, 0.5, 1], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="FrontLeg", pos=[0, 0.5, 0] , size=[0.2, 1, 0.2])
        pyrosim.Send_Joint(name = "Torso_LeftLeg" , parent= "Torso" , child = "LeftLeg" , type = "revolute", position = [-0.5, 0, 1], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="LeftLeg", pos=[-0.5, 0, 0] , size=[1, 0.2, 0.2])
        pyrosim.Send_Joint(name = "Torso_RightLeg" , parent= "Torso" , child = "RightLeg" , type = "revolute", position = [0.5, 0, 1], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="RightLeg", pos=[0.5, 0, 0] , size=[1, 0.2, 0.2])
        
        pyrosim.Send_Joint(name = "BackLeg_LowerBackLeg" , parent= "BackLeg" , child = "LowerBackLeg" , type = "revolute", position = [0, -1, 0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="LowerBackLeg", pos=[0, 0, -0.5] , size=[0.2, 0.2, 1])
        pyrosim.Send_Joint(name = "FrontLeg_LowerFrontLeg" , parent= "FrontLeg" , child = "LowerFrontLeg" , type = "revolute", position = [0, 1, 0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="LowerFrontLeg", pos=[0, 0, -0.5] , size=[0.2, 0.2, 1])
        pyrosim.Send_Joint(name = "LeftLeg_LowerLeftLeg" , parent= "LeftLeg" , child = "LowerLeftLeg" , type = "revolute", position = [-1, 0, 0], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="LowerLeftLeg", pos=[0, 0, -0.5] , size=[0.2, 0.2, 1])
        pyrosim.Send_Joint(name = "RightLeg_LowerRightLeg" , parent= "RightLeg" , child = "LowerRightLeg" , type = "revolute", position = [1, 0, 0], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="LowerRightLeg", pos=[0, 0, -0.5] , size=[0.2, 0.2, 1])
        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")
        # pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
        # pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "BackLeg")
        # pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "FrontLeg")
        # pyrosim.Send_Sensor_Neuron(name = 3 , linkName = "LeftLeg")
        # pyrosim.Send_Sensor_Neuron(name = 4 , linkName = "RightLeg")
        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "LowerBackLeg")
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "LowerFrontLeg")
        pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "LowerLeftLeg")
        pyrosim.Send_Sensor_Neuron(name = 3 , linkName = "LowerRightLeg")

        pyrosim.Send_Motor_Neuron( name = 4 , jointName = "Torso_BackLeg")
        pyrosim.Send_Motor_Neuron( name = 5 , jointName = "Torso_FrontLeg")
        pyrosim.Send_Motor_Neuron( name = 6 , jointName = "Torso_LeftLeg")
        pyrosim.Send_Motor_Neuron( name = 7 , jointName = "Torso_RightLeg")
        pyrosim.Send_Motor_Neuron( name = 8 , jointName = "BackLeg_LowerBackLeg")
        pyrosim.Send_Motor_Neuron( name = 9 , jointName = "FrontLeg_LowerFrontLeg")
        pyrosim.Send_Motor_Neuron( name = 10 , jointName = "LeftLeg_LowerLeftLeg")
        pyrosim.Send_Motor_Neuron( name = 11 , jointName = "RightLeg_LowerRightLeg")
        for currentRow in range(c.numSensorneurons):
            for currentColumn in range(c.numMotorneurons):
                pyrosim.Send_Synapse(sourceNeuronName = currentRow , targetNeuronName = currentColumn + c.numSensorneurons , weight = self.weights[currentRow][currentColumn])
        pyrosim.End()

    def Mutate(self):
        randomRow = random.randint(0, c.numSensorneurons-1)
        randomCol = random.randint(0, c.numMotorneurons-1)
        self.weights[randomRow,randomCol] = random.random()*2 -1

    def Set_ID(self, id):
        self.myID = id