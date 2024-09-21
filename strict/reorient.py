import pandas as pd
from utils import resample, overwrite
import multiprocessing as mp
from multiprocessing.pool import ThreadPool
import os
from tqdm import tqdm
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# load orientation_log.csv
orientation_log = pd.read_csv('orientation_log.csv')

# for the status column that says "needs reorient", run the function reorient with filename as the filename column
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

def thread_worker(rows):
    with mp.Pool(min(mp.cpu_count(),10)) as pool:
        indices = list(tqdm(pool.imap(process_row, [row for _, row in rows.iterrows()]), total=len(rows)))
    return indices

# Create a thread pool
num_threads = 2  # Adjust based on the cluster's capabilities
with ThreadPool(num_threads) as pool:
    chunk_size = len(needs_reorient) // num_threads
    chunks = [needs_reorient.iloc[i:i + chunk_size] for i in range(0, len(needs_reorient), chunk_size)]
    results = pool.map(thread_worker, chunks)

# Flatten the list of indices
indices = [index for sublist in results for index in sublist]

# Update the status column to "reoriented"
orientation_log.loc[indices, 'Status'] = 'reoriented'