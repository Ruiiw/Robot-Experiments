import numpy
import pyrosim.pyrosim as pyrosim
import random
import os
import time
import constants as c

class SOLUTION:

    def __init__(self, nextAvailableID):
        self.myID = nextAvailableID
        self.numLinks = random.randint(3, 7)
        #self.numLinks = 3
        print("link num", self.numLinks)
        self.numJoints = self.numLinks -1

        # random number of sensors
        self.hasSensor = [False] * self.numLinks
        for i in range(self.numLinks):
            if random.random() > 0.5:
                self.hasSensor[i] = True

        # keeps track of links' self.children
        # key: parent; value: self.children
        self.children = {}


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
        pyrosim.Start_URDF("body" + str(self.myID) + ".urdf")

        # create first link
        linkS = [random.uniform(0.2, 1), random.uniform(0.2, 1), random.uniform(0.2, 1)]
        print("initial link size", linkS)
        firstC = self.hasSensor[0]
        pyrosim.Send_Cube(name = "Link0", pos = [0, 0, linkS[2]/2], size = linkS, green=firstC)

        # dictionary for tracking every link's absolute position
        # key: link index; value: [x min, x max, y min, y max, z min, z max]
        linkPos = {}
        linkPos[0] = [-linkS[0]/2, linkS[0]/2, -linkS[1]/2, linkS[1]/2, 0, linkS[2]]

        # dictionary for each link's available face
        # key: link index; value: available faces
        # 1: x-1, 2: x+1, 3: y-1, 4: y+1, 5: z-1, 6: z+1
        self.availFace = {}
        self.availFace[0] = [1, 2, 3, 4, 6]

        # every link's absolute center
        absCenters = [[0, 0, linkS[2]/2]]

        # joint's absolute position
        absJoints = []

        # keeps track of all links' relative centers and sizes
        self.LinkCenters = [[0, 0, linkS[2]/2]]
        self.LinkSizes = [linkS]

        self.children = {}

        
        for i in range(1, self.numLinks):
            # randomly choose a generated link and a face on it to add a joint
            randomLinkIdx = random.choice(list(self.availFace.keys()))
            face = random.choice(self.availFace[randomLinkIdx])

            if randomLinkIdx in self.children:
                self.children[randomLinkIdx].append(i)
            else:
                self.children[randomLinkIdx] = [i]

            # width, length, height of the newly generated link
            linkW = random.uniform(0.2, 1)
            linkL = random.uniform(0.2, 1)
            linkH = random.uniform(0.2, 1)

            # New link's absolute position
            # xMin = absCenters[randomLinkIdx][0] - linkW/2
            # xMax = absCenters[randomLinkIdx][0] + linkW/2
            # yMin = absCenters[randomLinkIdx][1] - linkL/2
            # yMax = absCenters[randomLinkIdx][1] + linkL/2
            # zMin = absCenters[randomLinkIdx][2] - linkH/2
            # zMax = absCenters[randomLinkIdx][2] + linkH/2
            # if face == 1:
            #     xMin = absCenters[randomLinkIdx][0]-self.LinkSizes[randomLinkIdx][0]/2-linkW
            #     xMax = absCenters[randomLinkIdx][0]-self.LinkSizes[randomLinkIdx][0]/2
            # elif face == 2:
            #     xMin = absCenters[randomLinkIdx][0]+self.LinkSizes[randomLinkIdx][0]/2
            #     xMax = absCenters[randomLinkIdx][0]+self.LinkSizes[randomLinkIdx][0]/2+linkW
            # elif face == 3:
            #     yMin = absCenters[randomLinkIdx][1]-self.LinkSizes[randomLinkIdx][1]/2-linkL
            #     yMax = absCenters[randomLinkIdx][1]-self.LinkSizes[randomLinkIdx][1]/2
            # elif face == 4:
            #     yMin = absCenters[randomLinkIdx][1]+self.LinkSizes[randomLinkIdx][1]/2
            #     yMax = absCenters[randomLinkIdx][1]+self.LinkSizes[randomLinkIdx][1]/2+linkL
            # elif face == 5:
            #     zMin = absCenters[randomLinkIdx][2]-self.LinkSizes[randomLinkIdx][2]/2-linkH
            #     zMax = absCenters[randomLinkIdx][2]-self.LinkSizes[randomLinkIdx][2]/2
            # else:
            #     zMin = absCenters[randomLinkIdx][2]+self.LinkSizes[randomLinkIdx][2]/2
            #     zMax = absCenters[randomLinkIdx][2]+self.LinkSizes[randomLinkIdx][2]/2+linkH
            
            self.availFace[randomLinkIdx].remove(face)
            if len(self.availFace[randomLinkIdx]) == 0:
                self.availFace.pop(randomLinkIdx)
            
            newFaces = [1, 2, 3, 4, 6]

            # change the link's height if it's below the surface
            # if zMin <= 0:
            #     print(zMin)
            #     linkH = 2 * random.uniform(0.1, absCenters[randomLinkIdx][2])
            #     zMin = absCenters[randomLinkIdx][2]-linkH/2
            #     print("new zMin", zMin)
            #     newFaces.remove(5)

            if face != 6:
                if face%2 == 0:
                    newFaces.remove(face-1)
                else:
                    newFaces.remove(face+1)

            self.availFace[i] = newFaces

            # linkAbsPos = [xMin, xMax, yMin, yMax, zMin, zMax]
            # linkAbsCenter = [xMin+linkW/2, xMax-linkW/2, yMin+linkL/2, yMax-linkL/2, zMin+linkH/2, zMax-linkH/2]
            linkSize = [linkW, linkL, linkH]

            # actually append the new link
            if face == 1:
                jointPos = [self.LinkCenters[randomLinkIdx][0] - self.LinkSizes[randomLinkIdx][0]/2, self.LinkCenters[randomLinkIdx][1], self.LinkCenters[randomLinkIdx][2]]
                linkCenter = [-linkSize[0]/2, 0, 0]
                #absJoint = [absCenters[randomLinkIdx][0]-self.LinkSizes[randomLinkIdx][0]/2, absCenters[randomLinkIdx][1], absCenters[randomLinkIdx][2]]
            elif face == 2:
                jointPos = [self.LinkCenters[randomLinkIdx][0] + self.LinkSizes[randomLinkIdx][0]/2, self.LinkCenters[randomLinkIdx][1], self.LinkCenters[randomLinkIdx][2]]
                linkCenter = [linkSize[0]/2, 0, 0]
                #absJoint = [absCenters[randomLinkIdx][0]+self.LinkSizes[randomLinkIdx][0]/2, absCenters[randomLinkIdx][1], absCenters[randomLinkIdx][2]]
            elif face == 3:
                jointPos = [self.LinkCenters[randomLinkIdx][0], self.LinkCenters[randomLinkIdx][1] - self.LinkSizes[randomLinkIdx][1]/2, self.LinkCenters[randomLinkIdx][2]]
                linkCenter = [0, -linkSize[1]/2, 0]
                #absJoint = [absCenters[randomLinkIdx][0], absCenters[randomLinkIdx][1]-self.LinkSizes[randomLinkIdx][1]/2, absCenters[randomLinkIdx][2]]
            elif face == 4:
                jointPos = [self.LinkCenters[randomLinkIdx][0], self.LinkCenters[randomLinkIdx][1] + self.LinkSizes[randomLinkIdx][1]/2, self.LinkCenters[randomLinkIdx][2]]
                linkCenter = [0, linkSize[1]/2, 0]
                #absJoint = [absCenters[randomLinkIdx][0], absCenters[randomLinkIdx][1]+self.LinkSizes[randomLinkIdx][1]/2, absCenters[randomLinkIdx][2]]
            elif face == 5:
                jointPos = [self.LinkCenters[randomLinkIdx][0], self.LinkCenters[randomLinkIdx][1], self.LinkCenters[randomLinkIdx][2]- self.LinkSizes[randomLinkIdx][2]/2]
                linkCenter = [0, 0, -linkSize[2]/2]
                #absJoint = [absCenters[randomLinkIdx][0], absCenters[randomLinkIdx][1], absCenters[randomLinkIdx][2]-self.LinkSizes[randomLinkIdx][2]/2]
            else:
                jointPos = [self.LinkCenters[randomLinkIdx][0], self.LinkCenters[randomLinkIdx][1], self.LinkCenters[randomLinkIdx][2]+ self.LinkSizes[randomLinkIdx][2]/2]
                linkCenter = [0, 0, linkSize[2]/2]
                #absJoint = [absCenters[randomLinkIdx][0], absCenters[randomLinkIdx][1], absCenters[randomLinkIdx][2]+self.LinkSizes[randomLinkIdx][2]/2]

            # print("joint rela pos", jointPos)
            # print("joint abs pos", absJoint)
            # joint can move in any direction
            jointAx = random.choice(["1 0 0", "0 1 0", "0 0 1"])

            pyrosim.Send_Joint(
                name = "Link" + str(randomLinkIdx) + "_Link" + str(i),
                parent = "Link" + str(randomLinkIdx),
                child = "Link" + str(i),
                type = "revolute",
                position = jointPos,
                jointAxis = jointAx)
            
            color = self.hasSensor[i]

            # append the new link
            pyrosim.Send_Cube(name = "Link" + str(i), pos = linkCenter, size = linkSize, green = color)
            # absolute centers
            # absCenters.append(linkAbsCenter)
            # absJoints.append(absJoint)
            # relative centers
            self.LinkCenters.append(linkCenter)
            # link xyz absolute position
            # linkPos[i] = linkAbsPos
            # link size
            self.LinkSizes.append(linkSize)
                
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
        for parent in self.children:
            for child in self.children[parent]:
                pyrosim.Send_Motor_Neuron(name = motorName, jointName = "Link" + str(parent) + "_Link" + str(child))
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

        # choice = random.choice([1, 2, 3, 4])

        # add a link
        # if choice == 2 or choice == 3:
        #     if self.numLinks > 6:
        #         return
            
        #     randomLinkIdx = random.choice(list(self.availFace.keys()))
        #     face = random.choice(self.availFace[randomLinkIdx])
        #     curLinkIdx = self.numLinks+1

        #     if randomLinkIdx in self.children:
        #         self.children[randomLinkIdx].append(curLinkIdx)
        #     else:
        #         self.children[randomLinkIdx] = [curLinkIdx]

        #     # width, length, height of the newly generated link
        #     linkW = random.uniform(0.2, 1)
        #     linkL = random.uniform(0.2, 1)
        #     linkH = random.uniform(0.2, 1)

        #     self.availFace[randomLinkIdx].remove(face)
        #     if len(self.availFace[randomLinkIdx]) == 0:
        #         self.availFace.pop(randomLinkIdx)
            
        #     newFaces = [1, 2, 3, 4, 6]
            
        #     if face != 6:
        #         if face%2 == 0:
        #             newFaces.remove(face-1)
        #         else:
        #             newFaces.remove(face+1)

        #     self.availFace[self.numLinks+1] = newFaces

        #     linkSize = [linkW, linkL, linkH]

        #     # actually append the new link
        #     if face == 1:
        #         jointPos = [self.LinkCenters[randomLinkIdx][0] - self.LinkSizes[randomLinkIdx][0]/2, self.LinkCenters[randomLinkIdx][1], self.LinkCenters[randomLinkIdx][2]]
        #         linkCenter = [-linkSize[0]/2, 0, 0]
                
        #     elif face == 2:
        #         jointPos = [self.LinkCenters[randomLinkIdx][0] + self.LinkSizes[randomLinkIdx][0]/2, self.LinkCenters[randomLinkIdx][1], self.LinkCenters[randomLinkIdx][2]]
        #         linkCenter = [linkSize[0]/2, 0, 0]
                
        #     elif face == 3:
        #         jointPos = [self.LinkCenters[randomLinkIdx][0], self.LinkCenters[randomLinkIdx][1] - self.LinkSizes[randomLinkIdx][1]/2, self.LinkCenters[randomLinkIdx][2]]
        #         linkCenter = [0, -linkSize[1]/2, 0]
                
        #     elif face == 4:
        #         jointPos = [self.LinkCenters[randomLinkIdx][0], self.LinkCenters[randomLinkIdx][1] + self.LinkSizes[randomLinkIdx][1]/2, self.LinkCenters[randomLinkIdx][2]]
        #         linkCenter = [0, linkSize[1]/2, 0]
                
        #     elif face == 5:
        #         jointPos = [self.LinkCenters[randomLinkIdx][0], self.LinkCenters[randomLinkIdx][1], self.LinkCenters[randomLinkIdx][2]- self.LinkSizes[randomLinkIdx][2]/2]
        #         linkCenter = [0, 0, -linkSize[2]/2]
                
        #     else:
        #         jointPos = [self.LinkCenters[randomLinkIdx][0], self.LinkCenters[randomLinkIdx][1], self.LinkCenters[randomLinkIdx][2]+ self.LinkSizes[randomLinkIdx][2]/2]
        #         linkCenter = [0, 0, linkSize[2]/2]
                

        #     jointAx = random.choice(["1 0 0", "0 1 0", "0 0 1"])

        #     pyrosim.Send_Joint(
        #         name = "Link" + str(randomLinkIdx) + "_Link" + str(curLinkIdx),
        #         parent = "Link" + str(randomLinkIdx),
        #         child = "Link" + str(curLinkIdx),
        #         type = "revolute",
        #         position = jointPos,
        #         jointAxis = jointAx)
            
        #     hasColor = random.choice(0, 2)
        #     if hasColor == 0:
        #         self.hasSensor.append(True)
        #     else:
        #         self.hasSensor.append(False)

        #     # append the new link
        #     pyrosim.Send_Cube(name = "Link" + str(curLinkIdx), pos = linkCenter, size = linkSize, green = self.hasSensor[-1])
        #     # relative centers
        #     self.LinkCenters.append(linkCenter)
        #     # link size
        #     self.LinkSizes.append(linkSize)

        #     # UPDATE WEIGHTS


        # remove last link
        # if choice == 4:
        #     if self.numLinks < 3:
        #         return

        #     self.LinkSizes.pop()
        #     self.LinkCenters.pop()
        #     self.hasSensor.pop()

        #     self.numJoints -= 1
        #     # UPDATE WEIGHTS
        


    def Set_ID(self, id):
        self.myID = id