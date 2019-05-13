import os
import numpy as np
import matplotlib.pyplot as plt
from shutil import copy


def pwr_norm(image, file_name, norm_power, dir_name,
             plot_show=False, plot_save=False):
    '''
    Plot a raw image and normalised image - use power meter data to
    normalise images.  Normalised image's brightness estimated from
    pixels mean/std.  Optionally save corrected image out. Read data
    values in using Pandas for speed.
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
    norm_img *= 1e3  # increase precision for saving as int

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


def bg_norm(image,
            file_name,
            ROI,
            dir_name,
            plot_show=False,
            plot_save=False):
    '''
    Plot a raw image and normalised image - use the ROI to normalise the
    rest of the image.  Normalised image's brightness estimated from
    pixels mean/std.  Optionally save corrected image out. Read data
    values in using Pandas for speed.
    Args:
        image: <string> path to csv img file
        file_name: <string> file name without extension
        ROI: <tuple> x, y coordinates of ROI to use for BG correction
        dir_name: <string> directory path to concatenate corrected
                  image png directory to
        plot_show: <bool> if true raw and corrected image show
        plot_save: <bool> if true raw and corrected image saved
    Returns:
        norm_img: <array> normalised image as numpy array int16
    '''
    pass


def trim_spec():
    '''
    Calculate which files correspond to which wavelengths are to be
    removed.  Moves to new directory (_NOT_PROCESSED) corresonding numpy
    arrays (or raw csvs).
    '''
    pass


def trim_time():
    '''
    Calculate which directories correspond to the times which are not
    required.  Moves to new directory (_NOT_PROCESSED) unwanted files.
    '''
    pass


def roi():
    '''
    Processes numpy arrays to slice out only wanted ROI, then re-saves
    data for further processing.
    '''
    pass
