
import pandas as pd
from utils import resample, overwrite
import multiprocessing as mp
import os

# load orientation_log.csv
orientation_log = pd.read_csv('orientation_log.csv')

# for the status column that says "needs reorient", run the function reorient with filename as the filename column
needs_reorient = orientation_log[orientation_log['Status'] == 'needs resampling']
print(f"Number of files that need resampling: {len(needs_reorient)}")
def process_row(row):
    print(f"resampling : {row['File Name']}")
    path = row['File Name'].split('/')[0]
    filename = row['File Name'].split('/')[-1]
    resampled_filename = os.path.join(path, filename.split('.')[0] + ".resampled.nii.gz") 
    resample(row['File Name'], resampled_filename)
    overwrite(resampled_filename, row['File Name'])
    return row.name  # Return the index to update the status later

# Create a pool of worker processes
with mp.Pool(10) as pool:
    indices = pool.map(process_row, [row for _, row in needs_reorient.iterrows()])

# Update the status column to "reoriented"
orientation_log.loc[indices, 'Status'] = 'reoriented'