import os
import numpy as np
import matplotlib.pyplot as plt
from shutil import copy

def pwr_norm(dir_name,
             plot_show=False,
             plot_save=False):
    '''
    Read in and process the power spectrum data file
    Args:
        dir_name: <string> directory path to power spectrum
        plot_show: <bool> if true power spectrum shows
        plot_save: <bool> if true power spectrum is saved
    '''
    power_spectrum = os.path.join(dir_name, 'power_specrum.csv')
    step, wl, f, power = np.genfromtxt(power_spectrum,
                                       delimiter=',',
                                       skip_header=1,
                                       unpack=True)
    max_element = np.amax(power)
    norm_power = power / max_element

    if plot_show or plot_save:

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=[10,7])

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
            plt.savefig('Corrected_Power_Spectrum.png')
            copy('Corrected_Power_Spectrum.png', dir_name)
            os.remove('Corrected_Power_Spectrum.png')

        fig.clf()
        plt.close(fig)

    return step, wl, f, power, norm_power


def bg_norm(image,
            file_name,
            norm_power,
            dir_name,
            plot_show=False,
            plot_save=False):
    '''
    Plot a raw image and corrected image (calculate brightness values
    from pixels mean/std) save corrected image out. Read data values
    in using Pandas.
    Args:
        image: <string> path to csv img file
        file_name: <string> file name without extension
        norm_power: <array> normalised power array
        dir_name: <string> directory path to concatenate corrected
                  image png directory to
        plot_show: <bool> if true raw and corrected image show
        plot_save: <bool> if true raw and corrected image saved
    Returns:
        norm_img: <array> normalised image as numpy array int16
    '''
    file, img_no = file_name.split('_')

    norm_img = (image / norm_power[int(img_no)])
    norm_img *= 1e3 # increase precision for saving as int

    img_vmax = np.mean(image) + (1 * np.std(image))
    img_vmin = np.mean(image) - (1 * np.std(image))

    norm_img_vmax = np.mean(norm_img) + (1 * np.std(norm_img))
    norm_img_vmin = np.mean(norm_img) - (1 * np.std(norm_img))

    if plot_save or plot_show:
        fig, (ax1, ax2) = plt.subplots(2, 1)

        ax1.imshow(image,
                   cmap=plt.cm.cool,
                   origin='lower',
                   vmax=img_vmax,
                   vmin=img_vmin,
                   aspect='equal')
        ax1.set_title(f'Image {img_no}', fontsize=16)

        ax2.imshow(norm_img,
                   cmap=plt.cm.hot,
                   origin='lower',
                   vmax=norm_img_vmax,
                   vmin=norm_img_vmin,
                   aspect='equal')
        ax2.set_title(f'Normalised Image {img_no}', fontsize=16)

        fig.tight_layout()

        if plot_show:
            plt.show()

        if plot_save:
            out_name = (f'corrected_{file_name}.png')
            out_dir = os.path.join(dir_name, 'corrected_imgs_pngs')
            plt.savefig(out_name)
            copy(out_name, out_dir)
            os.remove(out_name)

        fig.clf()
        plt.close(fig)

    norm_img = (norm_img).astype('int16')
    return norm_img
  

def trim_spec():
    pass


def trim_time():
    pass


def roi():
    pass
