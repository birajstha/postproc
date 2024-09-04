import glob
import pandas as pd
import multiprocessing as mp
import os
from utils import run_3dTproject, overwrite, check_orientation, resample

#load processed_files.csv if exists or set set()
processed_files = pd.read_csv("processed_files.csv")["file_path"].to_set() if os.path.exists("processed_files.csv") else set()

strategy = "strict"  # Define your strategy variable

def process_file(sub, ses, scan, reg, censor):
    timeseries_path = f"/ocean/projects/med220004p/bshresth/vannucci/all_runs/scripts/outputs/ANTS_FSL_noBBR_{strategy}/output/pipeline_cpac_fmriprep-options/sub-{sub}/ses-{ses}/func"
    file = glob.glob(f"{timeseries_path}/sub-{sub}_ses-{ses}_task-{scan}_space-MNI152NLin2009cAsym_reg-{reg}_desc-preproc*_bold.nii.gz")
    if not file:
        return
    file = file[0]
    if file in processed_files:
        return
    
    mask_file = glob.glob(f"/ocean/projects/med220004p/bshresth/vannucci/all_runs/scripts/outputs/ANTS_FSL_noBBR_{strategy}/working/pipeline_cpac_fmriprep-options/cpac_pipeline_cpac_fmriprep-options_sub-{sub}_ses-{ses}/_scan_{scan}/align_template_mask_to_template_data_space-template_reg-strict_{reg}_*/tpl-MNI152NLin2009cAsym_res-02_desc-brain_mask_resample_resample.nii.gz")
    mask_file = mask_file[0] if mask_file else None

    output_ts = file.replace(".nii.gz", "_3dTproject.nii.gz")

    # print(f"Processing file: {file}")
    # print(f"Output file: {output_ts}")
    # print(f"Mask file: {mask_file}")
    if check_orientation(mask_file).strip() != "RPI":
        resampled_mask_file = mask_file.replace(".nii.gz", "_resample.nii.gz")
        resample(mask_file, resampled_mask_file)
        overwrite(keep_ts=resampled_mask_file, overwrite_ts=mask_file)
    run_3dTproject(input_ts=file, output_ts=output_ts, mask_file=mask_file)
    overwrite(keep_ts=output_ts, overwrite_ts=file)
    processed_files.add(file)
    print(f"Finished processing file: {file}")

    #save the processed files as a csv
    pd.DataFrame(processed_files, columns=["file_path"]).to_csv("processed_files.csv", index=False)

if __name__ == '__main__':
    df = pd.read_csv('strict.csv')
    with mp.Pool(10) as pool:
        pool.starmap(process_file, zip(df["sub"], df["ses"], df["scan"], df["reg"], df['file_path']))