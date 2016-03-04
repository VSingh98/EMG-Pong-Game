import socket
from os import path

'''
This class defines the static method changePosition that is called by
The snensory input method. The changePosition method is responsible for 
sending a UDP packet corresponding to position to the paddle position
'''

class Mapper(object):
    
    IP_ADDR = '127.0.0.1' # IP Address to send UDP packet
    PORTNUM = 5005 # Socket endpoint, where to communicate 

    DELTA = .001    # amuont by which we update position with each
                    # changePosition call

    MIDDLE = 0.5    # Middle position in game
    AXIS_SCALAR = 1    # Scalar by which to multiply normalized limits to send
                        # in UDP packet to game

    position = MIDDLE   # we initialize position to the middle
    
    vector = 0  # Will it go up (1), down(-1), or stay (0)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # create a socket
    
    sock.connect((IPADDR, PORTNUM)) # connect socket to server

    LEFT_NORMALIZATION_FACTOR = 0
    RIGHT_NORMALIZATION_FACTOR = 0
    
	LEFT_THRES = 0  # threshold for determining muscle flexion
	RIGHT_THRES = 0

	'''
	to initialize the normalization factors
	'''
	@staticmethod
	def init():
		if op.isFile('lnorm'):
			LEFT_NORMALIZATION_FACTOR = 6.0/7*float(open("lnorm", 'r').readline()[-1:])

		if op.isFile('rnorm'):
			RIGHT_NORMALIZATION_FACTOR = 6.0/7*float(open('rnorm','r').readline()[-1:])

		LEFT_THRES = LEFT_NORMALIZATION_FACTOR/6.0
		RIGHT_THRES = RIGHT_NORMALIZATION_FACTOR/6.0
    '''
    Purpose: This is method is called by signal filtering script to map the EMG
    values to position in the Pong video game and to send the respective UDP
    packet to the Pong server.
    '''
    @staticmethod
    def changePosition(leftVal, rightVal):

		if (leftVal < LEFT_THRES):
			leftVal = 0

		if (rightVal < RIGHT_THRES):
			rightVal = 0

        vector = leftVal/LEFT_NORMALIZATION_FACTOR - \
            rightVal/RIGHT_NORMALIZATION_FACTOR

        position = position + vector * DELTA

        # send UPD packet of position to game
        sendUDPPacket()

    '''
    Purpose: to send a UDP packet to the Pong server
    '''
    @staticmethod
    def sendUDPPacket():

        # keep position within dimensions of game
        if position > 1:
            position = 1

        elif position < -1:
            position = -1 
        
        # send str Pong server
        sock.sendto( str(position * AXIS_SCALAR) )
    


