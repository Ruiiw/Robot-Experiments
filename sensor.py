import numpy
import pyrosim.pyrosim as pyrosim

class SENSOR:

    def __init__(self, linkName):

        self.linkName = linkName
        self.values = numpy.zeros(1000)

    def Get_Value(self, i):
        self.values[i] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)
        if i == 999:
            print(self.values)

    def Save_Value(self):
        numpy.save('data/sensorData.npy', self.values)