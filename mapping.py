import socket

'''
This class defines the static method changePosition that is called by
The snensory input method. The changePosition method is responsible for 
sending a UDP packet corresponding to position to the paddle position
'''

class Mapper(object):
    
    IP_ADDR = '127.0.0.1'
    PORTNUM = 0

    ANALOG_VAL_THRESHOLD = 0.00002  # threshold for determining muscle flexion
    DELTA = .001    # amuont by which we update position with each
                    # changePosition call

    FAST_SEQUENCE_THRESHOLD = .4    # time in seconds between two arm flexions
                                    # to do teleporation

    UPPER_LIM = 1   # Upper limit of position in game
    LOWER_LIM = 0   # Lower limit of position in game
    MIDDLE = 0.5    # Middle position in game
    AXIS_SCALAR = 10    # Scalar by which to multiply normalized limits to send
                        # in UDP packet to game

    position = MIDDLE   # we initialize position to the middle
    
    times = [-1, -1]    # this will hold the times of the last two calls to
                        # changePosition

    vector = 0  # Will it go up (1), down(-1), or stay (0)

    armVectors = 0  # This is used to determine where the Paddle will teleport to
                    # if two calls were made within the FAST_SEQUENCE_THRESHOLD

    sock = socket.socket(socket.AF_INIT, socket.SOCK_DGRAM) # create a socket
    
    sock.connect((IPADDR, PORTNUM)) # connect socket to server

    '''
    Purpose: This is method is called by signal filtering script to map the EMG
    values to position in the Pong video game and to send the respective UDP
    packet to the Pong server.
    '''
    @staticmethod
    def changePosition(leftVal, rightVal, time):

        # determine movement vector from input values
        if (leftVal > ANALOG_VAL_THRESHOLD and rightVal > \
                ANALOG_VAL_THRESHOLD):
            vector = 0
        elif (leftVal > ANALOG_VAL_THRESHOLD):
            vector = 1
        elif (rightVal > ANALOG_VAL_THRESHOLD):
            vector = -1
        else:
            vector = 0
        
        # update time values with new time at which this method was called to
        # move the paddle
        if (vector != 0):
            times[1] = times[0]
            times[0] = time
        
        # update armVectors sum
        armVectors += vector

        # if this method is called back to back to change the paddle within the
        # FAST_SEQUENCE_THRESHOLD, we perform a teleportation.
        if (times[0] - times[1] < FAST_SEQUENCE_THRESHOLD):

            if (armVectors == 0): # if right->left or left->right, go to middle
                position == MIDDLE
            elif (armVectors == -2): # if right->right, go to bottom
                position == LOWER_LIM
            else:                    # if left->left, go to top
                position == UPPER_LIM

        # if not performing teleportation, move position in vector's direction
        else:
            position = position + vector * DELTA

        # if armsVector reaches two, reset back to zero
        if (armsVector == -2 or armsVector == 2):
            armsVector = 0

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
        
        # send hex decoded integer to Pong server
        sock.sendTo( hex(position * AXIS_SCALAR) )
