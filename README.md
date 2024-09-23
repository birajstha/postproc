
## CPAC post script for correcting the Orientations and headers

Lenient:
First, to apply to all files in func that have space-MNI in their filepath - NOT restricted to files that end in _bold (like last time)
run 3dresample to RPI first(this will grab the bold masks as well, this time)

Now restrict only to space-MNI and ends with _bold:
change pixdim4 to the TR value (0.8)
(this will also get the whole-head bold this time)

Now restrict to reg- in the filepath:
spike regression operations - grabbing the regressor, running that inverting function, and applying 3dTproject with the spike regressor
(iirc, we used -polort 2 in the lenient rerun this time so we don't need to do it here)

### Using the script
lenient:
1. [run_orientation_check.py](lenient/run_orientation_check.py) - to check all orientation of files and save `orientation_log.csv` as a list of files that need reorient
2. [reorient.py](lenient/reorient.py) - to reorient all files to "RPI" that are in orientation_log.csv that are not in "RPI"
3. [run_reorient.sh](lenient/run_reorient.sh) - to submit reorient.py to slurm and running it inside CPAC container

4. [run_check_tr.py](lenient/run_check_tr.py) - to check all tr/pixdim4 values of all bold files and save `tr_correction_log.csv` as list of files that need tr-correction
5. [correct_tr.py](lenient/correct_tr.py) - to correct TR of all bold files that are listed in tr_correction_log.csv that needs TR correction
6. [run_tr_correct.sh](lenient/run_tr_correct.sh) - to submit correct_tr.py to slurm and running it inside CPAC container

strict:
1. [run_orientation_check.py](strict/run_orientation_check.py) - to check all orientation of files and save `orientation_log.csv` as a list of files that need reorient
2. [reorient.py](strict/reorient.py) - to reorient all files to "RPI" that are in orientation_log.csv that are not in "RPI"
3. [run_reorient.sh](strict/run_reorient.sh) - to submit reorient.py to slurm and running it inside CPAC container

4. [run_check_tr.py](strict/run_check_tr.py) - to check all tr/pixdim4 values of all bold files and save `tr_correction_log.csv` as list of files that need tr-correction
5. [correct_tr.py](strict/correct_tr.py) - to correct TR of all bold files that are listed in tr_correction_log.csv that needs TR correction
6. [run_tr_correct.sh](strict/run_tr_correct.sh) - to submit correct_tr.py to slurm and running it inside CPAC container