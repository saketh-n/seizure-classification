# Contains the functionality to preprocess EEG data,
# load model weights and perform classification

from model import EEGNet
from constants import WEIGHT_DIR
from os import path, strerror
from errno import ENOENT


def load_binary_eeg_net(weights='EEGNet-8-2-weights.h5', num_samples=128):
    """
    Loads the EEGNet model with 2 output classes and
    loads pre-trained weights from weights file

    :param weights: filename of pre-trained weight file
    :param num_samples: number of samples in input
    :raises FileNotFoundError: if weights file is not in WEIGHT_DIR
    """

    # load EEGNet for binary classification
    eeg_net = EEGNet(nb_classes=2, channels=32, samples=num_samples)

    # check that model weights exist, throw error if not
    weights_file = path.join(WEIGHT_DIR, weights)
    if not path.exists(weights_file):
        raise FileNotFoundError(ENOENT, strerror(ENOENT), weights_file)

    # load pre-trained weights
    eeg_net.load_weights(weights_file, by_name=True, skip_mismatch=True)

    return eeg_net


def binary_classification(model, data):
    """
    performs binary classification on EEG data
    :param model: the binary classification model
    :param data: the EEG dataset to classify
    """
    return model.predict(data)
