import pandas as pd
import re
import os
import nibabel as nib
import sys
import subprocess
from concurrent.futures import ProcessPoolExecutor
import glob
from utils import resample, overwrite, update_pixel_dim, run_3dTproject
import multiprocessing

""" 
Lenient:
First, to apply to all files in func that have space-MNI in their filepath - NOT restricted to files that end in _bold (like last time)
run 3dresample to RPI first(this will grab the bold masks as well, this time)

Now restrict only to space-MNI and ends with _bold:
change pixdim4 to the TR value (0.8)
(this will also get the whole-head bold this time)

Now restrict to reg- in the filepath:
spike regression operations - grabbing the regressor, running that inverting function, and applying 3dTproject with the spike regressor
(iirc, we used -polort 2 in the lenient rerun this time so we don't need to do it here)

"""
           
def run(sub, ses, scan, reg, file_path):
    # # # Invert the 1's and 0's in the TSV
    df = pd.read_csv(file_path, header=0)
    #df = df.apply(pd.to_numeric, errors='coerce')  # Convert to numeric, setting non-numeric to NaN
    #df = df.fillna(0).astype(int)  # Fill NaNs with 0 and ensure all data is integer
    df = 1 - df

    # Construct new file path
    new_path = os.path.join(os.getcwd(), 'TSVs_strict')
    new_file = f'spikes_sub-{sub}_ses-{ses}_scan-{scan}_reg-{reg}.tsv'
    new_file_path = os.path.join(new_path, new_file)

    # # Ensure the new directory exists
    os.makedirs(new_path, exist_ok=True)

    # # Write the inverted data to the new file
    df.to_csv(new_file_path, header=None, index=False, sep='\t')

# Directory containing the files
home_dir = '/ocean/projects/med220004p/bshresth/vannucci/all_runs/scripts/outputs/old_outputs/ANTS_FSL_noBBR_strict/working/pipeline_cpac_fmriprep-options'

# Regex pattern to extract identifiers
pattern = re.compile(r'cpac_sub-(?P<sub>[^/]+)_ses-(?P<ses>[^/]+).*/nuisance_regression_space-template_res-derivative_reg-strict_(?P<reg>[^/]+)_[^/]+/_scan_(?P<scan>[^/]+)/find_offending_time_points/censors.tsv')

args_list = []
num_cores = multiprocessing.cpu_count()
# Set the number of processes to the number of CPU cores or a reasonable value
num_processes = min(20, num_cores) 


with multiprocessing.Pool(processes=num_processes) as pool:
    # Iterate over all files in the directory
    for root, dirs, files in os.walk(home_dir):
        for file in files:
            file_path = os.path.join(root, file)
            match = pattern.search(file_path)
            if not match:
                #print(f"No match found for file: {file_path}")
                continue
            else:
                sub = match.group('sub')
                ses = match.group('ses')
                scan = match.group('scan')
                reg = match.group('reg')

                print(f"Subject: {sub}, Session: {ses}, Scan: {scan}, Regression: {reg}")

                args_list.append((sub, ses, scan, reg, file_path))

    pool.starmap(run, args_list)
print("Finished processing all files")
