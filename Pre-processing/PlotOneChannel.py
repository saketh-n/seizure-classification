import numpy as np
import matplotlib.pyplot as plt
from mne.io import concatenate_raws, read_raw_edf
import os


#Load Data
filename = '00000258_s001_t000'
fileformat = '.edf'
load_path = 'C:/Users/User/Desktop/CSE 481C - Neruo Capstone/Project Repo/Data/TUSZ/v1.5.2/edf/dev/02_tcp_le/002/00000258/s001_2003_07_16/' \
            + filename + fileformat
print(load_path)
raw = read_raw_edf(load_path, preload=True)

#Inspect the .edf file
channel_names = raw.info['ch_names']
len_channels = len(channel_names)
print(channel_names)
print("Total Channels: ", len_channels)

#Make a directory
directory = filename
parent_path = 'C:/Users/User/Desktop/CSE 481C - Neruo Capstone/Project Repo/Data/GeneratedPlots/'
path = os.path.join(parent_path, directory)
os.mkdir(path)

def makePlots(i):
    #Select the required Channel
    requiredChannel = channel_names[i]
    copy = raw.copy()
    copy.pick(requiredChannel)

    #Plotting begins!
    data, times = copy[:, :]
    fig = plt.figure()
    plt.plot(times, data.T);
    plt.xlabel('Seconds')
    plt.ylabel('$\mu V$')
    plt.title('Channel: ' + str(requiredChannel));
    saveNameRAW = path + '/' + filename + '_' + requiredChannel + '_RAW'
    plt.savefig(saveNameRAW, dpi = 300)
    plt.close(fig)


    #Power spectrum
    psd_fig = copy.plot_psd(show=False)
    saveNamePower = path + '/' + filename + '_' + requiredChannel + '_psd'
    psd_fig.savefig(saveNamePower, dpi = 300)

ran = range(1, len_channels)
for i in ran:
    makePlots(i)
