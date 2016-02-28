#-----------------------------------------------------------------
# HELPER FUNCTIONS
#-----------------------------------------------------------------
# NEEDED MODULES
#------------------------
import numpy
import scipy.signal
import serial
#------------------------

## add_data(dataout, amount_to_add, sourcefile, f_del = None, dchk = False)
## Used to add a certain amount of data to a specific dataout input
## Returns a tuple with updated information
## Optional arguments include an initial value check and filtering constants
def add_data(dataout, amount_to_add, sourcefile, **args):
    flag = args.get('dchk', False)
    (new_tdata, new_ampdata, new_ampdata2) = (vals for vals in dataout)
    (temp_t, temp_a, temp_a2) = (numpy.array([]) for pos in range(len(dataout)))
    if type(sourcefile) is not 'file':
        if flag:
            while sourcefile.read() != 's':
                continue
        for vals in range(0,int(amount_to_add)):
            while True:
                lines = sourcefile.readline()
                try:                                              # Remove trash/initial values
                    if len(lines.split(' '))<3:
                        raise ValueError('Not enough values')
                    f_value = [float(values) for values in lines.strip('\n').split(' ')]
                except:
                    continue
                break
            temp_t = numpy.append(temp_t, f_value[0]/1000000)
            temp_a = numpy.append(temp_a, (f_value[1]*.0049-1.5)/3600)
            temp_a2 = numpy.append(temp_a2, (f_value[2]*0.0049-1.5)/3600)
    else:
        for vals in range(0,int(amount_to_add)):
            lines = sourcefile.readline()
            f_value = [float(values) for values in lines.split(' ')]
            temp_t = numpy.append(temp_t, f_value[0]/1000000)
            temp_a = numpy.append(temp_a, (f_value[1]*.0049-1.5)/3600)
            temp_a2 = numpy.append(temp_a2, (f_value[2]*0.0049-1.5)/3600)
    if 'f_del' in args:
        b_hi, a_hi = scipy.signal.butter(3, 0.1, 'high', analog = False)
        b_lo, a_lo = scipy.signal.butter(3, 0.5, 'low', analog = False)
        if args['f_del'][0] is 'init':                             # Init Scheme
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
            temp_a, fil_z[1] = scipy.signal.lfilter(b_lo,a_lo, temp_a, zi = fil_z[1])
            temp_a = numpy.absolute(temp_a)
            temp_a2, fil_z[2] = scipy.signal.lfilter(b_hi, a_hi, temp_a2, zi = fil_z[2])
            temp_a2, fil_z[3] = scipy.signal.lfilter(b_lo, a_lo, temp_a2, zi = fil_z[3])
            temp_a = numpy.absolute(temp_a)
    new_tdata = numpy.append(new_tdata, temp_t)
    new_ampdata = numpy.append(new_ampdata, temp_a)
    new_ampdata2 = numpy.append(new_ampdata2, temp_a2)
    if 'f_del' in args:
        return (new_tdata,(new_ampdata,new_ampdata2),fil_z)
    else:
        return (new_tdata,(new_ampdata, new_ampdata2))
