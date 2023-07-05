#Written by Aaron Lam
#Written on Python 3.10.8


#import necessary libaries
import pandas as pd
import glob
import os
from path import Path


#Setup paths and subject_ID
dir_path = "/Users/aaronlam/Library/CloudStorage/OneDrive-TheUniversityofSydney(Staff)/ASHS_tobeprocessed/completed"
savepath = "/Users/aaronlam/Library/CloudStorage/OneDrive-TheUniversityofSydney(Staff)/ASHS_tobeprocessed/completed"
subject_id = "ABC_ID"


master_df = pd.DataFrame() #set empty dataframe

#code below will look for each relevant file and sort into the correct format and then amalgamate into the correct format
for subdir, dir, files in os.walk(dir_path):
    for file in files:
        filepath = subdir + os.sep + file

        if filepath.endswith("left_corr_nogray_volumes.txt"): #left side files
            df = pd.read_csv(filepath,
                             sep = ' ',
                             usecols = [2, 3, 4],
                             names = ["ROI", "SliceNo", "Vol"]
                             )
            
            df = df.transpose()
            df.columns=df.iloc[0]
            df = df.tail(-1)
            df[subject_id] = file[:8] #this is based on HBA where the first 8 characters is the subject_ID. For instance ABC_1111 is [:8]
            df = df.set_index(subject_id)

            dfa = df.iloc[[0]].add_prefix("nslices_left_")
            dfb = df.iloc[[-1]].add_prefix("vol_left_")
            dfc = [dfa, dfb]
            df = pd.concat(dfc, axis=1)

            master_df = master_df.append(df)

        elif filepath.endswith("right_corr_nogray_volumes.txt"): #right side files
            df = pd.read_csv(filepath,
                             sep = ' ',
                             usecols = [2, 3, 4],
                             names = ["ROI", "SliceNo", "Vol"]
                             )
                             
            df = df.transpose()
            df.columns=df.iloc[0]
            df = df.tail(-1)
            df[subject_id] = file[:8] #this is based on HBA where the first 8 characters is the subject_ID. For instance ABC_1111 is [:8]
            df = df.set_index(subject_id)
            dfa = df.iloc[[0]].add_prefix("nslices_right_")
            dfb = df.iloc[[-1]].add_prefix("vol_right_")
            dfc = [dfa, dfb]
            df = pd.concat(dfc, axis=1)

            master_df = master_df.append(df)

        elif filepath.endswith("icv.txt"): #ICV files
            df = pd.read_csv(filepath,
                             sep = ' ',
                             usecols = [1],
                             names = ["ICV"]
                             )
            
            df[subject_id] = file[:8] #this is based on HBA where the first 8 characters is the subject_ID. For instance ABC_1111 is [:8]
            df = df.set_index(subject_id)

            master_df = master_df.append(df)

master_df = master_df.sum(level=0) #amalgamate based on index (for HBA studies this is ABC_ID)

master_df.to_csv(savepath + "amalgamated_ASHS_output.csv", mode = 'a', encoding = 'utf-8') #saves file
