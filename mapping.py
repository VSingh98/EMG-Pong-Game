import socket

'''
This class defines the static method changePosition that is called by
The snensory input method. The changePosition method is responsible for 
sending a UDP packet corresponding to position to the paddle position

'''
class Mapper(object):

	ANALOG_VAL_THRESHOLD = 0.00002
	DELTA = .001

	FAST_SEQUENCE_THRESHOLD = .4

	UPPER_LIM = 1
	LOWER_LIM = 0
	MIDDLE = 0.5
	AXIS_SCALAR = 10

	position = MIDDLE
    
	times = [-1, -1]
	armVectors = 0

	sock = socket.socket(socket.AF_INIT, socket.SOCK_DGRAM)

	@classmethod
	def changePosition(leftVal, rightVal, time):

		vector = int()

		if (leftVal > ANALOG_VAL_THRESHOLD && rightVal > \
				ANALOG_VAL_THRESHOLD):
			return;		
		
		elif (leftVal > THRESHOLD):
			vector = 1
		else:
			vector = -1
		
		times[1] = times[0]
		times[0] = time
		
		armVectors += vector

		
		if (times[0] - times[1] < FAST_SEQUENCE_THRESHOLD):
			if (armVectors == 0):
				position == MIDDLE
			elif (armVectors == -2):
				position == LOWER_LIM
			else:
				position == UPPER_LIM

			armVectors = 0
		else:
			position = position + vector * DELTA

		if (armsVector == -2 or armsVector == 2):
			armsVector = 0

		sock.sendTo(position * AXIS_SCALAR)		
