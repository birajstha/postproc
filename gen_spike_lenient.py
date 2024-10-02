import pandas as pd
from multiprocessing import Pool
import os
from tqdm import tqdm
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

workdir = "/ocean/projects/med220004p/bshresth/vannucci/all_runs/scripts/outputs/old_outputs/ANTS_FSL_noBBR_lenient/working/pipeline_cpac_fmriprep-options/"           

def run(args):
    sub, ses, scan, reg, file_path = args
    fdj = os.path.join(workdir, f'cpac_sub-{sub}_ses-{ses}/gen_motion_stats_111/_scan_{scan}/calculate_FDJ/FD_J.1D')
    if reg == "GSR": 
        return

    if os.path.exists(fdj):
        #print(Fore.GREEN + f"Processing sub-{sub}, ses-{ses}, scan-{scan}")
        # Read in the FDJ file
        fdj_df = pd.read_csv(fdj, header=None)
       
        threshold_df = (fdj_df > 0.9).astype(int)

        inverted_threshold_df = (1 - threshold_df)

        # make a df with first column as fdj values and another one thresholded fdj values at 0.2
        qc_df = pd.DataFrame()
        qc_df['fdj'] = fdj_df
        qc_df['thresholded_fdj'] = threshold_df
        qc_df['inverted_thresholded_fdj'] = inverted_threshold_df

        # Construct new file path
        new_path = os.path.join(os.getcwd(), 'TSVs_lenient')
        os.makedirs(new_path, exist_ok=True)
        new_file = f'spikes_sub-{sub}_ses-{ses}_scan-{scan}.tsv'
        new_file_path = os.path.join(new_path, new_file)
        threshold_df.to_csv(new_file_path, header=["spike"], index=False, sep='\t')
        
        #construct new file path for qc_df
        new_path_qc = os.path.join(os.getcwd(), 'TSVs_lenient', 'qc')
        new_file_qc = f'qc_sub-{sub}_ses-{ses}_scan-{scan}.tsv'
        new_file_path_qc = os.path.join(new_path_qc, new_file_qc)
        os.makedirs(new_path_qc, exist_ok=True)
        qc_df.to_csv(new_file_path_qc, header=['FD_J', 'thresholded_at_0.9', 'inverted'], index=False, sep='\t')

    else:
        print(Fore.RED + f"NO FDJ FILE for sub-{sub}, ses-{ses}, scan-{scan}")

if __name__ == "__main__":
    # Read in strict/strict.csv
    df = pd.read_csv('strict/strict.csv')
    
    # Prepare the arguments for each row
    args = [(row['sub'], row['ses'], row['scan'], row['reg'], row['file_path']) for _, row in df.iterrows()]

    # Use multiprocessing to process each row with 50 processes
    with Pool(processes=50) as pool:
        for _ in tqdm(pool.imap_unordered(run, args), total=len(args), desc="Processing"):
            pass