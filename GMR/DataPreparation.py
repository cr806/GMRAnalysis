import os
import numpy as np


def pwr_norm(dir_name):
    '''
    Read in and process the power spectrum data file
    Args:
        dir_name: <string> directory path to power spectrum
    '''
    power_spectrum = os.path.join(dir_name, 'power_specrum.csv')
    step, wl, f, power = np.genfromtxt(power_spectrum,
                                       delimiter=',',
                                       skip_header=1,
                                       unpack=True)
    max_element = np.amax(power)
    norm_power = power / max_element
    return step, wl, f, power, norm_power


def bg_norm():
    pass


def trim_spec():
    pass


def trim_time():
    pass


def roi():
    pass
