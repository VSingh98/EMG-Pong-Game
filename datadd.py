#-----------------------------------------------------------------
# HELPER FUNCTIONS
#-----------------------------------------------------------------
# NEEDED MODULES
#------------------------
import numpy
import scipy.signal
import serial
from change_mode import *
#------------------------

b_hi, a_hi = scipy.signal.butter(3, 0.1, 'high', analog = False)
b_lo, a_lo = scipy.signal.butter(3, 0.5, 'low', analog = False)

## add_data(dataout, amount_to_add, sourcefile, f_del = None)
## Used to add a certain amount of data to a specific dataout input
## Returns a tuple with updated information
## Optional filtering with use of f_del arg
def add_data(dataout, amount_to_add, sourcefile, **args):
    (temp_a, temp_a2) = ([],[])
    if type(sourcefile) is not 'file':
        for vals in range(0,int(amount_to_add)):
            while True:
                lines = sourcefile.readline()
                try:                                               # Remove trash data
                    if 's' in lines:
                        raise ChangeMode
                    if len(lines.split(' ')) != 2:
                        raise ValueError('Incorrect Number of Values')
                    f_value = [float(values) for values in lines.strip('\n').split(' ')]
                    break
                except ValueError:
                    print 'val discarded'
                    pass
            temp_a.append((f_value[0]*0.0049-1.5)/3600)
            temp_a2.append((f_value[1]*0.0049-1.5)/3600)
            
            ''' FOR DEBUG PURPOSES ONLY '''
#            temp_a.append(f_value[0]+1)
#            temp_a2.append(f_value[1]+1)

    else:                                                          # READ FROM FILE
        for vals in range(0,int(amount_to_add)):
            lines = sourcefile.readline()
            f_value = [float(values) for values in lines.strip('\n').split(' ')]
            temp_a.append((f_value[0]*0.0049-1.5)/3600)
            temp_a2.append((f_value[1]*0.0049-1.5)/3600)
    temp_a = numpy.array(temp_a)
    temp_a2 = numpy.array(temp_a2)
    if 'f_del' in args:                                            # FILTERING ROUTINE
        if str(args['f_del'][0]) == 'init':                             # Init Scheme
            fil_z = [scipy.signal.lfiltic(b_hi,a_hi, numpy.zeros_like(a_hi)), scipy.signal.lfiltic(b_lo,a_lo, numpy.zeros_like(a_lo)), scipy.signal.lfiltic(b_hi,a_hi,numpy.zeros_like(a_hi)), scipy.signal.lfiltic(b_lo, a_lo,numpy.zeros_like(a_lo))]
            temp_a, fil_z[0] = scipy.signal.lfilter(b_hi, a_hi, temp_a, zi = fil_z[0])
            temp_a, fil_z[1] = scipy.signal.lfilter(b_lo, a_lo, temp_a, zi = fil_z[1])
            temp_a = numpy.absolute(temp_a)
            temp_a2, fil_z[2] = scipy.signal.lfilter(b_hi, a_hi, temp_a2, zi = fil_z[2])
            temp_a2, fil_z[3] = scipy.signal.lfilter(b_lo, a_lo, temp_a2, zi = fil_z[3])
            temp_a2 = numpy.absolute(temp_a2)
        else:                                                      # Otherwise run this
            fil_z = list(args['f_del'])
            temp_a, fil_z[0] = scipy.signal.lfilter(b_hi, a_hi, temp_a, zi = fil_z[0])
            temp_a, fil_z[1] = scipy.signal.lfilter(b_lo, a_lo, temp_a, zi = fil_z[1])
            temp_a = numpy.absolute(temp_a)
            temp_a2, fil_z[2] = scipy.signal.lfilter(b_hi, a_hi, temp_a2, zi = fil_z[2])
            temp_a2, fil_z[3] = scipy.signal.lfilter(b_lo, a_lo, temp_a2, zi = fil_z[3])
            temp_a2 = numpy.absolute(temp_a2)
    new_ampdata = numpy.append(dataout[0], temp_a)
    new_ampdata2 = numpy.append(dataout[1], temp_a2)
    if 'f_del' in args:
        return ((new_ampdata, new_ampdata2), fil_z)
    else:
        return (new_ampdata, new_ampdata2)
