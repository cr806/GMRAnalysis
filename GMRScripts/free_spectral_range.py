import os
import csv
import numpy as np
import matplotlib.pyplot as plt
import GMRScripts.organisation_functions as org
from scipy.signal import find_peaks
from shutil import copy


def WavSpace(wavelength_settings):
    '''
    Reads in the wavelength parameters contained in wavelength_settings
    (from experiment settings files), and produces the measured wavelength
    as an array
    Args:
        wavelength_settings: <list> 1D array containing wavelength settings
    '''
    wav_i = wavelength_settings['wav_i']
    wav_f = wavelength_settings['wav_f']
    wav_step = wavelength_settings['wav_s']

    wav_difference = wav_f - wav_i
    wav_fraction = wav_difference / wav_step
    number_files = int(wav_fraction + 1)
    wavs = np.linspace(wav_i, wav_f, number_files)

    return wavs


def WavToFreq(wavelength):
    '''
    Converts a single wavelength value (or list of wavelength values)(nm)
    to frequency value(s) (Hz)
    Args:
        wavelength: <int> Wavelength parameter given in nanometers
    '''
    C = 299792458
    nm = 1e-9

    if isinstance(wavelength, float):
        return C / (wavelength * nm)

    if isinstance(wavelength, list):
        return [C / (w * nm) for w in wavelength]


def FreqToWav(frequency):
    '''
    Converts a single frequency value (or list of frequency values)(Hz)
    to wavelength value(s) (nm)
    Args:
        frequency: <int> Frequency parameters give in Hertz
    '''
    C = 299792458
    nm = 1e-9

    if isinstance(frequency, float):
        return (C / frequency) / nm

    if isinstance(frequency, list):
        return [(C / f) / nm for f in frequency]


def FileName(file):
    '''
    Takes a file name path and splits on the '/' to obtain only the file name.
    Then splits the file name and returns just the file name without an
    extension. Returns name string.
    Args:
        file_name: <str> Path to the file name you want to obtain
    '''
    path_string = os.path.splitext(file)[0]
    name_string = os.path.split(path_string)[-1]
    return name_string


def GenParams(wavs, wav_int):
    '''
    Reads in wavelength and intensity values from lists.
    Determines minimum and maximum frequency values and uses these values to
    create an equally spaced frequency step. Uses original converted frequency,
    regularly spaced frequency, and intensity values to create frequency and
    corresponding intensity values at regularly space frequency steps.
    Args:
        wavs: <list> Array of wavelengths
        wav_int: <list> Array of intensities (at wavelengths set out by wavs)
    '''
    irreg_freq = WavToFreq(wavs)
    freq_min = WavToFreq(max(wavs))
    freq_max = WavToFreq(min(wavs))

    freq = np.linspace(freq_min, freq_max, len(wavs))
    freq_int = np.interp(irreg_freq, freq, wav_int)

    return freq, freq_int


def PlotIntensity(wavs,
                  wav_int,
                  freq,
                  freq_int,
                  file_name,
                  pixel_stack_dir_pngs,
                  show=False,
                  save=False):
    '''
    Plots intensity as a function of wavelength and regularly spaced frequency
    values, can save or show graph depending on fiven args.
    Args:
        wavs: <list> Array of wavelengths
        wav_int: <list> Array of intensities (at wavelengths set out by wavs)
        freq: <list> Array of frequencies
        freq_int: <list> Array of intensities (at frequencies set out by freqs)
        file_name: <str> Filename for saving without extension
        pixel_stack_dir_name: <str> Directory for saving pixel stacks
        show: <bool> Show the graph plot
        save: <bool> Save the graph plot
    '''
    if show or save:
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=[10, 7])

        ax1.plot(wavs, wav_int, 'b', lw=2, label=file_name)
        ax1.grid(True)
        ax1.legend(frameon=True, loc=0, ncol=1, prop={'size': 10})
        ax1.set_xlabel("Wavelength [nm]", fontsize=18)
        ax1.set_ylabel("Intensity [au]", fontsize=18)
        ax1.set_title("Intensity As Function Of Wavelength", fontsize=20)

        ax2.plot(freq, freq_int, 'r', lw=2, label=file_name)
        ax2.grid(True)
        ax2.legend(frameon=True, loc=0, ncol=1, prop={'size': 10})
        ax2.set_xlabel("Frequency [Hz]", fontsize=18)
        ax2.set_ylabel("Intensity [au]", fontsize=18)
        ax2.set_title("Intensity As Function Of Frequency", fontsize=20)

        fig.tight_layout()

        if show:
            plt.show()

        if save:
            plt.savefig(f'{file_name}.png')
            org.CheckDirExists(pixel_stack_dir_pngs)
            copy(f'{file_name}.png', pixel_stack_dir_pngs)
            os.remove(f'{file_name}.png')

        fig.clf()
        plt.close(fig)


def FindPeaks(x, y):
    '''
    Find peaks in an array defined as having a height heigher than the
    mean value. Use those peak values to find the corresponding x-axis
    value. Returns x-axis values as an array.
    Args:
        x: <list> X-axis coordinate array
        y: <list> Y-axis coordinate array
    '''

    peak_coords, _ = find_peaks(y,
                                height=(sum(y)/len(y)),
                                distance=10,
                                width=1)
    return [x[peak] for peak in peak_coords]


def FreeSpectralRange(x, thickness, theta, wavelength=False, frequency=False):
    '''
    Find the free spectral range (peak distance) between consecutive peaks and
    uses a standard equation (fabry perot free spectral range) equation to then
    calculate the refractive index of the pixel.
    Args:
        x: <list> Frequency or wavelength array
        thickness: <int> Thickness of film in nanometers
        theta: <int> Angle of incidence in degrees
        wavelength: <bool> If x is a wavelength array set to True
        frequency: <bool> If x is a frequency array set to True
    '''

    # WHAT HAPPENS IF BOTH WAVELENGTH AND FREQUENCY ARE SET TO TRUE?
    C = 299792458
    nm = 1e-9
    L = thickness * nm
    costheta = np.cos(theta * (np.pi / 180))

    delta = [(x[a + 1] - x[a]) for a in range(len(x) - 1)]

    n_array = []
    if wavelength:
        for b in range(len(delta)):
            lambda_0 = x[b] * nm
            n_array.append((((lambda_0 * lambda_0) /
                             (delta[b] * nm)) - lambda_0) /
                           (2 * L * costheta))
        return n_array

    if frequency:
        for b in range(len(delta)):
            n_array.append(C / (2 * delta[b] * L * costheta))
        return n_array


def AverageRefIndex(wav_n, freq_n):
    '''
    Finds the average refractive index value from free spectral range
    calculations for both wavelength and regularly spaced frequency space.
    Args:
        wav_n: <list> Array containing all values of refractive index
               calculated from the wavelength space
        freq_n: <list> Array containing all values of refractive index
                calculated from the frequency space
    '''
    average_n = 0
    if wav_n:
        average_n += (sum(wav_n) / len(wav_n))
    if freq_n:
        average_n += (sum(freq_n) / len(freq_n))
    if wav_n and freq_n:
        average_n = average_n / 2

    return average_n


def WriteRowToFile(outfile_name, array_name):
    '''
    Writes an array (array_name) to a csv file as a single row within that
    file (outfile_name), can be iterated over. CSV file is tab delimited.
    Args:
        outfile_name: <str> Name of the csv file to be written to
        array_name: <str> Name of array to write to each row
    '''
    with open(outfile_name, 'a', newline='') as outfile:
        writer = csv.writer(outfile, delimiter=',')
        writer.writerow([array_name])
