import os
import numpy as np
import GMRScripts.organisation_functions as org
import GMRScripts.experiment_settings as exp
import GMRScripts.normalise_csv as ncsv
import GMRScripts.image_stack as imst
import GMRScripts.free_spectral_range as fsr
import GMRScripts.config_dirpath as con


main_dir = con.ConfigDirPath()
img_dir = os.path.join(main_dir, 'hs_img_000')

corrected_img_dir = os.path.join(img_dir, 'corrected_imgs')
corrected_img_dir_pngs = os.path.join(img_dir, 'corrected_imgs_pngs')

pixel_stack_dir = os.path.join(img_dir, 'pixel_stack')
pixel_stack_dir_pngs = os.path.join(img_dir, 'pixel_stack_pngs')

film_thickness = 6000

data_files = org.ExtractFiles(dir_name=img_dir, file_string='img_')

pwr_spec_filename = os.path.join(main_dir, 'power_spectrum.csv')
step, wl, f, power, norm_power = ncsv.ReadInPwr(pwr_spec_filename)
ncsv.PlotDouble(wl, power, norm_power, show=False)

for index, file in enumerate(data_files):
    file_name = os.path.join(img_dir, file)
    out_file = f'corrected_{file[0:-4]}'
    ncsv.PlotCorrectedImage(file_name,
                            out_file,
                            img_dir,
                            norm_power,
                            plot_show=False,
                            plot_save=False)
    org.UpdateProgress((index + 1) / len(data_files))

rows, cols = imst.FindImgSize(dir_name=corrected_img_dir,
                              file_string='corrected_img_')

# POTENTIAL ISSUE, ROW_STACK IS OVERWRITTEN EVERY LOOP
for row in range(5):  # range(rows):
    row_stack = imst.RowStack(corrected_img_dir,
                              'corrected_img_',
                              row,
                              pixel_stack_dir_pngs,
                              pixel_stack_dir,
                              showFig=False,
                              saveFig=True)
    org.UpdateProgress((row+1) / rows)


data_files2 = org.ExtractFiles(dir_name=pixel_stack_dir,
                               file_string='row_')

wavs = fsr.WavSpace(exp.FindWavSettings(main_dir))
for index, file in enumerate(data_files2):
    in_file2 = os.path.join(pixel_stack_dir, file)
    row_stack = np.load(in_file2)

    num_cols = len(row_stack[:, 0])
    average_n = []
    for a in range(num_cols):
        wav_int = row_stack[:, a]
        file_name = f'Col{a}_Row{index}'

        freq, freq_int = fsr.GenParams(list(wavs), wav_int)
        fsr.PlotIntensity(wavs,
                          wav_int,
                          freq,
                          freq_int,
                          file_name,
                          pixel_stack_dir_pngs,
                          save=True)

        wav_peaks = fsr.FindPeaks(wavs, wav_int)
        freq_peaks = fsr.FindPeaks(freq, freq_int)

        wav_n = fsr.FreeSpectralRange(wav_peaks,
                                      thickness=film_thickness,
                                      theta=0,
                                      wavelength=True)
        freq_n = fsr.FreeSpectralRange(freq_peaks,
                                       thickness=film_thickness,
                                       theta=0,
                                       frequency=True)
        if wav_n and freq_n:
            average_n.append(fsr.AverageRefIndex(wav_n, freq_n))
        else:
            average_n.append(0)
            print(f'No peaks found in col: {a}, row: {index}')


out_file = f'{img_dir.split("/")[-1]}_refractive_index'
fsr.WriteFile(outfile_name=out_file, array_name=average_n)

org.UpdateProgress((index + 1) / len(data_files2))
