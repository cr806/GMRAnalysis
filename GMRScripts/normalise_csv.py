import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import GMRScripts.organisation_functions as org
from shutil import copy


def ReadInPwr(file_name):
    '''
    Read in and process the power spectrum data file
    Args:
        file_name, string file path
    '''
    pwr_spec = os.path.join(file_name, 'power_spectrum.csv')
    step, wl, f, power = np.genfromtxt(pwr_spec,
                                       delimiter=',',
                                       skip_header=1,
                                       unpack=True)
    max_element = np.amax(power)
    norm_power = power / max_element

    return step, wl, f, power, norm_power


def PlotDouble(wl, power, norm_power, show=False, save=False):
    '''
    Plot power spectrum and corrected power spectrum
    Args:
        show, bool determines if plot is shown
        save, bool determines if plot is saved
    '''
    if show or save:
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=[10, 7])

        ax1.plot(wl, power, 'b', lw=2, label='Power Spectrum')
        ax1.grid(True)
        ax1.legend(frameon=True, loc=0, ncol=1, prop={'size': 10})
        ax1.set_xlabel("Wavelength [nm]", fontsize=18)
        ax1.set_ylabel("Power [au]", fontsize=18)
        ax1.set_title("Power Spectrum", fontsize=20)

        ax2.plot(wl, power/norm_power, 'r', lw=2,
                 label='Corrected Power Spectrum')
        ax2.grid(True)
        ax2.legend(frameon=True, loc=0, ncol=1, prop={'size': 10})
        ax2.set_xlabel("Wavelength [nm]", fontsize=18)
        ax2.set_ylabel("Corrected Power [au]", fontsize=18)
        ax2.set_title("Corrected Power Spectrum", fontsize=20)

        fig.tight_layout()
        if show:
            plt.show()
        if save:
            plt.savefig('Corrected_Power_Spectrum.png')

        fig.clf()
        plt.close(fig)


def Filename(file_name):
    '''
    Takes a file name path and splits on the '/' to obtain only the file name.
    Then splits the file name and returns just the file name without an
    extension. Returns name string.
    Args:
        file_name, path to the file name you want to obtain
    '''

    return os.path.splitext(os.path.basename(file_name))[0]


def PlotCorrectedImage(file_name,
                       out_name,
                       img_dir,
                       norm_power,
                       save_out=True,
                       plot_save=False,
                       plot_show=False):
    '''
    Plot a raw image and corrected image (calculate brightness
    values from pixels mean/std) save corrected image out
    '''
    corrected_img_dir = img_dir
    corrected_img_dir_pngs = f'{corrected_img_dir}_pngs'

    file, img_no = Filename(file_name).split('_')

    img = np.genfromtxt(file_name, delimiter='\t')

    norm_img = (img / norm_power[int(img_no)])
    norm_img *= 1e3  # increase precision for saving as int

    img_vmax = np.mean(img) + (1 * np.std(img))
    img_vmin = np.mean(img) - (1 * np.std(img))
    norm_img_vmax = np.mean(norm_img) + (1 * np.std(norm_img))
    norm_img_vmin = np.mean(norm_img) - (1 * np.std(norm_img))

    if save_out:
        org.ArraySave((img / norm_power[0]).astype('int16'),
                      out_name,
                      corrected_img_dir)

    if plot_save or plot_show:
        fig, (ax1, ax2) = plt.subplots(2, 1)

        ax1.imshow(img,
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
            plt.savefig(f'{out_name}.png')
            org.CheckDirExists(corrected_img_dir_pngs)
            copy(f'{out_name}.png', corrected_img_dir_pngs)
            os.remove(f'{out_name}.png')

        fig.clf()
        plt.close(fig)


def PlotCorrectedImagePanda(file_name,
                            out_name,
                            img_dir,
                            norm_power,
                            save_out=True,
                            plot_save=False,
                            plot_show=False):
    '''
    Plot a raw image and corrected image (calculate brightness
    values from pixels mean/std) save corrected image out.  Read
    data in using Pandas
    '''
    corrected_img_dir = img_dir
    corrected_img_dir_pngs = f'{corrected_img_dir}_pngs'

    file, img_no = Filename(file_name).split('_')

    img = pd.read_csv(file_name, sep=',')

    img = img.values

    norm_img = (img / norm_power[int(img_no)])
    norm_img *= 1e3  # increase precision for saving as int

    img_vmax = np.mean(img) + (1 * np.std(img))
    img_vmin = np.mean(img) - (1 * np.std(img))
    norm_img_vmax = np.mean(norm_img) + (1 * np.std(norm_img))
    norm_img_vmin = np.mean(norm_img) - (1 * np.std(norm_img))

    if save_out:
        org.ArraySave((img / norm_power[0]).astype('int16'),
                      out_name,
                      corrected_img_dir)

    if plot_save or plot_show:
        fig, (ax1, ax2) = plt.subplots(2, 1)

        ax1.imshow(img,
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
            plt.savefig(f'{out_name}.png')
            org.CheckDirExists(corrected_img_dir_pngs)
            copy(f'{out_name}.png',
                 corrected_img_dir_pngs)
            os.remove(f'{out_name}.png')

        fig.clf()
        plt.close(fig)
