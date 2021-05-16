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
directory = filename + '_allChannels'
parent_path = 'C:/Users/User/Desktop/CSE 481C - Neruo Capstone/Project Repo/Data/GeneratedPlots/'
path = os.path.join(parent_path, directory)
os.mkdir(path)

#Plotting begins!
#Raw data
#todo: instead of scrolly image, get a static image
bigPlot = raw.plot(duration=1200, block=True, show_scrollbars = False)
bigPlotName = path + '/' + filename + '_all' + '_RAW'
bigPlot.savefig(bigPlotName)
#plt.show()

#Power spectrum
#raw.plot_psd(tmax=np.inf)
#plt.show()

#Power spectrum
psd_fig = raw.plot_psd(show=False)
saveNamePower = path + '/' + filename + '_all' + '_psd'
psd_fig.savefig(saveNamePower, dpi = 300)