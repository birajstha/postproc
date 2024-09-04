
import pandas as pd
import glob
import os
from utils import remove_file
import multiprocessing as mp

output_dir = '/ocean/projects/med220004p/bshresth/vannucci/all_runs/scripts/outputs/ANTS_FSL_noBBR_strict/output/pipeline_cpac_fmriprep-options'


# load strict.csv
df = pd.read_csv('strict.csv')

# get unique sub ses scan
subs = df['sub'].unique()
sess = df['ses'].unique()
scans = df['scan'].unique()


to_remove = []
for sub in subs:
    for ses in sess:
        for scan in scans:
            sub_ses_scan = 'sub-'+sub + '_' + 'ses-' + ses + '_' +'task-' + scan
            sub_dir = f"{output_dir}/sub-{sub}/ses-{ses}/func"
            
            #check if sub_dir exists
            if not os.path.exists(sub_dir):
                continue

            # find matching file names in output directory
            file_names = glob.glob(f"{sub_dir}/sub-{sub}_ses-{ses}_task-{scan}_space-MNI152NLin2009cAsym_*final.nii.gz")
            if file_names:
                for file in file_names:                    
                    to_remove.append(file)
print(f"Found {len(to_remove)} files to remove")
# use mulitprocessing to remove files
# with mp.Pool(100) as pool:
#     pool.map(remove_file, to_remove)
#     print("Finished removing files")