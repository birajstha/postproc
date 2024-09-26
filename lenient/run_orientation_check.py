import pandas as pd
import glob
import os
from utils import check_orientation
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from colorama import init, Fore, Style

init(autoreset=True)

output_dir = '/ocean/projects/med220004p/trogers1/vannucci/all_runs/scripts/outputs/ANTS_FSL_noBBR_lenient/output/pipeline_cpac_fmriprep-options'

# Load .csv
df = pd.read_csv('lenient.csv')

# Get unique sub, ses, scan
subs = df['sub'].unique()
sess = df['ses'].unique()
scans = df['scan'].unique()

# Initialize an empty list to store all file paths to be processed
file_paths = []

for sub in subs:
    for ses in sess:
        for scan in scans:
            sub_dir = f"{output_dir}/sub-{sub}/ses-{ses}/func"
            
            # Check if sub_dir exists
            if not os.path.exists(sub_dir):
                continue

            # Find matching file names in output directory
            file_names = glob.glob(f"{sub_dir}/sub-{sub}_ses-{ses}_task-{scan}_space-MNI152NLin2009cAsym_*.nii.gz")
            file_paths.extend(file_names)

total_files = len(file_paths)
print(f"{Fore.GREEN}Total files to process: {total_files}")

def process_file(file):
    try:
        orientation = check_orientation(file).strip()
        if orientation == 'RPI':
            status = 'Already RPI'
        else:
            status = f'{orientation} needs resampling'
        return {'File Name': file, 'Status': status}
    except Exception as e:
        return {'File Name': file, 'Status': f'Error: {str(e)}'}

if __name__ == '__main__':
    num_threads = min(os.cpu_count() * 2, 100)  # Use more threads for I/O-bound tasks
    print(f"{Fore.YELLOW}Using {num_threads} threads")

    results = []
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = {executor.submit(process_file, file): file for file in file_paths}
        for future in tqdm(as_completed(futures), total=total_files, desc="Processing files"):
            results.append(future.result())

    log_df = pd.DataFrame(results)
    log_df.to_csv('orientation_log.csv', index=False)
    print(f"{Fore.BLUE}Processing complete. Log saved to 'orientation_log.csv'")