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
        # random number of sensors
        hasSensor = [False] * self.numLinks
        for i in range(self.numLinks):
            if random.random() > 0.5:
                hasSensor[i] = True
        
        # crete first link
        linkS = [random.uniform(0.2, 1), random.uniform(0.2, 1), random.uniform(0.2, 1)]

        pyrosim.Send_Cube(name = "Link0", pos = [0, 0, linkS[2]/2], size = linkS)
        pyrosim.Send_Joint(
            name = "Link0_Link1", 
            parent = "Link0", 
            child = "Link1", 
            type = "revolute", 
            position = [linkS[0]/2, 0, linkS[2]/2], 
            jointAxis = "0 1 0")


        for i in range(1, self.numLinks):
            # create other links
            linkSize = [random.uniform(0.2, 1), random.uniform(0.2, 1), random.uniform(0.2, 1)]
            pyrosim.Send_Cube(name = "Link" + str(i), pos = [linkSize[0]/2, 0, 0], size = linkSize)

            # create joints
            if i != self.numLinks - 1:
                pyrosim.Send_Joint(
                    name = "Link" + str(i) + "_Link" + str(i+1),
                    parent = "Link" + str(i),
                    child = "Link" + str(i+1),
                    type = "revolute",
                    position = [linkSize[0], 0, 0],
                    jointAxis = "0 1 0")
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