import os
import numpy as np
import matplotlib.pyplot as plt
import GMR.InputOutput as io

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


def normalise_file_size(number_files,
                        image_save=False):
    '''
    Calculates the total file size output for normalising images and
    processing a data cube.
    Args:
        number_files: <int> number of files to process
        image_save: <bool> if images are saved set True
    '''
    file_size = (0.00775 * number_files) - 0.00578

    if image_save:
        file_size = (0.00794 * number_files) - 0.00578

    file_size = round(file_size, 2)
    return file_size


def normalise_process_time(number_files,
                           image_save=False):
    '''
    Calculates the total processing time for normalising images
    and processing a data cube.
    Args:
        number_files: <int> number of files to process
        image_save: <bool> if images are saved set True
    '''
    process_time = -0.3+(2.5*np.exp((number_files-173.2)/324.3))

    if image_save:
        process_time = -3.7+(2.9*np.exp((number_files+290.5)/421.9))

    process_time = round(process_time, 1)
    return process_time

def processing_parameters(main_dir,
                          exp_settings,
                          image_save=False):
    '''
    Calculate the total processing time based on the number of files
    present in each hs_img. Give the option to output a time for
    both image output and data output.
    '''
    no_files = []
    for hs_img in exp_settings['hs_imgs']:
        img_dir = os.path.join(main_dir, hs_img)
        if not os.path.isdir(img_dir):
            continue

        data_files = io.extract_files(dir_name=img_dir,
                                      file_string='img_')
        no_files.append(len(data_files))

    number_files = sum(no_files)
    process_time = normalise_process_time(number_files,
                                          image_save)
    file_size = normalise_file_size(number_files,
                                    image_save)

    print(f'\nTotal Number Of Files: {number_files}')
    print(f'Image Save Set To: {image_save}')
    print(f'Total File Size Approximately: {file_size} GB')
    print(f'\nImage Save Set To: {image_save}')
    print(f'Total Processing Time Approximately: {process_time} mins')



if __name__ == '__main__':

    number_files = [100, 200, 300, 400, 500, 600, 700, 800]
    image_save = [True, False]
    for files in number_files:
        for save in image_save:
            file_size = normalise_file_size(files, image_save=save)
            process_time = normalise_process_time(files, image_save=save)
