import numpy
import pyrosim.pyrosim as pyrosim
import random
import os
import time
import constants as c

class SOLUTION:

    def __init__(self, nextAvailableID):
        self.myID = nextAvailableID
        self.numLinks = random.randint(3, 8)
        print("link num", self.numLinks)
        self.numJoints = self.numLinks -1

        # random number of sensors
        self.hasSensor = [False] * self.numLinks
        for i in range(self.numLinks):
            if random.random() > 0.5:
                self.hasSensor[i] = True

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

        # create first link
        linkS = [random.uniform(0.2, 1), random.uniform(0.2, 1), random.uniform(0.2, 1)]
        firstC = self.hasSensor[0]
        pyrosim.Send_Cube(name = "Link0", pos = [0, 0, linkS[2]/2], size = linkS, green=firstC)

        # dictionary for tracking every link's absolute position
        # key: link index; value: [(x min, x max), (y min, y max), (z min, z max)]
        linkPos = {}
        linkPos[0] = [-linkS[0]/2, linkS[0]/2, -linkS[1]/2, linkS[1]/2, 0, linkS[2]]

        # keeps track of all links' relative centers and positions
        LinkCenters = [[0, 0, linkS[2]/2]]
        LinkSizes = [linkS]

        for i in range(1, self.numLinks):
            print(i)
            # randomly choose a generated link and a face on it to add a joint
            faceDim = random.choice(["x", "y", "z"])
            faceDir = random.choice([-1, 1])
            randomLinkIdx = random.randint(0, len(LinkCenters)-1)
            print("random",randomLinkIdx)

            # width, length, height of the newly generated link
            linkW = random.uniform(0.2, 1)
            linkL = random.uniform(0.2, 1)
            linkH = random.uniform(0.2, 1)

            # New link's absolute position
            
            # if faceDim == "x": 
            #     if faceDir == -1:
            #         linkP = [LinkCenters[randomLinkIdx]-LinkSizes[randomLinkIdx]/2-linkW, LinkCenters[randomLinkIdx]-LinkSizes[randomLinkIdx]/2]
            #     else:
                    
            # elif faceDim == "y":
            #     if faceDir == -1:
            #         jointPos = [LinkCenters[randomLinkIdx][0], LinkCenters[randomLinkIdx][1] - LinkSizes[randomLinkIdx][1]/2, LinkCenters[randomLinkIdx][2]]
            #         linkCenter = [0, -linkSize[1]/2, 0]
            #     else:
            #         jointPos = [LinkCenters[randomLinkIdx][0], LinkCenters[randomLinkIdx][1] + LinkSizes[randomLinkIdx][1]/2, LinkCenters[randomLinkIdx][2]]
            #         linkCenter = [0, linkSize[1]/2, 0]
            # else:
            #     if faceDir == -1:
            #         jointPos = [LinkCenters[randomLinkIdx][0], LinkCenters[randomLinkIdx][1], LinkCenters[randomLinkIdx][2]- LinkSizes[randomLinkIdx][2]/2]
            #         linkCenter = [0, 0, -linkSize[2]/2]
            #     else:
            #         jointPos = [LinkCenters[randomLinkIdx][0], LinkCenters[randomLinkIdx][1], LinkCenters[randomLinkIdx][2]+ LinkSizes[randomLinkIdx][2]/2]
            #         linkCenter = [0, 0, linkSize[2]/2]

            # make sure the new link doesn't intersect with others

            linkSize = [linkW, linkL, linkH]

            if faceDim == "x": 
                if faceDir == -1:
                    jointPos = [LinkCenters[randomLinkIdx][0] - LinkSizes[randomLinkIdx][0]/2, LinkCenters[randomLinkIdx][1], LinkCenters[randomLinkIdx][2]]
                    linkCenter = [-linkSize[0]/2, 0, 0]
                else:
                    jointPos = [LinkCenters[randomLinkIdx][0] + LinkSizes[randomLinkIdx][0]/2, LinkCenters[randomLinkIdx][1], LinkCenters[randomLinkIdx][2]]
                    linkCenter = [linkSize[0]/2, 0, 0]
            elif faceDim == "y":
                if faceDir == -1:
                    jointPos = [LinkCenters[randomLinkIdx][0], LinkCenters[randomLinkIdx][1] - LinkSizes[randomLinkIdx][1]/2, LinkCenters[randomLinkIdx][2]]
                    linkCenter = [0, -linkSize[1]/2, 0]
                else:
                    jointPos = [LinkCenters[randomLinkIdx][0], LinkCenters[randomLinkIdx][1] + LinkSizes[randomLinkIdx][1]/2, LinkCenters[randomLinkIdx][2]]
                    linkCenter = [0, linkSize[1]/2, 0]
            else:
                if faceDir == -1:
                    jointPos = [LinkCenters[randomLinkIdx][0], LinkCenters[randomLinkIdx][1], LinkCenters[randomLinkIdx][2]- LinkSizes[randomLinkIdx][2]/2]
                    linkCenter = [0, 0, -linkSize[2]/2]
                else:
                    jointPos = [LinkCenters[randomLinkIdx][0], LinkCenters[randomLinkIdx][1], LinkCenters[randomLinkIdx][2]+ LinkSizes[randomLinkIdx][2]/2]
                    linkCenter = [0, 0, linkSize[2]/2]

            print(jointPos)
            # joint can move in any direction
            jointAx = random.choice(["1 0 0", "0 1 0", "0 0 1"])

            pyrosim.Send_Joint(
                name = "Link" + str(i-1) + "_Link" + str(i),
                parent = "Link" + str(i-1),
                child = "Link" + str(i),
                type = "revolute",
                position = jointPos,
                jointAxis = jointAx)
            
            color = self.hasSensor[i]

            # append the new link
            pyrosim.Send_Cube(name = "Link" + str(i), pos = linkCenter, size = linkSize, green = color)

            LinkCenters.append(linkCenter)
            LinkSizes.append(linkSize)
                
        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")
        self.numMotorNeurons = self.numJoints
        self.numSensorNeurons = 0
        
        for i in range(self.numLinks):
            if self.hasSensor:
                self.numSensorNeurons += 1
                pyrosim.Send_Sensor_Neuron(name = i, linkName = "Link" + str(i))
        
        motorName = self.numSensorNeurons
        for i in range(self.numJoints):
            pyrosim.Send_Motor_Neuron(name = motorName, jointName = "Link" + str(i) + "_Link" + str(i+1))
            motorName += 1
        
        self.weights = numpy.random.rand(self.numSensorNeurons, self.numMotorNeurons) * 2 -1
        for currentRow in range(self.numSensorNeurons):
            for currentColumn in range(self.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName = currentRow , targetNeuronName = currentColumn + self.numSensorNeurons , weight = self.weights[currentRow][currentColumn])
        pyrosim.End()

    def Mutate(self):
        randomRow = random.randint(0, self.numSensorNeurons-1)
        randomCol = random.randint(0, self.numMotorNeurons-1)
        self.weights[randomRow,randomCol] = random.random()*2 -1

    def Set_ID(self, id):
        self.myID = id