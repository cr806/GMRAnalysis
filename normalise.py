import os
import GMRScripts.organisation_functions as org
import GMRScripts.normalise_csv as ncsv
import GMRScripts.config_dirpath as con

main_dir = con.ConfigDirPath()
data_dirs = os.listdir(main_dir)

for directory in data_dirs:
    img_dir = os.path.join(main_dir, directory)

    data_files = org.ExtractFiles(dir_name=img_dir, file_string='img_')

    step, wl, f, power, norm_power = ncsv.ReadInPwr(dir_name=img_dir)

    ncsv.PlotDouble(wl, power, norm_power, show=False)

    for index, file in enumerate(data_files):
        file_name = os.path.join(img_dir, file)
        ncsv.PlotCorrectedImage(file_name,
                                f'corrected_{file[0:-4]}',
                                img_dir,
                                norm_power,
                                save_out=True,
                                plot_show=False,
                                plot_save=False)

        org.UpdateProgress((index + 1) / len(data_files))
