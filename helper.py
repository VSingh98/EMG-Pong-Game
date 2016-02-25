#-----------------------------------------------------------------
# HELPER FUNCTIONS FOR LAB 3
#-----------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig

## data_cutter(datain, timecut, convert = False)
## DATAIN AND TIMECUT ARE REQUIRED ARGUMENTS
def data_cutter(datain, timecut, **args):
    data = np.loadtxt(datain, unpack = True)
    timedata = data[0]/1000000 - data[0].min()/1000000
    where = np.where(timedata>int(timecut)/1000)[0][0]
    if(args.get('convert',False)):
       return (timedata[:where],(data[1][:where]*.0049-1.5)/3600)
    else:
        return (timedata[:where],data[1][:where])

## EMG_plotter(xsize, ysize, (x1data,y1data,appendsub1title = '', appendy1label = '(V)'), ...)
## MAX GRAPHS PLOTTABLE = xsize * ysize plots (limitation set by subplot function)
## May receive any numer of inputs, with appendsubtitle and apendylabel being optional arguments
def EMG_plotter(xsize,ysize,*plots):
    listplots = list(plots)
    num = 1
    for loc in range(0,len(listplots)):
        if(len(listplots[loc])==2):
            listplots[loc] += ('','(V)',)
        elif(len(listplots[loc])==3):
            listplots[loc] += ('(V)',)
    for tuples in listplots:
        plt.subplot(xsize,ysize,num)
        plt.title('EMG SAMPLE DATA '+tuples[2])
        plt.xlabel('Time (s)')
        plt.ylabel('Read Voltage '+tuples[3])
        plt.plot(tuples[0], tuples[1], 'k')
        num += 1

## add_data(dataout, amount_to_add, sourcefile)
## Used to add a certain amount of data to a specific dataout input
## Returns a tuple with updated information (numpy arrays cannot be directly transformed)
def add_data(dataout, amount_to_add, sourcefile, **args):
    new_tdata, new_ampdata = dataout
    temp_t, temp_a = (np.array([]), np.array([]))
    if(args.get('serialsource',False)):
        for vals in range(0,int(amount_to_add)):
            lines = ''
            while(True):
                lines += sourcefile.read()
                if(lines[-1] == '\n'):
                    break
            f_value = [(float(values)) for values in lines.strip('\n').split(' ')]
            temp_t = np.append(temp_t, f_value[0]/1000000)
            temp_a = np.append(temp_a, (f_value[1]*.0049-1.5)/3600)
    else:
        for vals in range(0,int(amount_to_add)):
            lines = sourcefile.readline()
            f_value = [float(values) for values in lines.split(' ')]
            temp_t = np.append(temp_t, f_value[0]/1000000)
            temp_a = np.append(temp_a, (f_value[1]*.0049-1.5)/3600)
    if(args.get('filterdat',False)):
        b_hi, a_hi = sig.butter(3, 0.1, 'high', analog = False)
        b_lo, a_lo = sig.butter(3, 0.5, 'low', analog = False)
        if 'f_del' not in args:
            print('No filter delay was specified, Defaulting to non-filter routine')
        elif 'f_del' in args and args['f_del'][0] is 'init':        # Init Scheme
            fil_z = [sig.lfiltic(b_hi,a_hi, np.zeros_like(a_hi)), sig.lfiltic(b_lo,a_lo, np.zeros_like(a_lo))]
            temp_a, fil_z[0] = sig.lfilter(b_hi, a_hi, temp_a, zi = fil_z[0])
            temp_a, fil_z[1] = sig.lfilter(b_lo, a_lo, temp_a, zi = fil_z[1])
            temp_a = np.absolute(temp_a)
        else:                                                      # Otherwise run this
            fil_z = list(args['f_del'])
            temp_a, fil_z[0] = sig.lfilter(b_hi, a_hi, temp_a, zi = fil_z[0])
            temp_a, fil_z[1] = sig.lfilter(b_lo,a_lo, temp_a, zi = fil_z[1])
            temp_a = np.absolute(temp_a)
    new_tdata = np.append(new_tdata, temp_t)
    new_ampdata = np.append(new_ampdata, temp_a)
    if 'fil_z' in locals():
        return (new_tdata,new_ampdata, fil_z)
    else:
        return (new_tdata, new_ampdata)
