import pandas as pd
import glob
import os
from utils import find_pixel_dim
from tqdm import tqdm
from multiprocessing import Pool, cpu_count
from colorama import Fore, Style, init

init(autoreset=True)

output_dir = '/ocean/projects/med220004p/bshresth/vannucci/all_runs/scripts/outputs/ANTS_FSL_noBBR_lenient/output/pipeline_cpac_fmriprep-options'

# Load .csv
df = pd.read_csv('lenient.csv')

# Get unique sub ses scan
subs = df['sub'].unique()
sess = df['ses'].unique()
scans = df['scan'].unique()

# Initialize an empty DataFrame
log_df = pd.DataFrame(columns=['File Name', 'Status'])

# Collect all file paths to process
file_paths = []

for sub in subs:
    for ses in sess:
        for scan in scans:
            sub_ses_scan = 'sub-'+sub + '_' + 'ses-' + ses + '_' +'task-' + scan
            sub_dir = f"{output_dir}/sub-{sub}/ses-{ses}/func"
            
            # Check if sub_dir exists
            if not os.path.exists(sub_dir):
                continue

            # Find matching file names in output directory
            file_names = glob.glob(f"{sub_dir}/sub-{sub}_ses-{ses}_task-{scan}_space-MNI152NLin2009cAsym_*_bold.nii.gz")
            file_paths.extend(file_names)

total_files = len(file_paths)
print(f"{Fore.GREEN}Total files to process: {total_files}")

def process_file(file):
    try:
        pixel_dim = round(float(find_pixel_dim(file)), 1)
        if pixel_dim == 0.8:
            status = 'Already 0.8'
        else:
            status = f'{pixel_dim} needs updating'
        return {'File Name': file, 'Status': status}
    except Exception as e:
        return {'File Name': file, 'Status': f'Error: {str(e)}'}

if __name__ == '__main__':
    num_processes = min(cpu_count(), 10)  # Start with a smaller number of processes
    print(f"{Fore.YELLOW}Using {num_processes} processes")

    with Pool(num_processes) as pool:
        results = list(tqdm(pool.imap(process_file, file_paths), total=total_files, desc="Processing files"))

    log_df = pd.DataFrame(results)
    log_df.to_csv('tr_correction_log.csv', index=False)
    print(f"{Fore.BLUE}Processing complete. Log saved to 'tr_correction_log.csv'")