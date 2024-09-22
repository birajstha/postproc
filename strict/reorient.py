import pandas as pd
from utils import resample, overwrite
import multiprocessing as mp
import os
from tqdm import tqdm
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Load orientation_log.csv
orientation_log = pd.read_csv('orientation_log.csv')

# For the status column that says "needs reorient", run the function reorient with filename as the filename column
needs_reorient = orientation_log[orientation_log['Status'].str.contains('needs resampling')]
print(f"Number of files that need resampling: {len(needs_reorient)}")

def process_row(row):
    print(Fore.YELLOW + f"resampling : {row['File Name']}")
    path = row['File Name'].split('/')[0]
    filename = row['File Name'].split('/')[-1]
    resampled_filename = os.path.join(path, filename.split('.')[0] + ".resampled.nii.gz") 
    resample(row['File Name'], resampled_filename)
    overwrite(resampled_filename, row['File Name'])
    print(Fore.GREEN + f"completed : {row['File Name']}")
    return row.name  # Return the index to update the status later

# Use a multiprocessing pool with a maximum of 10 processes
with mp.Pool(min(mp.cpu_count(), 10)) as pool:
    indices = list(tqdm(pool.imap(process_row, [row for _, row in needs_reorient.iterrows()]), total=len(needs_reorient)))

# Update the status column to "reoriented"
orientation_log.loc[indices, 'Status'] = 'reoriented'