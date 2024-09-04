
import pandas as pd
from utils import update_pixel_dim
import multiprocessing as mp
import os


log = pd.read_csv('tr_correction_log.csv')


needs_tr_correction = log[log['Status'] == 'needs updating']
print(f"Number of files that need tr correction: {len(needs_tr_correction)}")
def process_row(row):
    print(f"correcting : {row['File Name']}")
    update_pixel_dim(row['File Name'], 0.8)
    print(f"Finished : {row['File Name']}")
    return row.name  # Return the index to update the status later

# Create a pool of worker processes
with mp.Pool(10) as pool:
    indices = pool.map(process_row, [row for _, row in needs_tr_correction.iterrows()])

# Update the status column to "reoriented"
log.loc[indices, 'Status'] = 'updated'
# write out
log.to_csv('tr_correction_log.csv', index=False)