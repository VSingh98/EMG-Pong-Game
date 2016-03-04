#! /PATH/TO/PYTHON
import serial
import change_mode

ser = serial.Serial('/dev/ttyACM0', 115200, timeout = 4) 
ser.setDTR(False)
ser.setDTR(True)

with ser:
    while True:
        try:
            if ser.read() == 'c':

                try:
					calibrate(ser)		
                
                except ChangeMode:
                    pass

            else:
                
                try:
                   # call game metohd
                   pass
               
                except ChangeMode:
                    pass 

		except KeyboardInterrupt:
			break;
