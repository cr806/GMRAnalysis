import os


def ReadInSettings(dir_name):
    '''
    Reads in the experiment settings file outputted from GMRX setup detailing
    the number of images, integration time, initial/final wavelength and step,
    time step and image numbers.
    Args:
        dir_name, string directory containing experiment settings document
    Returns:
        an array containing each line of the experiment settings document
    '''

    exp_settings = {
        'int_time': 0.0,
        'slit': 0.0,
        'wav_i': 0.0,
        'wav_f': 0.0,
        'wav_s': 0.0,
        'time_s': 0,
        'filenames': []
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
        if 'time step' in line.lower():
            exp_settings['time_s'] = int(line.split(':')[1].strip())
        if 'hs_img_' in line.lower():
            exp_settings['filenames'].append(line.split('\t')[0].strip())

    return exp_settings


def FindWavSettings(dir_name):
    '''
    Reads in the experiment settings file outputted from GMRX setups detailing
    the number of images, integration time, initial/final wavelength and step,
    time step and image numbers.
    Args:
        dir_name, string directory containing experiment settings document
    Returns:
        only returns the wavelength initial/final/step parameters
    '''

    my_settings = ReadInSettings(dir_name)

    wavelength_settings = []
    wavelength_settings.append(my_settings[5].split(': ')[1])
    wavelength_settings.append(my_settings[6].split(': ')[1])
    wavelength_settings.append(my_settings[7].split(': ')[1])

    return wavelength_settings


if __name__ == '__main__':
    main_dir = '/Users/chris/Documents/SoftwareDev/Python' \
               '/GMR Analysis Project/Put_Data_Here'

    exp_settings = ReadInSettings(main_dir)
    print(exp_settings)
    # wavelength_settings = FindWavSettings(img_dir)
