import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import mne
from mne.io import concatenate_raws, read_raw_edf
from constants import load_edf
import numpy as np
import os

# Passing in raw to avoid memory expensive load_data repetition
def plot_channels(filename, raw: mne.io.edf.edf.RawEDF, socketio):
    # Inspect the .edf file
    channel_names = raw.info['ch_names']
    len_channels = len(channel_names)
    socketio.emit('lenChannels', {'value': len_channels})
    
    # Make a directory
    path = os.getcwd() + '/saved_plots/' + filename
    os.mkdir(path)

    raw_path = path + '/RAW/'
    os.mkdir(raw_path)
    psd_path = path + '/psd/'
    os.mkdir(psd_path)

    for i in range(1, len_channels):
        # Select required channel
        requiredChannel = channel_names[i]
        copy = raw.copy()
        copy.pick(requiredChannel)

        # Plotting begins
        data, times = copy[:, :]
        plt.plot(times, data.T)
        plt.xlabel('Seconds')
        plt.ylabel('$\mu V$')
        plt.title('Channel: ' + str(requiredChannel))
        saveNameRAW = raw_path + requiredChannel + '.png'
        plt.savefig(saveNameRAW, dpi = 300)
        
        # Power spectrum
        psd_fig = copy.plot_psd(show=False)
        saveNamePower = psd_path + requiredChannel + '.png'
        psd_fig.savefig(saveNamePower, dpi = 300)
        socketio.emit('plotPass', {'value': i})