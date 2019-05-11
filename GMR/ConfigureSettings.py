import os
import sys


def check_dir_exists(dir_name):
    '''
    Check to see if a directory path exists, if not create one.
    Args:
        dir_name: <string> directory path
    '''
    if os.path.isdir(dir_name) is False:
        os.mkdir(dir_name)


def config_dir_path():
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
    Creates all essential directories required within the code. All sub
    directories are created within the given dir_name.
    Args:
        dir_name: <string) directory path for data
    '''
    create_dir_list = ['corrected_imgs']
    for directory in create_dir_list:
        new_dir = os.path.join(dir_name, directory)
        new_png_dir = os.path.join(dir_name, f'{directory}_pngs')
        check_dir_exists(new_dir)
        check_dir_exists(new_png_dir)


def update_progress(progress):
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
