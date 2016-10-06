from daqface import DAQ as daq
import numpy as np
import time


def deliver_reward(ai_device, ao_device, sync_clock, samp_rate, secs):
    on = np.ones((1, int(samp_rate*secs))) * 5.0
    off = np.zeros((1, int(samp_rate/100)))

    vec = np.hstack((on, off))

    reward = daq.AoAiMultiTask(ai_device, 1, ao_device, samp_rate, vec.shape[1]/float(samp_rate), vec, sync_clock)
    out = reward.DoTask()

    return out

# TESTING
# deliver_reward("dev2/ai0", "dev2/ao1", "/dev2/ai/SampleClock", 20000, 0.15)