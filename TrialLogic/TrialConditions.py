import numpy as np
from enum import Enum


class TrialResult(Enum):
    correct_response = 1
    correct_rejection = 2
    miss = 3
    false_alarm = 4


def lick_detect(lick_data, threshold, percent_accepted):
    # first binarise the data
    lick_response = np.zeros(len(lick_data))
    lick_response[np.where(lick_data > threshold)] = 1

    # then determine percentage responded
    percent_responded = np.sum(lick_response) / len(lick_response)

    # return whether this is accepted as a response or not
    # return whether this is accepted as a response or not
    return percent_responded >= percent_accepted


def trial_result(_rewarded, _response):
    # returns trial result enum, correct bool, timeout bool
    rewarded = _rewarded == 1
    if rewarded == 1 and _response:
        return TrialResult.correct_response, True, False
    elif rewarded == 1 and not _response:
        return TrialResult.miss, False, False
    elif not rewarded and not _response:
        return TrialResult.correct_rejection, True, False
    elif not rewarded and _response:
        return TrialResult.false_alarm, False, True
    else:
        print('unknown trial condition')
        return TrialResult.miss, False, False