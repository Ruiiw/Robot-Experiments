import pyrosim.pyrosim as pyrosim
import random

def Generate_Box():
    pyrosim.Start_URDF("box.urdf")
    pyrosim.Send_Cube(name="box", pos=[-20, 20, 0.5] , size=[1, 1, 1])
    pyrosim.End()

def Generate_Body():
    pyrosim.Start_URDF("body.urdf")
    length = 1
    width = 1
    height = 1
    pyrosim.Send_Cube(name="Torso", pos=[1.5, 0, 1.5] , size=[length, width, height])
    pyrosim.Send_Joint(name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [1, 0, 1])
    pyrosim.Send_Cube(name="BackLeg", pos=[-0.5, 0, -0.5] , size=[length, width, height])
    pyrosim.Send_Joint(name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [2, 0, 1])
    pyrosim.Send_Cube(name="FrontLeg", pos=[0.5, 0, -0.5] , size=[length, width, height])
    pyrosim.End()

def Generate_Brain():
    pyrosim.Start_NeuralNetwork("brain.nndf")
    pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
    pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "BackLeg")
    pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "FrontLeg")
    pyrosim.Send_Motor_Neuron( name = 3 , jointName = "Torso_BackLeg")
    pyrosim.Send_Motor_Neuron( name = 4 , jointName = "Torso_FrontLeg")
    pyrosim.Send_Synapse(sourceNeuronName = 0 , targetNeuronName = 3 , weight = -1.0)
    pyrosim.Send_Synapse(sourceNeuronName = 1 , targetNeuronName = 3 , weight = -1.0)
    pyrosim.Send_Synapse(sourceNeuronName = 0 , targetNeuronName = 4 , weight = -1.0)
    pyrosim.Send_Synapse(sourceNeuronName = 2 , targetNeuronName = 4 , weight = -1.0)
    sensorNeuNames = [0, 1, 2]
    motorNeuNames = [3, 4]
    for sNeuron in sensorNeuNames:
        for mNeuron in motorNeuNames:
            pyrosim.Send_Synapse(sourceNeuronName = sNeuron , targetNeuronName = mNeuron , weight = random.randrange(-1, 1))
    pyrosim.End()


Generate_Box()
Generate_Body()
Generate_Brain()