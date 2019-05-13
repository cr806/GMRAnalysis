import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


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


def check_dir_exists(dir_name):
    '''
    Check to see if a directory path exists, if not create one.
    Args:
        dir_name: <string> directory path
    '''
    if os.path.isdir(dir_name) is False:
        os.mkdir(dir_name)


def exp_in(dir_name):
    '''
    Reads in the experiment settings file outputted from GMRX setup detailing
    the number of images, integration time, initial/final wavelength and step,
    time step and image numbers.
    Args:
        dir_name: <string> directory containing experiment settings document
    Returns:
        an array containing each line of the experiment settings document
    '''

    exp_settings = {
        'int_time' : 0.0,
        'slit' : 0.0,
        'wav_i' : 0.0,
        'wav_f' : 0.0,
        'wav_s' : 0.0,
        'time_s' : 0,
        'hs_imgs': []
    }

    with open(os.path.join(dir_name, 'experiment_settings.txt'), 'r') as exp:
        lines = exp.readlines()

    for line in lines:
        if not line.strip():
            continue
        if 'integration time' in line.lower():
            exp_settings['int_time'] = float(line.split(':')[1].strip())
        if 'slit widths' in line.lower():
            exp_settings['slit'] = int(line.split(':')[1].strip())
        if 'initial wavelength' in line.lower():
            exp_settings['wav_i'] = float(line.split(':')[1].strip())
        if 'final wavelength' in line.lower():
            exp_settings['wav_f'] = float(line.split(':')[1].strip())
        if 'wavelength step' in line.lower():
            exp_settings['wav_s'] = float(line.split(':')[1].strip())
        #if 'time step' in line.lower():
        #    exp_settings['time_s'] = int(line.split(':')[1].strip())
        if 'hs_img_' in line.lower():
            exp_settings['hs_imgs'].append(line.split('\t')[0].strip())

    return exp_settings


def get_pwr_spectrum(dir_name,
                     plot_show=False,
                     plot_save=False):
    '''
    Read in and process the power spectrum data file
    Args:
        dir_name: <string> directory path to power spectrum
        plot_show: <bool> if true power spectrum shows
        plot_save: <bool> if true power spectrum is saved
    '''
    power_spectrum = os.path.join(dir_name, 'power_spectrum.csv')
    step, wl, f, power = np.genfromtxt(power_spectrum,
                                       delimiter='\t',
                                       skip_header=1,
                                       unpack=True)
    max_element = np.amax(power)
    norm_power = power / max_element

    if plot_show or plot_save:

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=[10, 7])

        ax1.plot(wl, power, 'b', lw=2, label='Power Spectrum')
        ax1.grid(True)
        ax1.legend(frameon=True, loc=0, ncol=1, prop={'size': 10})
        ax1.set_xlabel("Wavelength [nm]", fontsize=14)
        ax1.set_ylabel("Power [au]", fontsize=14)
        ax1.set_title("Power Spectrum", fontsize=18)

        ax2.plot(wl, power/norm_power, 'r', lw=2,
                 label='Corrected Power Spectrum')
        ax2.grid(True)
        ax2.legend(frameon=True, loc=0, ncol=1, prop={'size': 10})
        ax2.set_xlabel("Wavelength [nm]", fontsize=14)
        ax2.set_ylabel("Corrected Power [au]", fontsize=14)
        ax2.set_title("Corrected Power Spectrum", fontsize=18)

        fig.tight_layout()
        if plot_show:
            plt.show()
        if plot_save:
            out_name = 'Corrected_Power_Spectrum.png'
            out_path = os.path.join(dir_name, out_name)
            plt.savefig(out_path)

        fig.clf()
        plt.close(fig)

    return step, wl, f, power, norm_power


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


def get_filename(file_path):
    '''
    Takes a file name path and splits on '/' to obtain only the file name.
    Splits the file name from extension and returns just the user asigned
    file name as a string.
    Args:
        file_name: <string> path to file
    '''

    return os.path.splitext(os.path.basename(file_path))[0]


def csv_in(file_path):
    '''
    Reads in raw csv img file using pandas, with a delimiter (sep). Also
    utilises filename function to determine a file_name, this is
    essentially a method of returning a user given (or system given) file
    name without extension. Returns the img values and the file name.
    Args:
        file_name: <string> file path
    '''
    file_name = get_filename(file_path)
    img = pd.read_csv(file_path, sep='\t')
    img = img.values
    return img, file_name


def array_in(file_path, mode):
    '''
    Loads in numpy array using the mmap_mode specified in args. Also
    brings in the file name using get_filename function.
    Args:
        file_path: <string> file path string
        mode: <mmap_mode> None, 'r+', 'r', 'w+', 'c'
    '''
    corrected_img = np.load(file_path, mmap_mode=mode)
    file_name = get_filename(file_path)
    return corrected_img, file_name


def array_out(array_name, file_name, dir_name):
    '''
    Save array as file name in a given directory
    Args:
        array_name: <array> python array to save
        file_name: <string> file name to save out
        dir_name: <string> directory name to copy saved array to
    '''
    check_dir_exists(dir_name)

    file_name = f'{file_name}.npy'
    file_path = os.path.join(dir_name, file_name)

    np.save(file_path, array_name)


def png_out(image_data,
            file_name,
            dir_name,
            image_title,
            out_name,
            plot_show=False):
    '''
    Save array as png image at file name in a given directory
    Args:
        array_name: <array> python array to save
        file_name: <string> file name to save out
        dir_name: <string> directory name to copy saved array to
    '''
    img_vmax = np.mean(image_data) + (1 * np.std(image_data))
    img_vmin = np.mean(image_data) - (1 * np.std(image_data))

    fig, ax1 = plt.subplots(1, 1)

    ax1.imshow(image_data,
               cmap=plt.cm.cool,
               origin='lower',
               vmax=img_vmax,
               vmin=img_vmin,
               aspect='equal')
    ax1.set_title(image_title, fontsize=16)

    fig.tight_layout()

    if plot_show:
        plt.show()

    out_dir = os.path.join(dir_name, 'corrected_imgs_pngs')
    out_path = os.path.join(out_dir, out_name)
    plt.savefig(out_path)

    fig.clf()
    plt.close(fig)


def csv_out():
    '''
    Save array as human-readable CSV file at file name in a given directory
    Args:
        array_name: <array> python array to save
        file_name: <string> file name to save out
        dir_name: <string> directory name to copy saved array to
    '''
    pass


def user_in():
    pass


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
