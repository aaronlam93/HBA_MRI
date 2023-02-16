#!/bin/bash
#Compiling the aseg from each participant.
#Written by Aaron Lam

#load freesurfer
#export FREESURFER_HOME=/usr/local/freesurfer
#source $FREESURFER_HOME/SetUpFreeSurfer.sh

cd '/Volumes/BMRI/CRU/HBA/ABC_MRI/MRI_Data/Sleep_fastsurfer/preprocessing'

#directory of your subject files
export SUBJECTS_DIR=$PWD
list="`ls -d */`"
asegstats2table --subjects $list --meas volume --skip --tablefile aseg_stats.txt