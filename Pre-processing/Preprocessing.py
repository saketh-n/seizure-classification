import numpy as np
import matplotlib.pyplot as plt
from mne.io import concatenate_raws, read_raw_edf
import mne
import os
from mne.time_frequency import tfr_morlet, psd_multitaper

def raw_plot():
    # Plotting begins!
    data, times = raw[:, :]
    fig = plt.figure()
    plt.plot(times, data.T);
    plt.xlabel('Seconds')
    plt.ylabel('$\mu V$')
    plt.title('Filtered at 60Hz');
    plt.show()

#Load Data
filename = '00003010_s003_t000'
fileformat = '.edf'
load_path = 'C:/Users/User/Desktop/CSE 481C - Neruo Capstone/Project Repo/Data/TUH/' + filename + fileformat
print(load_path)
raw = read_raw_edf(load_path, preload=True)

#Inspect the .edf file
channel_names = raw.info['ch_names']
len_channels = len(channel_names)
print(channel_names)
print("Total Channels: ", len_channels)
print(raw.info)

#Notch filter 60Hz - Probably don't need this if we down sample to 100Hz sampling rate from 256Hz
#raw.notch_filter(np.arange(60, 125, 60))

# Resample to 100 Hz
raw_resampled = raw.resample(100, npad='auto')

#Referencing - not sure if this is even doing anything
raw.set_eeg_reference([])

#raw_plot()
psd_fig = raw.plot_psd(show=True)

events = mne.find_events(raw)
print(events[:5])

# # define frequencies of interest (log-spaced)
# freqs = np.logspace(*np.log10([6, 35]), num=8)
# n_cycles = freqs / 2.  # different number of cycle per frequency
# power, itc = tfr_morlet(epochs, freqs=freqs, n_cycles=n_cycles, use_fft=True,
#                         return_itc=True, decim=3, n_jobs=1)
#
#
# #Inspect Power
# power.plot_topo(baseline=(-0.5, 0), mode='logratio', title='Average power')
# power.plot([82], baseline=(-0.5, 0), mode='logratio', title=power.ch_names[82])
#
# fig, axis = plt.subplots(1, 2, figsize=(7, 4))
# power.plot_topomap(ch_type='grad', tmin=0.5, tmax=1.5, fmin=8, fmax=12,
#                    baseline=(-0.5, 0), mode='logratio', axes=axis[0],
#                    title='Alpha', vmax=0.45, show=False)
# power.plot_topomap(ch_type='grad', tmin=0.5, tmax=1.5, fmin=13, fmax=25,
#                    baseline=(-0.5, 0), mode='logratio', axes=axis[1],
#                    title='Beta', vmax=0.45, show=False)
# mne.viz.tight_layout()
# plt.show()
