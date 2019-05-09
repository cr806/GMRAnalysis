import os
import numpy as np
import GMRScripts.organisation_functions as org
import GMRScripts.experiment_settings as exp
import GMRScripts.normalise_csv as ncsv
import GMRScripts.image_stack as imst
import GMRScripts.free_spectral_range as fsr
import GMRScripts.config_dirpath as con


main_dir = con.ConfigDirPath()

film_thickness = 6000


exp_settings = exp.ReadInSettings(main_dir)
hs_filename = exp_settings['filenames'][0]
img_dir = os.path.join(main_dir, hs_filename)

corrected_img_dir = os.path.join(img_dir, 'corrected_imgs')
corrected_img_dir_pngs = os.path.join(img_dir, 'corrected_imgs_pngs')
pixel_stack_dir = os.path.join(img_dir, 'pixel_stack')
pixel_stack_dir_pngs = os.path.join(img_dir, 'pixel_stack_pngs')

step, wl, f, power, norm_power = ncsv.ReadInPwr(main_dir)
ncsv.PlotDouble(wl, power, norm_power, show=False)

data_files = org.ExtractFiles(dir_name=img_dir, file_string='img_')
if (not os.path.isdir(corrected_img_dir) or
        len(os.listdir(corrected_img_dir)) < len(wl)):

    for index, file in enumerate(data_files):
        file_name = os.path.join(img_dir, file)
        out_name = f'corrected_{file[0:-4]}'
        ncsv.PlotCorrectedImagePanda(file_name,
                                     out_name,
                                     corrected_img_dir,
                                     norm_power,
                                     plot_show=False,
                                     plot_save=False)
        org.UpdateProgress((index + 1) / len(data_files))

rows, cols = imst.FindImgSize(dir_name=corrected_img_dir,
                              file_string='corrected_img_')

if (not os.path.isdir(pixel_stack_dir) or
        len(os.listdir(pixel_stack_dir)) < rows):

    for row in range(rows):
        row_stack = imst.RowStack(corrected_img_dir,
                                  'corrected_img_',
                                  row,
                                  pixel_stack_dir_pngs,
                                  pixel_stack_dir,
                                  showFig=False,
                                  saveFig=False)
        org.UpdateProgress((row+1) / rows)

data_files2 = org.ExtractFiles(dir_name=pixel_stack_dir,
                               file_string='row_')

wavs = fsr.WavSpace(exp_settings)
for index, file in enumerate(data_files2):
    in_file2 = os.path.join(pixel_stack_dir, file)
    row_stack = np.load(in_file2)

    num_cols = 20  # len(row_stack[:, 0])
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
        wav_n = fsr.FreeSpectralRange(wav_peaks,
                                      thickness=film_thickness,
                                      theta=0,
                                      wavelength=True)

        freq_peaks = fsr.FindPeaks(freq, freq_int)
        freq_n = fsr.FreeSpectralRange(freq_peaks,
                                       thickness=film_thickness,
                                       theta=0,
                                       frequency=True)
        if wav_n or freq_n:
            average_n.append(fsr.AverageRefIndex(wav_n, freq_n))
        else:
            average_n.append(0)
            print(f'No peaks found in col: {a}, row: {index}')

        org.UpdateProgress((a + 1) / num_cols)

    out_file = f'{hs_filename}_refractive_index.csv'
    fsr.WriteRowToFile(outfile_name=out_file, array_name=average_n)

    org.UpdateProgress((index + 1) / len(data_files2))
