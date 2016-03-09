''' Defines the loop necessary for main game functioning '''

''' Necessary modules '''
from time import sleep, time
from datadd import *
from mapping import *

MAX_SIZE = 200    # Keep about 1 second of data
TOREAD = 10       # Amount to read/send per loop
RATE = 200        # Arduino Read Rate
SEND_RATE = 100   # Rate to send information at
SCALE = RATE/SEND_RATE   # Can only be an integer!
fil_box = scipy.signal.boxcar(50)  # Type of filtering to implement

def game_loop(serial):
    data = ([],[])
    fil_dat = ('init', None)
    
    while True:
        (data, fil_dat) = add_data(data, 10, serial, f_del = fil_dat)
        
        if data[0].size > MAX_SIZE:              # Delete superfluous data
            data = [arr[-MAX_SIZE:] for arr in data]

        smoothed = [scipy.signal.lfilter(fil_box, 1, dat) for dat in data]
            
        for val in range(0,TOREAD/SCALE):             # Push data to send to mapper (Needs calibration!)
            itertime = time()
            Mapper.changePosition(smoothed[0][-TOREAD+(val*SCALE)], smoothed[1][-TOREAD+(val*SCALE)])
            sleep((1/SEND_RATE) - (itertime - time()))

def calibrate(serial):
    data = ([],[])
    fil_dat = ('init', None)

    while True:
        try:
            (data, fil_dat) = add_data(data, 10, serial, f_del = fil_dat)
            arm_norm = [0,0]          # Arm normilization factors (left,right)
            
            if data[0].shape[0] > MAX_SIZE:      # Delete superfluous data
                data = [arr[-MAX_SIZE:] for arr in data]
                
            smoothed = [scipy.signal.lfilter(fil_box, 1, dat) for dat in data]
            
            if smoothed[0].max() > arm_norm[0]:     # Keep track of maximum
                arm_norm[0] = smoothed[0].max()
            if smoothed[1].max() > arm_norm[1]:
                arm_norm[1] = smoothed[1].max()
                
        except ChangeMode:
            norm_write(str(arm_norm[0]), str(arm_norm[1]))
            Mapper.init()
            raise
        
        except KeyboardInterrupt:
            norm_write(str(arm_norm[0]), str(arm_norm[1]))
            Mapper.init()
            raise

def norm_write(lnorm, rnorm):
    with open('lnorm', 'w') as lfile:
        lfile.write(lnorm)
    with open('rnorm', 'w') as rfile:
        rfile.write(rnorm)
