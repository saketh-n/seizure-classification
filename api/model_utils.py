# Contains the functionality to preprocess EEG data,
# load model weights and perform classification

import pickle
import sys
from constants import KNN_MODEL_PATH
from mne.io import read_raw_edf, edf
from os import getcwd

# The KNN model was pickled with scikit-learn 0.23, which kept DistanceMetric
# in sklearn.neighbors._dist_metrics; alias the module so the pickle loads
# under the scikit-learn pinned in requirements.txt.
import sklearn.metrics._dist_metrics
sys.modules.setdefault('sklearn.neighbors._dist_metrics', sklearn.metrics._dist_metrics)


def load_knn_model():
    return pickle.load(open(KNN_MODEL_PATH, 'rb'))


def load_edf(filename):
    load_path = getcwd() + '/saved_data/' + filename
    raw = read_raw_edf(load_path, preload=True)
    return raw


def get_edf_length(raw: edf.edf.RawEDF):
    return len(raw)/raw.info['sfreq']
