import numpy as np

def simple():
    pass


def find_min_wl(spec_list, wl):
    '''
    Finds the minimum wavelength for each spectrum in a list of spectra
    Args:
        spec_list: 2D numpy array from 
        wl: 1D numpy array from InputOutput.get_pwr_spectrum
    Returns
        min_wl: 1D numpy array of minimum wavelengths in spec_list
    '''
    indices =  [np.argmin(spectrum) for spectrum in spec_list]
    min_wl = [wl[i] for i in indices]
    return min_wl

    
def find_max_wl(spec_list, wl):
    '''
    Finds the maximum wavelength for each spectrum in a list of spectra
    Args:
        spec_list: 2D numpy array from 
        wl: 1D numpy array from InputOutput.get_pwr_spectrum
    Returns
        max_wl: 1D numpy array of maximum wavelengths in spec_list
    '''
    indices =  [np.argmax(spectrum) for spectrum in spec_list]
    max_wl = [wl[i] for i in indices]
    return max_wl


def s_fano():
    pass


def d_fano():
    pass


def sd_fano():
    pass


def dd_fano():
    pass
