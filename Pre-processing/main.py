from tfr import one_tfr
import numpy as np
import matplotlib.pyplot as plt
from mne import Epochs, make_fixed_length_events
from mne.io import concatenate_raws, read_raw_edf
import mne
import os

# -------------------------------------

def load():
    # Load Data
    filename = '00000258_s001_t000'
    fileformat = '.edf'
    load_path = 'C:/Users/User/Desktop/CSE 481C - Neruo Capstone/Project Repo/Data/TUSZ/v1.5.2/edf/dev/02_tcp_le/002/00000258/s001_2003_07_16/' \
                + filename + fileformat
    return load_path, filename

# --------------------------------------

def plot_tfr_and_raw_bin_width_all_channel(raw, start, stop, filename, binNumber):
    # Channel Info
    channel_names = raw.info['ch_names']

    # Setting reference
    raw.set_eeg_reference(ref_channels=['EEG CZ-LE'])
    rawLength = int(len(raw) / raw.info['sfreq'])
    print(rawLength)

    # Construct events
    events = mne.make_fixed_length_events(raw, duration=rawLength - 1)

    # Construct Epochs
    epochs = mne.Epochs(raw, events, preload=True, tmin=0, tmax=rawLength - 1, baseline=None)

    # Plotting TFRs
    frequencies = np.arange(1, 50, 1)
    power = mne.time_frequency.tfr_morlet(epochs, n_cycles=2, return_itc=False, freqs=frequencies, decim=3)  # Run this only once

    #debug
    print(filename)
    print(binNumber)

    # Make a directory path
    directory = filename + '_tfr_and_raw'
    parent_path = 'C:/Users/User/Desktop/CSE 481C - Neruo Capstone/Project Repo/Data/GeneratedPlots/'
    path = os.path.join(parent_path, directory)

    #If directory does not exist then make it
    if(os.path.exists(path) == False):
        os.mkdir(path)

    for i in range(len(channel_names)):

        # Select the required channel
        requiredChannel = channel_names[i]

        #Plot RAW
        copy = raw.copy()
        copy.pick(requiredChannel)
        copy.crop(tmin=start, tmax=stop, include_tmax=True)

        # Plotting begins!
        data, times = copy[:, :]
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(times, data.T, linewidth=0.5);
        ax.set_xticklabels([])


        plt.xlabel('Seconds')
        plt.ylabel('$\mu V$')
        plt.title('Channel: ' + str(requiredChannel));
        positions = np.arange(0, start-stop, 1)



        saveNameRAW = path + '/' + filename + '_' + 'bn' + str(binNumber) + '_' + str(requiredChannel) + '_raw'
        plt.savefig(saveNameRAW, dpi=300)
        plt.close(fig)

        # Plot TFR
        tfr_fig = power.plot(requiredChannel, tmin=start, tmax=stop, vmin=-0.000000005, vmax=0.000000005, show=False)
        saveNamePower = path + '/' + filename + '_' + 'bn' + str(binNumber) + '_' + str(requiredChannel) + '_tfr'
        tfr_fig.savefig(saveNamePower, dpi=300)




# ------------------------------------------------------

def spectral_power(raw, filename):
    channel_names = raw.info['ch_names']

    # Make a directory path
    directory = filename + '_tfr_and_raw'
    parent_path = 'C:/Users/User/Desktop/CSE 481C - Neruo Capstone/Project Repo/Data/GeneratedPlots/'
    path = os.path.join(parent_path, directory)

    # If directory does not exist then make it
    if (os.path.exists(path) == False):
        os.mkdir(path)

    for i in range(len(channel_names)):

        # Select the required channel
        requiredChannel = channel_names[i]

        # Power spectrum
        copy = raw.copy()
        copy.pick(requiredChannel)
        psd_fig = copy.plot_psd(show=False)
        saveNamePower = path + '/' + filename + '_' + str(requiredChannel) + '_psd'
        psd_fig.savefig(saveNamePower, dpi=300)

if __name__ == '__main__':
    load_path, filename = load()
    raw = read_raw_edf(load_path, preload=True)

    # Resample to 100 Hz
    raw = raw.resample(100, npad='auto')

    print(raw.info)
    binNumber = 10

    #Plot TFR and RAW data for the corresponding time for all channels
    # plot_tfr_and_raw_bin_width_all_channel(raw = raw, start=100, stop=350, filename=filename, binNumber=binNumber)

    #Plot Spectral Power Density Plot of all channels
    spectral_power(raw=raw, filename=filename)




