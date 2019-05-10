import os
import numpy as np
from shutil import copy
import pandas as pd


def check_dir_exists(dir_name):
    '''
    Check to see if a directory path exists, if not create one.
    Args:
        dir_name: <string> directory path
    '''
    if os.path.isdir(dir_name) is False:
        os.mkdir(dir_name)


def exp_in():
    '''
    Asigns directory path for all data, allowing user input without
    code file path alterations.
    The current working directory (cwd) will then contain all data to
    be analysed. A directory is created name "Put_Data_Here".
    The function waits for user to place data in the folder e.g.
    "hs_img_000", "power_spectrum.csv", "experimental_settings.txt"
    from GMR X.
    Once data is present, the function returns the "Put_Data_Here"
    directory as the main directory and then directory paths can be
    asigned.
    Args:
        The function requires no arguments but will not work unless data
        is present in the new (created) directory and awaits user input.
    '''
    root = os.getcwd()
    main_dir = os.path.join(root, 'Put_Data_Here')
    check_dir_exists(main_dir)

    while len(os.listdir(main_dir)) == 0:
        print('Place data into "Put_Data_Here" folder with this code')
        print('Once complete, restart code')
        os.sys.exit(0)

    else:
        print('Data present in "Put_Data_Here", ensure it is correct\n')
        input('Press enter to continue...\n')

    print('Data set(s) to be examined:')
    print(os.listdir(main_dir))
    print('\n')
    return main_dir


def create_all_dirs(dir_name):
    '''
    '''
    create_dir = ['corrected_imgs']
    


def file_sort(dir_name):
    '''
    Numerically sort a directory containing a combination of string file names
    and numerical file names
    Args:
        dir_name: <string> directory path
    '''
    return sorted(os.listdir(dir_name))


def extract_files(dir_name, file_string):
    '''
    Stack file names in a directory into an array. Returns data files array.
    Args:
        dir_name: <string> directory path
        file_string: <string> string contained within desired files
    '''
    dir_list = file_sort(dir_name)
    return [a for a in dir_list if file_string in a]


def filename(file_path):
    '''
    Takes a file name path and splits on '/' to obtain only the file name.
    Splits the file name from extension and returns just the user asigned
    file name as a string.
    Args:
        file_name: <string> path to file
    '''
    return os.path.splitext(os.path.basename(file_name))[0]


def raw_in(file_path):
    '''
    Reads in raw csv img file using pandas, with a delimiter (sep). Also
    utilises filename function to determine a file_name, this is
    essentially a method of returning a user given (or system given) file
    name without extension. Returns the img values and the file name.
    Args:
        file_name: <string> file path
    '''
    file_name = filename(file_path)
    img = pd.read_csv(file_name, sep='\t')
    img = img.values
    return img, file_name


def array_in():
    pass


def data_array_out(array_name, file_name, dir_name):
    '''
    Save array as file name in a given directory
    Args:
        array_name: <array> python array to save
        file_name: <string> file name to save out
        dir_name: <string> directory name to copy saved array to
    '''
    check_dir_exists(dir_name)

    file_name = f'(file_name).npy'
    np.save(file_name, array_name)
    copy(file_name, dir_name)
    os.remove(file_name)


def png_out():
    pass


def csv_out():
    pass


def user_in():
    pass


if __name__ == '__main__':
    main_dir = exp_in()
    hs_imgs = os.listdir(main_dir)

    for hs_img in hs_imgs:
        img_dir = os.path.join(main_dir, hs_img)

        if not os.path.isdir(img_dir):
            continue

        print(img_dir)
        print(os.listdir(img_dir))
