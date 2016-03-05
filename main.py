import serial
import gameloops
from change_mode import *

ser = serial.Serial('/dev/ttyACM1', 115200, timeout = 4)
ser.setDTR(False)
ser.setDTR(True)

while True:            # Need to filter out initial trash
    mode = ser.read()
    if mode.isalpha():
        break

while True:
    try:
        if mode is 'c':
            try:
                gameloops.calibrate(ser)   ## Or feel free to use your function!
                
            except ChangeMode:
                pass
            
        else:
            try:
                gameloops.game_loop(ser)

            except:
                raise
    except KeyboardInterrupt:
        print 'Cancelling program'
        break
