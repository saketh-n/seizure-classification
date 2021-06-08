import numpy as np
import matplotlib.pyplot as plt
import mne
import os

# -----------------------------------------------------

def spectral_power(raw, filename):
    channel_names = raw.info['ch_names']

    # Make a directory path
    directory = filename + '_tfr_raw_spd'
    # parent_path = 'C:/Users/User/Desktop/CSE 481C - Neruo Capstone/Project Repo/Data/GeneratedPlots/'
    parent_path = os.getcwd() + '/saved_plots/'
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


# -----------------------------------------------------

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
    directory = filename + '_tfr_raw_spd'
    # parent_path = 'C:/Users/User/Desktop/CSE 481C - Neruo Capstone/Project Repo/Data/GeneratedPlots/'
    parent_path = os.getcwd() + '/saved_plots/'
    #If directory (saved_plots) does not exist then make it
    if not os.path.isdir(parent_path):
        os.mkdir(parent_path)

    path = os.path.join(parent_path, directory)

    #If directory does not exist then make it
    if not os.path.isdir(path):
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
        ax.plot(times, data.T, linewidth=0.5)
        ax.set_xticklabels([])


        plt.xlabel('Seconds')
        plt.ylabel('$\mu V$')
        plt.title('Channel: ' + str(requiredChannel))
        positions = np.arange(0, start-stop, 1)



        saveNameRAW = path + '/' + filename + '_' + 'bn' + str(binNumber) + '_' + str(requiredChannel) + '_raw' + '.png'
        plt.savefig(saveNameRAW, dpi=300)
        plt.close(fig)

        # Plot TFR
        tfr_fig = power.plot(requiredChannel, tmin=start, tmax=stop, vmin=-0.000000005, vmax=0.000000005, show=False)
        saveNamePower = path + '/' + filename + '_' + 'bn' + str(binNumber) + '_' + str(requiredChannel) + '_tfr' + '.png'
        print(type(power))
        tfr_fig[0].savefig(saveNamePower, dpi=300)