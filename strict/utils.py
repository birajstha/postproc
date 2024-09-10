

import os
import subprocess
import nibabel as nib



def resample(input_ts, output_ts, orientation="RPI"):
    cmd_resample = ["3dresample", 
        "-orient", orientation,
        "-prefix", output_ts,
        "-inset", input_ts
    ]
    subprocess.run(cmd_resample, check=True)
     
def overwrite(keep_ts, overwrite_ts):
    cmd_overwrite = ["mv", keep_ts, overwrite_ts]
    subprocess.run(cmd_overwrite, check=True)

def find_pixel_dim(file_path):
    nii = nib.load(file_path)
    header = nii.header
    pixdim = header.get_zooms()
    return pixdim[3]

def update_pixel_dim(file_path, new_pixdim4):
    # Ensure the file exists
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Print the current pixdim[4] value for verification
    print(f'Updating {file_path} with new pixdim[4] value: {new_pixdim4}')

    # Construct the command to update the pixdim[4] value using 3drefit
    command = ['3drefit', '-TR', str(new_pixdim4), file_path]
    
    # Execute the command
    try:
        subprocess.run(command, check=True)
        print(f'Successfully updated TR to {new_pixdim4} seconds.')
    except subprocess.CalledProcessError as e:
        print(f'Error occurred while updating the file: {e}')
        

def run_3dTproject(input_ts, output_ts, mask_file, tsv_file):
    cmd_3dTproject = ["3dTproject",
                "-input", input_ts,
                "-mask", mask_file,
                "-ort", tsv_file,
                "-polort", "2",
                "-prefix", output_ts]
    subprocess.run(cmd_3dTproject, check=True)

def check_orientation(file_path):
    cmd_3dinfo = ["3dinfo", 
        "-orient", file_path
    ]
    result = subprocess.run(cmd_3dinfo, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.decode('utf-8')

def remove_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        print(f"File {file_path} does not exist")