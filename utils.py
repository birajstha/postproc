

import os
import subprocess
import nibabel as nib



def resample(input_ts, output_ts):
    cmd_resample = ["3dresample", 
        "-orient", "RPI",
        "-prefix", output_ts,
        "-inset", input_ts
    ]
    subprocess.run(cmd_resample, check=True)
     
def overwrite(input_ts, output_ts):
    cmd_overwrite = ["mv", input_ts, output_ts]
    subprocess.run(cmd_overwrite, check=True)


def update_pixel_dim(file_path, new_pixdim4):
    # Update pixdim[4] field
    nii = nib.load(file_path)
    header = nii.header
    pixdim = header.get_zooms()
    new_pixdim = pixdim[:3] + (new_pixdim4,)

    # Create a new NIfTI image with the updated header
    new_header = header.copy()
    new_header.set_zooms(new_pixdim)
    updated_nii = nib.Nifti1Image(nii.get_fdata(), nii.affine, new_header)

    # Save the updated image back to the file
    nib.save(updated_nii, file_path)

def run_3dTproject(input_ts, output_ts, mask_file):
   cmd_3dTproject = ["3dTproject",
                "-input", input_ts,
                "-mask", mask_file, 
                "-polort", 2,
                "-prefix", output_ts]