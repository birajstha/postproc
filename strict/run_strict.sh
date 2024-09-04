#!/bin/bash
#SBATCH --mem=30G
#SBATCH -N 1
#SBATCH -p RM-shared
#SBATCH -t 60:00:00
#SBATCH --ntasks-per-node=20

path_to_script=/ocean/projects/med220004p/bshresth/vannucci/all_runs/scripts/post_proc/strict/run_3dTproject_log.py
IMAGE="/ocean/projects/med220004p/bshresth/code/images/cpac_nightly.sif"
singularity exec $IMAGE python $path_to_script