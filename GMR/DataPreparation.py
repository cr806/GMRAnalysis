import os
import numpy as np
import matplotlib.pyplot as plt

def pwr_norm(image_data, file_name, norm_power, dir_name):
    '''
    Plot a raw image and normalised image - use power meter data to
    normalise images.  Normalised image's brightness estimated from
    pixels mean/std.  Optionally save corrected image out. Read data
    values in using Pandas for speed.
    Args:
        image_data: <array> csv image data as 2D array
        file_name: <string> file name without extension
        norm_power: <array> normalised power array
        dir_name: <string> directory path to concatenate corrected
                  image png directory to
    Returns:
        norm_img: <array> normalised image as numpy array int16
    '''
    file, img_no = file_name.split('_')

    norm_img = (image_data / norm_power[int(img_no)])
    norm_img *= 1e3  # increase precision for saving as int

    norm_img = (norm_img).astype('int16')
    return norm_img


def bg_norm(image,
            file_name,
            ROI,
            dir_name,
            plot_show=False,
            plot_save=False):
    '''
    Plot a raw image and normalised image - use the ROI to normalise the
    rest of the image.  Normalised image's brightness estimated from
    pixels mean/std.  Optionally save corrected image out. Read data
    values in using Pandas for speed.
    Args:
        image: <string> path to csv img file
        file_name: <string> file name without extension
        ROI: <tuple> x, y coordinates of ROI to use for BG correction
        dir_name: <string> directory path to concatenate corrected
                  image png directory to
        plot_show: <bool> if true raw and corrected image show
        plot_save: <bool> if true raw and corrected image saved
    Returns:
        norm_img: <array> normalised image as numpy array int16
    '''
    pass


def trim_spec():
    '''
    Calculate which files correspond to which wavelengths are to be
    removed.  Moves to new directory (_NOT_PROCESSED) corresonding numpy
    arrays (or raw csvs).
    '''
    pass


def trim_time():
    '''
    Calculate which directories correspond to the times which are not
    required.  Moves to new directory (_NOT_PROCESSED) unwanted files.
    '''
    pass


def roi():
    '''
    Processes numpy arrays to slice out only wanted ROI, then re-saves
    data for further processing.
    '''
    pass


def reshape_to_spec_lists(hs_data_cube, img_width = 1920, img_height=1080):
    '''
    Reshapes a numpy hyperspectral data cube with axes (lambda, x, y)
    into an array with axes (pixels, lambda) so the spectrum corresponding
    to each pixel can be iterated.
    Args:
        hs_data_cube: 3D numpy array
        img_width: int, width of image in pixels. Optional
        img_height: int, height of image in pixels. Optional
    Returns:
        spec_list: 2D numpy array
    '''
    img_width, img_height = hs_data_cube.shape[1:]
    num_pixels = img_width*img_height
    
    spec_list = np.reshape(hs_data_cube, (num_wavs, num_pixels))
    spec_list = np.transpose(spectra)
    return spec_list

def reshape_to_img(spec_list, img_width = 1920, img_height = 1080)
    '''
    Args:
        spec_list: 1D numpy array
        img_width: int, width of image in pixels. Optional
        img_height: int, height of image in pixels. Optional
    Returns:
        img_array: 2D numpy array
    '''
    img_array = np.reshape(spec_list, (img_width, img_height))
    img_array = np.transpose(img_array)
    return img_array
