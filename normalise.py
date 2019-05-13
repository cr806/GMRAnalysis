import os
import GMR.ConfigureSettings as cs
import GMR.InputOutput as io
import GMR.DataPreparation as dp
import GMRScripts.normalise_csv as ncsv
import time

main_dir = cs.config_dir_path()

exp_settings = io.exp_in(main_dir)
print('Experiment Settings:\n' + f'{exp_settings}' + '\n')

step, wl, f, power, norm_power = dp.pwr_norm(dir_name=main_dir,
                                             plot_show=False,
                                             plot_save=True)

for hs_img in exp_settings['hs_imgs']:
    img_dir = os.path.join(main_dir, hs_img)
    if not os.path.isdir(img_dir):
        continue

    cs.create_all_dirs(dir_name=img_dir)

    data_files = io.extract_files(dir_name=img_dir,
                                  file_string='img_')

    print('\nNormalising csvs...')
    for index, file in enumerate(data_files):
        file_path = os.path.join(img_dir, file)
        img, file_name = io.raw_in(file_path=file_path)

        norm_img = dp.bg_norm(image=img,
                              file_name=file_name,
                              norm_power=norm_power,
                              dir_name=img_dir,
                              plot_show=False,
                              plot_save=False)

        io.data_array_out(array_name=norm_img,
                          file_name=f'corrected_{file_name}',
                          dir_name=os.path.join(img_dir,
                                                'corrected_imgs'))

        cs.update_progress(index / len(data_files))
