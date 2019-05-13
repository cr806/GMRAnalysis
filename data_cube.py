import os
import GMR.InputOutput as io

main_dir = io.config_dir_path()


exp_settings = io.exp_in(main_dir)
print('Experiment Settings:\n' + f'{exp_settings}' + '\n')

for hs_img in exp_settings['hs_imgs']:
    img_dir = os.path.join(main_dir, hs_img)
    if not os.path.isdir(img_dir):
        continue
    corrected_img_dir = os.path.join(img_dir, 'corrected_imgs')

    data_files = io.extract_files(dir_name=corrected_img_dir,
                                  file_string='corrected_img_')

    data_cube = []

    print('\nBuilding data cube...')
    for index, file in enumerate(data_files):
        file_path = os.path.join(corrected_img_dir,
                                 file)
        corrected_img, file_name = io.array_in(file_path,
                                               mode='r')
        data_cube.append(corrected_img)

        io.update_progress(index / len(data_files))

    print('\nSaving data cube...approximately 1min per 100 imgs')
    io.array_out(array_name=data_cube,
                 file_name=f'{hs_img}_datacube',
                 dir_name=img_dir)
