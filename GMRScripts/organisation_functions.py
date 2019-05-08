import os
import sys
import platform
import numpy as np
from shutil import copy


def Platform():
    '''
    Determines the directory path based on which operating system the user is
    using. This is only relevant if you use two different operating systems.
    Returns main directory as a path.
    Args:
        No required args but does require user input to determine the directory
        path you wish to use.
    '''
    if platform.system() == 'Windows':
        os.system('cls')
        main_dir = os.path.join('C:/'
                                'Users',
                                'joshs',
                                'Documents',
                                'Masters_Project')

    if platform.system() == 'Linux' or platform.system() == 'Darwin':
        os.system('clear')
        main_dir = os.path.join('media',
                                'mass_storage',
                                'josh',
                                'Documents',
                                'Masters_Project')

    return main_dir


def FileSort(dir_name):
    '''
    Numerically sort a directory containing a combination of string file names
    and numerical file names
    Args:
        dir_name, string with directory path
    '''
    return sorted(os.listdir(dir_name))


def ExtractFiles(dir_name, file_string):
    '''
    Stack file names in a directory into an array. Returns data files array.
    Args:
        dir_name, string with directory path
        file_string, string within desired file names
    '''
    dir_list = FileSort(dir_name)

    return [a for a in dir_list if file_string in a]


def CheckDirExists(dir_name):
    '''
    Check to see if a directory path exists, and if not create one
    Args:
        dir_name, string directory path
    '''
    if os.path.isdir(dir_name) is False:
        os.mkdir(dir_name)


def ArraySave(array_name, file_name, dir_name):
    '''
    Save array as file name in a directory
    Args:
        array_name: python array to save
        file_name: string file name to save array
        dir_name: string directory name to copy saved array to
    '''
    CheckDirExists(dir_name)

    file_name = f'{file_name}.npy'
    np.save(file_name, array_name)
    copy(file_name, dir_name)
    os.remove(file_name)


def UpdateProgress(progress):
    '''
    Function to display to terminal or update a progress bar according to
    value passed.
    Args:
        progress: <float> between 0 and 1. Any int will be converted
                  to a float. Values less than 0 represent a 'Halt'.
                  Values greater than or equal to 1 represent 100%
    '''
    barLength = 50  # Modify this to change the length of the progress bar
    status = " "

    if isinstance(progress, int):
        progress = float(progress)

    if not isinstance(progress, float):
        progress = 0
        status = 'Error: progress input must be float\r\n'

    if progress < 0:
        progress = 0
        status = 'Halt...\r\n'

    if progress >= 1:
        progress = 1
        status = 'Done...\r\n'

    block = int(round(barLength * progress))
    progress_str = '#' * block + '-' * (barLength - block)
    text = f'\rPercent: [{progress_str}] {(progress * 100):.0f}% {status}'
    sys.stdout.write(text)
    sys.stdout.flush()


if __name__ == '__main__':

    # main_dir is equivalent to root, then all directories defined here
    main_dir = Platform()
    sub_dir = os.path.join(main_dir, '220319_to_120419', '100419')
    img_dir = os.path.join(sub_dir, 'test')
    corrected_img_dir = os.path.join(img_dir, 'corrected_imgs')
    corrected_img_dir_pngs = os.path.join(img_dir, 'corrected_imgs_pngs')
    pixel_stack_dir = os.path.join(img_dir, 'pixel_stack')
    pixel_stack_dir_pngs = os.path.join(img_dir, 'pixel_stack_pngs')

    data_files = ExtractFiles(dir_name=img_dir, file_string='img_')
    print(data_files)
