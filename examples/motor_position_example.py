import brickpi
import time

interface=brickpi.Interface()
interface.initialize()

motors = [0,1]

interface.motorEnable(motors[0])
interface.motorEnable(motors[1])

motorParams = interface.MotorAngleControllerParameters()
motorParams.maxRotationAcceleration = 6.0
motorParams.maxRotationSpeed = 12.0
motorParams.feedForwardGain = 255/20.0
motorParams.minPWM = 18.0
motorParams.pidParameters.minOutput = -255
motorParams.pidParameters.maxOutput = 255
motorParams.pidParameters.k_p = 650.0*0.6
motorParams.pidParameters.k_i = 2*motorParams.pidParameters.k_p / 0.36
motorParams.pidParameters.k_d = motorParams.pidParameters.k_p * 0.36 / 8

interface.setMotorAngleControllerParameters(motors[0],motorParams)
interface.setMotorAngleControllerParameters(motors[1],motorParams)

logPath = '~/Documents/log'

try:
	while True:
		angle = float(input("Enter a angle to rotate (in radians): "))
		interface.startLogging(logPath + 'logDefaultPositionSetup.txt')
		interface.increaseMotorAngleReferences(motors,[angle,angle])

		while not interface.motorAngleReferencesReached(motors) :
			motorAngles = interface.getMotorAngles(motors)
			if motorAngles :
				print "Motor angles: ", motorAngles[0][0], ", ", motorAngles[1][0]
			time.sleep(0.1)

		print "Destination reached!"

except KeyboardInterrupt:
        interface.stopLogging()
        interface.terminate()
