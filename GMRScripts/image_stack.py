import os
import numpy as np
import matplotlib.pyplot as plt
import GMRScripts.organisation_functions as org
from shutil import copy


def FindImgSize(dir_name, file_string):
    '''
    Find size of an individual image from the hyperspectral imaging file,
    used to determine the pixel size of the camera. Find the height and
    width of each image and outputs the number of rows and columns as
    variables.
    Args:
        dir_name: string directory name containing images
        file_string: string image names within directory (eg. IMG_, .csv)
    '''
    data_files = org.ExtractFiles(dir_name=dir_name,
                                  file_string=file_string)
    zero_data = data_files[0]
    zero = os.path.join(dir_name, zero_data)
    zero_file = np.load(zero)

    return np.shape(zero_file)


def RowStack(dir_name,
             file_string,
             row,
             pixel_stack_dir_pngs,
             pixel_stack_dir,
             saveout=True,
             showFig=False,
             saveFig=False):
    '''
    Stacks the corrected image files as a row group and plots wavelength
    against column on a colour plot with the colour representing the
    intensity.
    If the lines across the graphs look smooth then the film is even.
    Args:
        dir_name: string directory name containing corrected image files
        file_string: string to search for corrected image files
        row: row number within pixels (can be iterated over)
        pixel_stack_dir_pngs: string directory for pixel figures
        pixel_stack_dir: string directory for pixel arrays
        saveout: bool saves numpy array and moves to pixel_stack_dir
                 directory
        show: bool show colour plot
        save: bool saves colour plot and moves to pixel_stack_dir_pngs
              directory
    '''
    data_files = org.ExtractFiles(dir_name=dir_name,
                                  file_string=file_string)

    row_stack = []
    for selected_file in data_files:
        file = np.load(os.path.join(dir_name, selected_file))
        row_stack.append(file[row][:])

    if saveout:
        org.ArraySave(array_name=row_stack,
                      file_name=f'row_{row}',
                      dir_name=pixel_stack_dir)

    if showFig or saveFig:
        fig, ax = plt.subplots(1, 1)
        ax.pcolormesh(row_stack,)
        ax.set_title(f'Row {row}', fontsize=18)

        if showFig:
            plt.show()

        if saveFig:
            plt.savefig(f'row_{row}.png')
            org.CheckDirExists(pixel_stack_dir_pngs)
            copy(f'row_{row}.png', pixel_stack_dir_pngs)
            os.remove(f'row_{row}.png')

        fig.clf()
        plt.close(fig)
