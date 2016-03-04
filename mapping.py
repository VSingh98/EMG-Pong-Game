import socket

'''
This class defines the static method changePosition that is called by
The snensory input method. The changePosition method is responsible for 
sending a UDP packet corresponding to position to the paddle position
'''

class Mapper(object):
    
    IP_ADDR = '127.0.0.1' # IP Address to send UDP packet
    PORTNUM = 5005 # Socket endpoint, where to communicate 

    ANALOG_VAL_THRESHOLD = 0.00002  # threshold for determining muscle flexion
    DELTA = .001    # amuont by which we update position with each
                    # changePosition call

    UPPER_LIM = 1   # Upper limit of position in game
    LOWER_LIM = 0   # Lower limit of position in game
    MIDDLE = 0.5    # Middle position in game
    AXIS_SCALAR = 1    # Scalar by which to multiply normalized limits to send
                        # in UDP packet to game

    position = MIDDLE   # we initialize position to the middle
    
    vector = 0  # Will it go up (1), down(-1), or stay (0)

    sock = socket.socket(socket.AF_INIT, socket.SOCK_DGRAM) # create a socket
    
    sock.connect((IPADDR, PORTNUM)) # connect socket to server

    LEFT_NORMALIZATION_FACTOR = int(open("lnorm", 'r').readline()[-1:])

    RIGHT_NORMALIZATION_FACTOR = int(open("rnorm", 'r').readline()[-1:])


    '''
    Purpose: This is method is called by signal filtering script to map the EMG
    values to position in the Pong video game and to send the respective UDP
    packet to the Pong server.
    '''
    @staticmethod
    def changePosition(leftVal, rightVal, time):

        vector = leftVal/LEFT_NORMALIZATION_FACTOR - \
            rightVal/RIGHT_NORMALIZATION_FACTOR

        if (vector < ANALOG_VAL_THRESHOLD):
            vector = 0


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
        sock.sendTo( str(position * AXIS_SCALAR) )
    


