import mne
from mne.io import read_raw_edf
import numpy as np
import os
# Constants for model training and inference
WEIGHT_DIR = '../training/weights'
NUM_CLASSES = 2
EEG_NET_WEIGHTS = 'EEGNet-8-2-weights.h5'

def load_edf(filename):
    load_path = os.getcwd() + '/saved_data/' + filename
    raw = read_raw_edf(load_path, preload=True)
    return raw

def get_edf_length(raw: mne.io.edf.edf.RawEDF):
    return np.shape(raw._data)[1]/raw.info['sfreq']