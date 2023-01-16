import numpy
import matplotlib.pyplot

frontLegSensorValues = numpy.load('data/frontLegSensorData.npy')
backLegSensorValues = numpy.load('data/backLegSensorData.npy')
targetAngles = numpy.load('data/targetAngles.npy')
print(backLegSensorValues)
# matplotlib.pyplot.plot(frontLegSensorValues, linewidth = 3, label = 'front leg')
# matplotlib.pyplot.plot(backLegSensorValues, label = 'back leg')
matplotlib.pyplot.plot(targetAngles)
matplotlib.pyplot.legend()
matplotlib.pyplot.show()