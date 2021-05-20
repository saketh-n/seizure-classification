import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mne.io import concatenate_raws, read_raw_edf
import os

def plot_channels(filename):
    # Load data
    load_path = os.getcwd() + '/saved_data/' + filename
    raw = read_raw_edf(load_path, preload=True)

    # Inspect the .edf file
    channel_names = raw.info['ch_names']
    len_channels = len(channel_names)

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