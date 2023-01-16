import pybullet as p
import pybullet_data
import time
import pyrosim.pyrosim as pyrosim
import numpy
import random

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0,0,-9.8)
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")

p.loadSDF("world.sdf")

pyrosim.Prepare_To_Simulate(robotId)
frontLegSensorValues = numpy.zeros(1000)
backLegSensorValues = numpy.zeros(1000)
linAngles = numpy.linspace(0, 2*numpy.pi, 1000)
targetAngles = numpy.sin(linAngles)
numpy.save('data/targetAngles.npy', targetAngles)

for i in range(1000):
    p.stepSimulation()
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    pyrosim.Set_Motor_For_Joint(
    bodyIndex = robotId,
    jointName = "Torso_BackLeg",
    controlMode = p.POSITION_CONTROL,
    targetPosition = random.uniform(-numpy.pi/4, numpy.pi/4),
    maxForce = 60)
    pyrosim.Set_Motor_For_Joint(
    bodyIndex = robotId,
    jointName = "Torso_FrontLeg",
    controlMode = p.POSITION_CONTROL,
    targetPosition = random.uniform(-numpy.pi/4, numpy.pi/4),
    maxForce = 60)
    time.sleep(1/60)

# print(frontLegSensorValues)
# print(backLegSensorValues)
numpy.save('data/frontLegSensorData.npy', frontLegSensorValues)
numpy.save('data/backLegSensorData.npy', backLegSensorValues)
p.disconnect()