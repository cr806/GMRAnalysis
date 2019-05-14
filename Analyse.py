import os
import numpy as np
from pprint import pprint
import GMR.InputOutput as io
import GMR.DataPreparation as dp


root = '/Users/chris/Documents/SoftwareDev/Python/GMR Analysis Project/TEST'
analysis = io.analysis_in_json(root)

for index, experiment in enumerate(analysis["experiments"]):
    print(f'Experiment {index + 1} out of {len(analysis["experiments"])}')
    print(f'Experiment folder: {experiment["dir_name"]}')
    print(f'Experiment path: {experiment["root_path"]}')

    if experiment["root_path"]:
        main_dir = experiment["root_path"]
    else:
        main_dir = io.config_dir_path()

    exp_settings = io.exp_in_json(main_dir)
    print(f'Experiment Settings:')
    pprint(exp_settings)
    print('=' * 40)

    save_imgs = True if 'True' in experiment["save_imgs"] else False
    step, wl, f, power, norm_power = io.get_pwr_spectrum(dir_name=main_dir,
                                                         plot_show=False,
                                                         plot_save=save_imgs)

    for hs_img in exp_settings['hs_imgs']:
        img_dir = os.path.join(main_dir, hs_img)
        if not os.path.isdir(img_dir):
            continue

        io.create_all_dirs(dir_name=img_dir)

        data_files = io.extract_files(dir_name=img_dir,
                                      file_string='img_')

        print('\nNormalising csvs...')
        for index, file in enumerate(data_files):
            file_path = os.path.join(img_dir, file)
            img, file_name = io.csv_in(file_path=file_path)

            if 'Power Meter' in experiment["normalise"]:
                norm_img = dp.pwr_norm(image_data=img,
                                       file_name=file_name,
                                       norm_power=norm_power,
                                       dir_name=img_dir)
            elif 'BG' in experiment["normalise"]:
                # NEED TO UPDATE THIS STATEMENT
                print('Performing BG normalisation')
                norm_img = np.random.randint(255, size=(1080, 1920))

            if save_imgs:
                _, img_no = file_name.split('_')
                io.png_out(image_data=img,
                           file_name=file_name,
                           dir_name=img_dir,
                           image_title=f'Image: {img_no}',
                           out_name=f'{file_name}.png',
                           plot_show=False)
                io.png_out(image_data=norm_img,
                           file_name=file_name,
                           dir_name=img_dir,
                           image_title=f'Normalised image: {img_no}',
                           out_name=f'corrected_{file_name}.png',
                           plot_show=False)

            io.array_out(array_name=norm_img,
                         file_name=f'corrected_{file_name}',
                         dir_name=os.path.join(img_dir,
                                               'corrected_imgs'))

            io.update_progress(index / len(data_files))
