
import pandas as pd
import glob
import os
from utils import resample, overwrite, update_pixel_dim, run_3dTproject, check_orientation, find_pixel_dim

output_dir = '/ocean/projects/med220004p/bshresth/vannucci/all_runs/scripts/outputs/ANTS_FSL_noBBR_strict/output/pipeline_cpac_fmriprep-options'


# load strict.csv
df = pd.read_csv('strict.csv')

# get unique sub ses scan
subs = df['sub'].unique()
sess = df['ses'].unique()
scans = df['scan'].unique()

# need to create a string sub_ses_scan without repeating the same sub_ses_scan
#df['sub_ses_scan'] = 'sub-'+df['sub'] + '_' + 'ses-' + df['ses'] + '_' +'task-' + df['scan']


# list = df['sub_ses_scan'].unique()
# Initialize an empty DataFrame
log_df = pd.DataFrame(columns=['File Name', 'Status'])

for sub in subs:
    for ses in sess:
        for scan in scans:
            sub_ses_scan = 'sub-'+sub + '_' + 'ses-' + ses + '_' +'task-' + scan
            sub_dir = f"{output_dir}/sub-{sub}/ses-{ses}/func"
            
            #check if sub_dir exists
            if not os.path.exists(sub_dir):
                continue

            # find matching file names in output directory
            file_names = glob.glob(f"{sub_dir}/sub-{sub}_ses-{ses}_task-{scan}_space-MNI152NLin2009cAsym_*_bold.nii.gz")
            if file_names:
                for file in file_names:
                    pixel_dim = round(float(find_pixel_dim(file)),1)
                    print(f"Pixel Dimension : {pixel_dim}")
                    if pixel_dim == 0.8:
                        print(f"Pixel dim is already 0.8 : {file}")
                        new_row = pd.DataFrame({'File Name': [file], 'Status': ['Already 0.8']})
                        log_df = pd.concat([log_df, new_row], ignore_index=True)
                    else:
                        new_row = pd.DataFrame({'File Name': [file], 'Status': ['needs updating']})
                        log_df = pd.concat([log_df, new_row], ignore_index=True)


# Save the log DataFrame to a CSV file
log_df.to_csv('tr_correction_log.csv', index=False)