import mne
import numpy as np 
import math


# Pre-processes 'raw' edf data
# Returns pre-processed edf data as a ndarray to pass to model
def preprocess(raw: mne.io.edf.edf.RawEDF):
    samp_freq = raw.info['sfreq']
    nchannels = raw.info['nchan']
    nyquist_freq = int(samp_freq / 2)
    freqs = range(60, nyquist_freq, 60)
    # Notch filter
    notch_filtered = mne.filter.notch_filter(raw._data, samp_freq, freqs)
    # TODO: Bandpass filter
    # TODO: Referencing op
    # Downsampling
    notch_filtered = mne.io.RawArray(notch_filtered, raw.info)
    downsampled = notch_filtered.resample(samp_freq / 2)._data
    # Reshape to have 64 channels, to fit model
    # TODO: Better strat than this later
    num_samples = np.shape(downsampled)[1]
    if (nchannels > 64):
        # pick only the first 64
        downsampled = downsampled[0:64]
    else:
        # Repeat the channels till we get 64
        right_nchannels = np.zeros((64, num_samples))
        num_reps = math.floor(64 / nchannels)
        for i in range(num_reps):
            start_ind = i * nchannels
            end_ind = (i + 1) * nchannels
            # Downsampled end index, for times when 64 isn't
            # a multiple of nchannels
            dend_ind = nchannels
            if (end_ind > 64):
                overflow = end_ind - 64
                end_ind = 64
                dend_ind = nchannels - overflow

            right_nchannels[i * nchannels: (i+1) * nchannels] = downsampled[0:dend_ind]
        downsampled = right_nchannels

    # Needs another reshaping to be 64 * (multiple of 128) * 1
    return downsampled.reshape(64, num_samples, 1)


def preprocess_simple(raw: mne.io.edf.edf.RawEDF):
    samp_freq = raw.info['sfreq']
    nchannels = raw.info['nchan']
    nyquist_freq = int(samp_freq / 2)
    freqs = range(60, nyquist_freq, 60)
    # Notch filter
    notch_filtered = mne.filter.notch_filter(raw._data, samp_freq, freqs)
    # Downsampling
    notch_filtered = mne.io.RawArray(notch_filtered, raw.info)
    downsampled = notch_filtered.resample(samp_freq / 2)._data
    num_samples = np.shape(downsampled)[1]
    if (nchannels > 64):
        # pick only the first 64
        downsampled = downsampled[0:64]
    else:
        # Repeat the channels till we get 64
        right_nchannels = np.zeros((64, num_samples))
        num_reps = math.floor(64 / nchannels)
        for i in range(num_reps):
            start_ind = i * nchannels
            end_ind = (i + 1) * nchannels
            # Downsampled end index, for times when 64 isn't
            # a multiple of nchannels
            dend_ind = nchannels
            if (end_ind > 64):
                overflow = end_ind - 64
                end_ind = 64
                dend_ind = nchannels - overflow

            right_nchannels[i * nchannels: (i+1) * nchannels] = downsampled[0:dend_ind]
        downsampled = right_nchannels

    # Needs another reshaping to be 64 * (multiple of 128) * 1
    return downsampled.reshape(64, num_samples, 1)
