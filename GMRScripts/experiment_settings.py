import os
import GMRScripts.organisation_functions as org


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
    with open(os.path.join(dir_name, 'experiment_settings.txt', 'r')) as exp_settings:
        lines = exp_settings.readlines()

    my_settings = []
    for line in lines:
        my_settings.append(line)
        print(line)

    return my_settings


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
    # main_dir is equivalent to root,
    # then all directories defined here.
    main_dir = org.Platform()
    sub_dir = os.path.join(main_dir, '220319_to_120419', '100419')
    img_dir = os.path.join(sub_dir, 'test')
    corrected_img_dir = os.path.join(img_dir, 'corrected_imgs')
    corrected_img_dir_pngs = os.path.join(img_dir, 'corrected_imgs_pngs')
    pixel_stack_dir = os.path.join(img_dir, 'pixel_stack')
    pixel_stack_dir_pngs = os.path.join(img_dir, 'pixel_stack_pngs')

    exp_settings = ReadInSettings(img_dir)
    wavelength_settings = FindWavSettings(img_dir)
