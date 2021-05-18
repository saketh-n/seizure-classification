import numpy as np
import matplotlib.pyplot as plt
from mne.io import concatenate_raws, read_raw_edf
import os


#Load Data
filename = '00003010_s003_t000'
fileformat = '.edf'
load_path = 'C:/Users/User/Desktop/CSE 481C - Neruo Capstone/Project Repo/Data/TUH/' + filename + fileformat
print(load_path)
raw = read_raw_edf(load_path, preload=True)

#Inspect the .edf file
print(raw.info)

#Make a directory
# directory = filename + '_allChannels'
# parent_path = 'C:/Users/User/Desktop/CSE 481C - Neruo Capstone/Project Repo/Data/GeneratedPlots/'
# path = os.path.join(parent_path, directory)
# os.mkdir(path)

#Plotting begins!
#Raw data with SCROLL
raw.plot(duration=100, block=True)
plt.show()