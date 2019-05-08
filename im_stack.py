import os
import GMRScripts.organisation_functions as org
import GMRScripts.image_stack as imst

main_dir = org.Platform()
sub_dir = os.path.join(main_dir, '220319_to_120419', '100419')
img_dir = os.path.join(sub_dir, 'test')
corrected_img_dir = os.path.join(img_dir, 'corrected_imgs')
corrected_img_dir_pngs = os.path.join(img_dir, 'corrected_imgs_pngs')
pixel_stack_dir = os.path.join(img_dir, 'pixel_stack')
pixel_stack_dir_pngs = os.path.join(img_dir, 'pixel_stack_pngs')

rows, cols = imst.FindImgSize(dir_name=corrected_img_dir,
                              file_string='corrected_img_')

for row in range(rows):
    row_stack = imst.RowStack(dir_name=corrected_img_dir,
                              file_string='corrected_img_',
                              row=row,
                              pixel_stack_dir_pngs=pixel_stack_dir_pngs,
                              pixel_stack_dir=pixel_stack_dir,
                              saveout=True,
                              show=False,
                              save=True)
    org.UpdateProgress((row + 1) / rows)
