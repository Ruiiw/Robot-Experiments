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
        self.numLinks = random.randint(3, 8)
        self.numJoints = self.numLinks -1

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
        hasSensor = [False] * self.numLinks
        for i in range(self.numLinks):
            if random.random() > 0.5:
                hasSensor[i] = True
        
        for i in range(self.numLinks):
            linkSize = [random.random(), random.random(), random.random()]
            pyrosim.Send_Cube(
                size = linkSize
            )
        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")
       
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