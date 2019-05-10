import os
import GMR.InputOutput as io
import GMRScripts.normalise_csv as ncsv
import time

main_dir = io.exp_in()
hs_imgs = os.listdir(main_dir)

for hs_img in hs_imgs:
    img_dir = os.path.join(main_dir, hs_img)

    if not os.path.isdir(img_dir):
        continue

    data_files = io.extract_files(dir_name=img_dir,
                                  file_string='img_')

    for file in data_files:
        file_path = os.path.join(img_dir, file)
        img, file_name = io.raw_in(file_path)
        print(img)
        time.sleep(5)
        print(file_name)

#data_files = org.ExtractFiles(dir_name=img_dir, file_string='img_')
#in_file = os.path.join(img_dir, 'power_spectrum.csv')

#step, wl, f, power, norm_power = ncsv.ReadInPwr(in_file)

#ncsv.PlotDouble(wl, power, norm_power, show=False)

#for index, file in enumerate(data_files):
#    file_name = os.path.join(img_dir, file)
#    ncsv.PlotCorrectedImage(file_name,
#                            f'corrected_{file[0:-4]}',
#                            save_out=True,
#                            plot_show=False,
#                            plot_save=False)
#
#    org.UpdateProgress((index + 1) / len(data_files))
