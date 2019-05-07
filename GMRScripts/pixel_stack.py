import os
import numpy as np
import matplotlib.pyplot as plt
from GMRScripts.organisation_functions import Platform, ExtractFiles
from GMRScripts.experiment_settings import ReadInSettings, FindWavSettings
from GMRScripts.free_spectral_range import WavSpace


def PixelStack(wavelength_settings, show=False):
    '''
    Takes in row numpy array files saved previously, reads array column by
    column to give an individual pixel variation as a function of wavelength.

    THIS FUNCTION CURRENTLY OUTPUTS NOTHING AND NEEDS DATA ANALYSIS ADDING
    TO IT SUCH AS FINDING A MAXIMUM, OR USING FREE SPECTRAL RANGE ANALYSIS,
    OR FOURIER TRANSFORMS.

    Args:
        wavelength_settings: array outputted through the find wavelength
                             settings function
        show: bool if true pixel plot will show
    '''

    data_files = ExtractFiles(dir_name=pixel_stack_dir,
                              file_string='row_')

    wavs = WavSpace(wavelength_settings)
    for selected_file in data_files:
        file = os.path.join(pixel_stack_dir, selected_file)
        # file_name = os.path.splitext(file)[0]
        row_stack = np.load(file)
        num_cols = len(row_stack[:, 0])
        for a in range(num_cols):
            pixel_stack = row_stack[:, a]
            fig, ax = plt.subplots(1, 1)
            ax.plot(wavs, pixel_stack)
            if show:
                plt.show()

if __name__ == '__main__':
    # main_dir is equivalent to root, then all directories defined here
    main_dir = Platform()
    sub_dir = os.path.join(main_dir, '220319_to_120419', '100419')
    img_dir = os.path.join(sub_dir, 'test')
    corrected_img_dir = os.path.join(img_dir, 'corrected_imgs')
    corrected_img_dir_pngs = os.path.join(img_dir, 'corrected_imgs_pngs')
    pixel_stack_dir = os.path.join(img_dir, 'pixel_stack')
    pixel_stack_dir_pngs = os.path.join(img_dir, 'pixel_stack_pngs')

    exp_settings = ReadInSettings(img_dir)
    wavelength_settings = FindWavSettings(img_dir)
    PixelStack(wavelength_settings=wavelength_settings, show=False)
