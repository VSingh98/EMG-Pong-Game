' Defines the loop necessary for main game functioning '

' Necessary modules '
from time import sleep, time
from datadd import *
from mapping import *

MAX_SIZE = 200    # Keep about 1 second of data
TOREAD = 10       # Amount to read/send per loop
RATE = 200        # Read rate of Arduino (Hz)

fil_box = scipy.signal.boxcar(50)  # Type of filtering to implement

def game_loop(serial):
    data = ([],[])
    fil_dat = ('init', None)
    
    while True:
        (data, fil_dat) = add_data(data, 10, serial, f_del = fil_dat)
        
        if data[0].size > MAX_SIZE:              # Delete superfluous data
            data = [arr[-MAX_SIZE:] for arr in data]
            print data

        smoothed = scipy.signal.lfilter(fil_box, 1, data, axis = 0)
            
        for val in range(0,TOREAD):
            itertime = time()
            Mapper.changePosition(smoothed[0][-TOREAD+val], smoothed[1][-TOREAD+val])
            sleep(1/RATE - (itertime - time()))

def calibrate(serial):
    data = ([],[])
    fil_dat = ('init', None)

    while True:
        try:
            (data, fil_dat) = add_data(data, 10, serial, f_del = fil_dat)
            arm_norm = [0,0]          # Arm normilization factors (left,right)
            
            if data[0].shape[0] > MAX_SIZE:
                data = [arr[-MAX_SIZE:] for arr in data]
                
            smoothed = scipy.signal.lfilter(fil_box, 1, data, axis = 0)
            
            if data[0].max() > arm_norm[0]:
                arm_norm[0] = data[0].max()
            if data[1].max() > arm_norm[1]:
                arm_norm[1] = data[1].max()

            'For debugging purposes only'
            #sleep(0.5)
                
        except ChangeMode:
            norm_write(str(arm_norm[0]), str(arm_norm[1]))
            Mapper.init()
            raise
        except KeyboardInterrupt:
            norm_write(str(arm_norm[0]), str(arm_norm[1]))
            raise

def norm_write(lnorm, rnorm):
    with open('lnorm', 'w') as lfile:
        lfile.write(lnorm)
    with open('rnorm', 'w') as rfile:
        rfile.write(rnorm)
