import numpy as np
import matplotlib.pyplot as plt
from mne.io import concatenate_raws, read_raw_edf


#Load Data
load_path = 'C:/Users/User/Desktop/CSE 481C - Neruo Capstone/Project Repo/Data/TUH/00003010_s003_t000.edf'
print(load_path)
raw = read_raw_edf(load_path, preload=True)

#Inspect the .edf file
print(raw.info)

#Plotting begins!
#Raw data
raw.plot(duration=100, block=True)
plt.show()

#Power spectrum
raw.plot_psd(tmax=np.inf)
plt.show()
