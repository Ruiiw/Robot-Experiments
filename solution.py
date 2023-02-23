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

    
    # def Create_Body(self):
    #     pyrosim.Start_URDF("body.urdf")

    #     # create first link
    #     linkS = [random.uniform(0.2, 1), random.uniform(0.2, 1), random.uniform(0.2, 1)]
    #     firstC = self.hasSensor[0]
    #     pyrosim.Send_Cube(name = "Link0", pos = [0, 0, linkS[2]/2], size = linkS, green=firstC)

    #     # dictionary for tracking every link's absolute position
    #     # key: link index; value: [(x min, x max), (y min, y max), (z min, z max)]
    #     linkPos = {}
    #     linkPos[0] = [-linkS[0]/2, linkS[0]/2, -linkS[1]/2, linkS[1]/2, 0, linkS[2]]

    #     # every link's absolute center
    #     absCenters = [[0, 0, linkS[2]/2]]

    #     # keeps track of all links' relative centers and positions
    #     LinkCenters = [[0, 0, linkS[2]/2]]
    #     LinkSizes = [linkS]

    #     for i in range(1, self.numLinks):
    #         print(i)
    #         # randomly choose a generated link and a face on it to add a joint
    #         faceDim = random.choice(["x", "y", "z"])
    #         faceDir = random.choice([-1, 1])
    #         randomLinkIdx = random.randint(0, len(LinkCenters)-1)
    #         print("random",randomLinkIdx)

    #         # width, length, height of the newly generated link
    #         linkW = random.uniform(0.2, 1)
    #         linkL = random.uniform(0.2, 1)
    #         linkH = random.uniform(0.2, 1)

    #         # New link's absolute position
    #         xMin = absCenters[randomLinkIdx][0] - linkW/2
    #         xMax = absCenters[randomLinkIdx][0] + linkW/2
    #         yMin = absCenters[randomLinkIdx][1] - linkL/2
    #         yMax = absCenters[randomLinkIdx][1] + linkL/2
    #         zMin = absCenters[randomLinkIdx][2] - linkL/2
    #         zMax = absCenters[randomLinkIdx][2] + linkL/2
    #         if faceDim == "x": 
    #             if faceDir == -1:
    #                 xMin = absCenters[randomLinkIdx][0]-LinkSizes[randomLinkIdx][0]/2-linkW
    #                 xMax = absCenters[randomLinkIdx][0]-LinkSizes[randomLinkIdx][0]/2
    #             else:
    #                 xMin = absCenters[randomLinkIdx][0]+LinkSizes[randomLinkIdx][0]/2
    #                 xMax = absCenters[randomLinkIdx][0]+LinkSizes[randomLinkIdx][0]/2+linkW
    #         elif faceDim == "y":
    #             if faceDir == -1:
    #                 yMin = absCenters[randomLinkIdx][1]-LinkSizes[randomLinkIdx][1]/2-linkL
    #                 yMax = absCenters[randomLinkIdx][1]-LinkSizes[randomLinkIdx][1]/2
    #             else:
    #                 yMin = absCenters[randomLinkIdx][1]+LinkSizes[randomLinkIdx][1]/2
    #                 yMax = absCenters[randomLinkIdx][1]+LinkSizes[randomLinkIdx][1]/2+linkL
    #         else:
    #             if faceDir == -1:
    #                 zMin = absCenters[randomLinkIdx][2]-LinkSizes[randomLinkIdx][2]/2-linkH
    #                 zMax = absCenters[randomLinkIdx][2]-LinkSizes[randomLinkIdx][2]/2
    #             else:
    #                 zMin = absCenters[randomLinkIdx][2]+LinkSizes[randomLinkIdx][2]/2
    #                 zMax = absCenters[randomLinkIdx][2]+LinkSizes[randomLinkIdx][2]/2+linkH
            

    #         # make sure the new link doesn't intersect with others
    #         # for link in linkPos:
    #         #     if xMin < linkPos[link][1]:
    #         #         dif = linkPos[link][1]-xMin
    #         #         xMin = linkPos[link][1]
    #         #         linkW -= dif
    #         #     elif xMax > linkPos[link][0]:
    #         #         dif = xMax-linkPos[link][0]
    #         #         xMax = linkPos[link][0]
    #         #         linkW -= dif
    #         #     elif yMin < linkPos[link][3]:
    #         #         dif = linkPos[link][3]-yMin
    #         #         yMin = linkPos[link][3]
    #         #         linkL -= dif
    #         #     elif yMax > linkPos[link][2]:
    #         #         dif = yMax-linkPos[link][2]
    #         #         yMax = linkPos[link][2]
    #         #         linkL -= dif
    #         #     elif zMin < linkPos[link][5]:
    #         #         dif = linkPos[link][5]-zMin
    #         #         zMin = linkPos[link][5]
    #         #         linkH -= dif
    #         #     elif zMax > linkPos[link][4]:
    #         #         dif = zMax-linkPos[link][4]
    #         #         zMax = linkPos[link][4]
    #         #         linkL -= dif

    #         linkAbsPos = [xMin, xMax, yMin, yMax, zMin, zMax]
    #         linkAbsCenter = [xMin+linkW/2, xMax-linkW/2, yMin+linkL/2, yMax-linkL/2, zMin+linkH/2, zMax-linkH/2]
    #         linkSize = [linkW, linkL, linkH]

    #         if faceDim == "x": 
    #             if faceDir == -1:
    #                 jointPos = [LinkCenters[randomLinkIdx][0] - LinkSizes[randomLinkIdx][0]/2, LinkCenters[randomLinkIdx][1], LinkCenters[randomLinkIdx][2]]
    #                 linkCenter = [-linkSize[0]/2, 0, 0]
    #             else:
    #                 jointPos = [LinkCenters[randomLinkIdx][0] + LinkSizes[randomLinkIdx][0]/2, LinkCenters[randomLinkIdx][1], LinkCenters[randomLinkIdx][2]]
    #                 linkCenter = [linkSize[0]/2, 0, 0]
    #         elif faceDim == "y":
    #             if faceDir == -1:
    #                 jointPos = [LinkCenters[randomLinkIdx][0], LinkCenters[randomLinkIdx][1] - LinkSizes[randomLinkIdx][1]/2, LinkCenters[randomLinkIdx][2]]
    #                 linkCenter = [0, -linkSize[1]/2, 0]
    #             else:
    #                 jointPos = [LinkCenters[randomLinkIdx][0], LinkCenters[randomLinkIdx][1] + LinkSizes[randomLinkIdx][1]/2, LinkCenters[randomLinkIdx][2]]
    #                 linkCenter = [0, linkSize[1]/2, 0]
    #         else:
    #             if faceDir == -1:
    #                 jointPos = [LinkCenters[randomLinkIdx][0], LinkCenters[randomLinkIdx][1], LinkCenters[randomLinkIdx][2]- LinkSizes[randomLinkIdx][2]/2]
    #                 linkCenter = [0, 0, -linkSize[2]/2]
    #             else:
    #                 jointPos = [LinkCenters[randomLinkIdx][0], LinkCenters[randomLinkIdx][1], LinkCenters[randomLinkIdx][2]+ LinkSizes[randomLinkIdx][2]/2]
    #                 linkCenter = [0, 0, linkSize[2]/2]

    #         print(jointPos)
    #         # joint can move in any direction
    #         jointAx = random.choice(["1 0 0", "0 1 0", "0 0 1"])

    #         pyrosim.Send_Joint(
    #             name = "Link" + str(i-1) + "_Link" + str(i),
    #             parent = "Link" + str(i-1),
    #             child = "Link" + str(i),
    #             type = "revolute",
    #             position = jointPos,
    #             jointAxis = jointAx)
            
    #         color = self.hasSensor[i]

    #         # append the new link
    #         pyrosim.Send_Cube(name = "Link" + str(i), pos = linkCenter, size = linkSize, green = color)
    #         # absolute centers
    #         absCenters.append(linkAbsCenter)
    #         # relative centers
    #         LinkCenters.append(linkCenter)
    #         # link xyz absolute position
    #         linkPos[i] = linkAbsPos
    #         # link size
    #         LinkSizes.append(linkSize)
                
    #     pyrosim.End()

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

        # dictionary for each link's available face
        # key: link index; value: available faces
        # 1: x-1, 2: x+1, 3: y-1, 4: y+1, 5: z-1, 6: z+1
        availFace = {}
        availFace[0] = [1, 2, 3, 4, 6]

        # every link's absolute center
        absCenters = [[0, 0, linkS[2]/2]]

        # keeps track of all links' relative centers and sizes
        LinkCenters = [[0, 0, linkS[2]/2]]
        LinkSizes = [linkS]

        for i in range(1, self.numLinks):
            print(i)
            # randomly choose a generated link and a face on it to add a joint
            # faceDim = random.choice(["x", "y", "z"])
            # faceDir = random.choice([-1, 1])

            while True:
                randomLinkIdx = random.randint(0, len(LinkCenters)-1)
                print(availFace[randomLinkIdx])
                face = random.choice(availFace[randomLinkIdx])
                if face != None:
                    break

            print("random",randomLinkIdx)

            # width, length, height of the newly generated link
            linkW = random.uniform(0.2, 1)
            linkL = random.uniform(0.2, 1)
            linkH = random.uniform(0.2, 1)

            # New link's absolute position

            xMin = absCenters[randomLinkIdx][0] - linkW/2
            xMax = absCenters[randomLinkIdx][0] + linkW/2
            yMin = absCenters[randomLinkIdx][1] - linkL/2
            yMax = absCenters[randomLinkIdx][1] + linkL/2
            zMin = absCenters[randomLinkIdx][2] - linkL/2
            zMax = absCenters[randomLinkIdx][2] + linkL/2
            if face == 1:
                xMin = absCenters[randomLinkIdx][0]-LinkSizes[randomLinkIdx][0]/2-linkW
                xMax = absCenters[randomLinkIdx][0]-LinkSizes[randomLinkIdx][0]/2
            elif face == 2:
                xMin = absCenters[randomLinkIdx][0]+LinkSizes[randomLinkIdx][0]/2
                xMax = absCenters[randomLinkIdx][0]+LinkSizes[randomLinkIdx][0]/2+linkW
            elif face == 3:
                yMin = absCenters[randomLinkIdx][1]-LinkSizes[randomLinkIdx][1]/2-linkL
                yMax = absCenters[randomLinkIdx][1]-LinkSizes[randomLinkIdx][1]/2
            elif face == 4:
                yMin = absCenters[randomLinkIdx][1]+LinkSizes[randomLinkIdx][1]/2
                yMax = absCenters[randomLinkIdx][1]+LinkSizes[randomLinkIdx][1]/2+linkL
            elif face == 5:
                zMin = absCenters[randomLinkIdx][2]-LinkSizes[randomLinkIdx][2]/2-linkH
                zMax = absCenters[randomLinkIdx][2]-LinkSizes[randomLinkIdx][2]/2
            else:
                zMin = absCenters[randomLinkIdx][2]+LinkSizes[randomLinkIdx][2]/2
                zMax = absCenters[randomLinkIdx][2]+LinkSizes[randomLinkIdx][2]/2+linkH
            
            availFace[randomLinkIdx].remove(face)
            
            newFaces = [1, 2, 3, 4, 5, 6]
            if face%2 == 0:
                newFaces.remove(face-1)
            else:
                newFaces.remove(face+1)
            

            # make sure the new link doesn't intersect with others
            for link in linkPos:
                if xMin < linkPos[link][1]:
                    dif = linkPos[link][1]-xMin
                    xMin = linkPos[link][1]
                    linkW -= dif
                    if 1 in newFaces:
                        newFaces.remove(1)
                elif xMax > linkPos[link][0]:
                    dif = xMax-linkPos[link][0]
                    xMax = linkPos[link][0]
                    linkW -= dif
                    if 2 in newFaces:
                        newFaces.remove(2)
                elif yMin < linkPos[link][3]:
                    dif = linkPos[link][3]-yMin
                    yMin = linkPos[link][3]
                    linkL -= dif
                    if 3 in newFaces:
                        newFaces.remove(3)
                elif yMax > linkPos[link][2]:
                    dif = yMax-linkPos[link][2]
                    yMax = linkPos[link][2]
                    linkL -= dif
                    if 4 in newFaces:
                        newFaces.remove(4)
                elif zMin < linkPos[link][5]:
                    dif = linkPos[link][5]-zMin
                    zMin = linkPos[link][5]
                    linkH -= dif
                    if 5 in newFaces:
                        newFaces.remove(5)
                elif zMax > linkPos[link][4]:
                    dif = zMax-linkPos[link][4]
                    zMax = linkPos[link][4]
                    linkL -= dif
                    if 6 in newFaces:
                        newFaces.remove(6)

            availFace[i] = newFaces

            linkAbsPos = [xMin, xMax, yMin, yMax, zMin, zMax]
            linkAbsCenter = [xMin+linkW/2, xMax-linkW/2, yMin+linkL/2, yMax-linkL/2, zMin+linkH/2, zMax-linkH/2]
            linkSize = [linkW, linkL, linkH]

            # actually append the new link
            if face == 1:
                jointPos = [LinkCenters[randomLinkIdx][0] - LinkSizes[randomLinkIdx][0]/2, LinkCenters[randomLinkIdx][1], LinkCenters[randomLinkIdx][2]]
                linkCenter = [-linkSize[0]/2, 0, 0]
            elif face == 2:
                jointPos = [LinkCenters[randomLinkIdx][0] + LinkSizes[randomLinkIdx][0]/2, LinkCenters[randomLinkIdx][1], LinkCenters[randomLinkIdx][2]]
                linkCenter = [linkSize[0]/2, 0, 0]
            elif face == 3:
                jointPos = [LinkCenters[randomLinkIdx][0], LinkCenters[randomLinkIdx][1] - LinkSizes[randomLinkIdx][1]/2, LinkCenters[randomLinkIdx][2]]
                linkCenter = [0, -linkSize[1]/2, 0]
            elif face == 4:
                jointPos = [LinkCenters[randomLinkIdx][0], LinkCenters[randomLinkIdx][1] + LinkSizes[randomLinkIdx][1]/2, LinkCenters[randomLinkIdx][2]]
                linkCenter = [0, linkSize[1]/2, 0]
            elif face == 5:
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
            # absolute centers
            absCenters.append(linkAbsCenter)
            # relative centers
            LinkCenters.append(linkCenter)
            # link xyz absolute position
            linkPos[i] = linkAbsPos
            # link size
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