from daqface import DAQ as daq
import numpy as np


def check_beam(device, channels, beam_channel):
    try:
        check = daq.ThreadSafeAnalogInput(device, channels, 1000, 0.1)
        analog_data = check.DoTask()

        check_mean = np.mean(analog_data[beam_channel])
        return check_mean < 1
    # TODO - need to check if this version is thread / repeat safe. Try/Except is for extra caution
    except:
        return False