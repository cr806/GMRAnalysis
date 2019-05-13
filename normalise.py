import os
import GMR.InputOutput as io
import GMR.DataPreparation as dp

main_dir = io.config_dir_path()

exp_settings = io.exp_in(main_dir)
print('Experiment Settings:\n' + f'{exp_settings}' + '\n')

step, wl, f, power, norm_power = io.get_pwr_spectrum(dir_name=main_dir,
                                                     plot_show=False,
                                                     plot_save=True)

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

        _, img_no = file_name.split('_')
        io.png_out(img, file_name, img_dir,
                   f'Image: {img_no}', plot_show=True)

        norm_img = dp.pwr_norm(image_data=img,
                               file_name=file_name,
                               norm_power=norm_power,
                               dir_name=img_dir)

        io.png_out(norm_img, file_name, img_dir,
                   f'Normalised image: {img_no}', plot_show=True)

        io.array_out(array_name=norm_img,
                     file_name=f'corrected_{file_name}',
                     dir_name=os.path.join(img_dir,
                                           'corrected_imgs'))

        io.update_progress(index / len(data_files))
