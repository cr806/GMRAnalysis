import os
import GMRScripts.organisation_functions as org
import GMRScripts.normalise_csv as ncsv

main_dir = org.Platform()
sub_dir = os.path.join(main_dir, '220319_to_120419', '100419')
img_dir = os.path.join(sub_dir, 'test')
corrected_img_dir = os.path.join(img_dir, 'corrected_imgs')
corrected_img_dir_pngs = os.path.join(img_dir, 'corrected_imgs_pngs')
pixel_stack_dir = os.path.join(img_dir, 'pixel_stack')
pixel_stack_dir_pngs = os.path.join(img_dir, 'pixel_stack_pngs')

data_files = org.ExtractFiles(dir_name=img_dir, file_string='img_')
in_file = os.path.join(img_dir, 'power_spectrum.csv')

step, wl, f, power, norm_power = ncsv.ReadInPwr(in_file)

ncsv.PlotDouble(wl, power, norm_power, show=False)

for index, file in enumerate(data_files):
    file_name = os.path.join(img_dir, file)
    ncsv.PlotCorrectedImage(file_name,
                            'corrected_' + file[0:-4],
                            save_out=True,
                            plot_show=False,
                            plot_save=False)

    org.UpdateProgress((index + 1) / len(data_files))
