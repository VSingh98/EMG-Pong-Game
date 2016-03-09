import serial
import gameloops
from change_mode import *

ser = serial.Serial('/dev/ttyACM0', 115200, timeout = 4)
ser.setDTR(False)
ser.setDTR(True)

while True:            # Need to filter out initial trash
    mode = ser.read()
    if mode.isalpha():
        if mode is 's':
            gameloops.Mapper.init()      # Manually init if directly going to game mode
        break

while True:
    try:
        if mode is 'c':
            try:
                gameloops.calibrate(ser)
                
            except ChangeMode:
                mode = 's'

            ''' UNCOMMENT TO WORK WIHTOUT POTENTIOMETER '''
           # except KeyboardInterrupt:
           #     mode = 's'
            
        else:
            try:
                gameloops.game_loop(ser)

            except:
                raise
            
    except KeyboardInterrupt:
        print 'Cancelling program'
        break
