# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 16:29:17 2021

@author: Martin
"""
# Import libraries
import mat73
import scipy.io as sio
import numpy as np
import random

# Change directory
#os.chdir('C:/Users/Martin/Downloads/CMPUT652_2/CMPUT_652_project-main/data')

# Define the subjects to include
subj = np.array(["A0003", "A0005", "A0008"])

# Load datasets and combine into one variable
subjData = [0] * len(subj)
trialLen = [0] * len(subj)
for i in range(0,len(subj)):
    print("Loading subject", subj[i])
    if subj[i] == "A0003":
        subjData[i] = sio.loadmat(subj[i] + '_ASL_NR_epoch_parsed.mat')
        trialLen[i] = subjData[i]['data'].shape[0]
        subjData[i]['task'] = subjData[i]['task'][0]
    else:
        subjData[i] = mat73.loadmat(subj[i] + '_ASL_NR_epoch_parsed.mat')
        trialLen[i] = subjData[i]['data'].shape[0]

# Find the one with the least amount of trials
lowTrial = trialLen.index(np.min(trialLen))
otherTrials = np.where(trialLen != np.min(trialLen))

# Loop through this individuals trials
combData = subjData[lowTrial]
for i in range(0,np.min(trialLen)):
    # Define the task, labelsm and time for the current trial
    task = subjData[lowTrial]['task'][i]
    labels = subjData[lowTrial]['labels'][:,i]
    
    # Loop through rest of subjects
    for j in otherTrials[0]:
        # Define the current other subject
        otherSubj = subjData[j]
        
        # Find where the task and labels match
        indices = np.where(np.logical_and(task == otherSubj['task'], labels[0] == otherSubj['labels'][0], labels[1] == otherSubj['labels'][1]))[0]
        
        # Pick a random index
        randTrial = random.choice(indices)
        
        # Select the data for that trial
        otherSubjTrial = otherSubj['data'][randTrial]
        
        # Sum the trials together
        combData['data'][i] = np.add(otherSubjTrial, combData['data'][i])
        
# Divide by the number of subjects
combData['data'] = combData['data']/len(subj)
        
# Save results as mat file
sio.savemat(("combined" + str(subj) + ".mat"), combData)
