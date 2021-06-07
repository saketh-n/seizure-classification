# Contains the functionality to preprocess EEG data,
# load model weights and perform classification

import pickle
from constants import KNN_MODEL_PATH
from mne.io import read_raw_edf, edf
from os import getcwd


def load_knn_model():
    return pickle.load(open(KNN_MODEL_PATH, 'rb'))


def load_edf(filename):
    load_path = getcwd() + '/saved_data/' + filename
    raw = read_raw_edf(load_path, preload=True)
    return raw


def get_edf_length(raw: edf.edf.RawEDF):
    return len(raw)/raw.info['sfreq']
