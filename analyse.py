import numpy
import matplotlib.pyplot

frontLegSensorValues = numpy.load('data/frontLegSensorData.npy')
backLegSensorValues = numpy.load('data/backLegSensorData.npy')
backLeg_targetAngles = numpy.load('data/backLeg_targetAngles.npy')
frontLeg_targetAngles = numpy.load('data/frontLeg_targetAngles.npy')
matplotlib.pyplot.plot(backLeg_targetAngles, label = 'front leg')
matplotlib.pyplot.plot(frontLeg_targetAngles, label = 'back leg')
matplotlib.pyplot.legend()
matplotlib.pyplot.show()