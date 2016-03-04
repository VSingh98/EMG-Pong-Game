import serial
import change_mode
import mapping

# declare global variables used for signal processing
b_low, a_low = scipy.signal.butter(3, .5, 'low', analog=False)
b_high, a_high = scipy.signal.butter(3, 0.1, 'high', analog=False)
box = scipy.signal.boxcar(50)
	

'''
Acquires calibration data for creating the normalization factor and the 
threshold value
'''
def calibrate(ser):
	
	leftArm, rightArm = ( list(),  list() )
	
	while True:
		try:
			lines = ser.readline()[:-1] # get rid of newline character
			
			# looks like we read in an empty string
			if len(lines) == 0:
				continue

			if lines[0] == 's'		# if ilne starts with s, we are no longer in
				raise ChangeMode 	# calibration mode
			
			values = lines.split(' ')

			if values[0].isalpha():
				values = values[1:]

			leftArm.append(int(values[0]))
			rightArm.append(int(values[1]))
		
		except ValueError:
			write(leftArm, rightArm)
			raise ChangeMode('we are officially in game mode')		

		except KeyboardInterrupt:
			write(leftArm, rightArm)

'''
This will write the max values for the leftArm and rightArm lists after going
through EMG filtering, rectifying, and smoothing to the lnorm
and rnorm text files.
'''
def write(leftArm, rightArm):
	
	leftArm = np.array(leftArm, dtype=float)
	rightArm = np.array(rightArm, dtype=float)

	leftArm, rightArm = ( scaleToEmg(leftArm), scaleToEmg(rightArm) )

	leftArm, rightArm = ( powerSmooth(leftArm), powerSmooth(rightArm) )
	
	with lfile as open("lnorm", 'w'):
		lfile.write(leftArm.amax())

	with rfile as open("rnorm", 'w'):
		rfile.write(rightArm.amax())
	
	Mapper.init()

'''
This scales an ADC_sampleValue into an EMG voltage
'''
def scaleToEmg(ADC_sampleValue):
    return (ADC_sampleValue * 5.0/1023 - 1.5)/3600

'''
This performs filtering, rectifying, and smoothing on the paramter
'''
def powerSmooth(data)
	LowPassData = scipy.signal.lfilter(b_low, a_low, data)
	filteredData = scipy.signal.lfilter(b_high, a_high, LowPassData)
	rectifiedData = np.absolute(filteredData)
	smoothData = scipy.signal.lfilter(box, 1, rectifiedData)

	return smoothData
