from daqface import DAQ as daq
import numpy as np


def check_beam(device, channels, beam_channel):
    try:
        check = daq.AnalogInput(device, channels, 1000, 0.1)
        check.DoTask()

        check_mean = np.mean(check.analogRead[beam_channel])
        return check_mean < 1
    # TODO - sloppy, think that constant creating of task causes crashing, this is a bit of a hack
    except:
        return False