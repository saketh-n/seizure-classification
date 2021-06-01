# Contains the functionality to preprocess EEG data,
# load model weights and perform classification

import torch
import pickle
import tensorflow.keras as keras
from model import EEGNet, simple_binary_classifier, MLP
from constants import WEIGHT_DIR
from os import path, strerror
from errno import ENOENT


def load_binary_eeg_net(weights='EEGNet-8-2-weights.h5'):
    """
    Loads the EEGNet model with 2 output classes and
    loads pre-trained weights from weights file

    :param weights: filename of pre-trained weight file
    :raises FileNotFoundError: if weights file is not in WEIGHT_DIR
    """

    # load EEGNet for binary classification
    eeg_net = EEGNet(nb_classes=2)

    # check that model weights exist, throw error if not
    weights_file = path.join(WEIGHT_DIR, weights)
    if not path.exists(weights_file):
        raise FileNotFoundError(ENOENT, strerror(ENOENT), weights_file)

    # TODO: Replace this load_weights w model re-train
    # eeg_net.load_weights(weights_file)

    return eeg_net


def load_binary_mlp(weights=''):
    """
    Loads multi-layer perceptron (mlp) model for binary classification
    :param weights: path to weights file
    """
    mlp = simple_binary_classifier(nb_classes=2)
    if weights != '':
        # check that model weights exist, throw error if not
        weights_file = path.join(WEIGHT_DIR, weights)
        if not path.exists(weights_file):
            raise FileNotFoundError(ENOENT, strerror(ENOENT), weights_file)
        mlp = keras.models.load_model(WEIGHT_DIR)

    return mlp


def load_pytorch_mlp(weights=''):
    mlp = MLP()
    if weights != '':
        # check that model weights exist, throw error if not
        weights_file = path.join(WEIGHT_DIR, weights)
        if not path.exists(weights_file):
            raise FileNotFoundError(ENOENT, strerror(ENOENT), weights_file)
        mlp.load_state_dict(torch.load(weights_file))
    return mlp


def load_knn_model():
    knn_model_path = path.join('../training/', 'knn_classifier.pkl')
    return pickle.load(open(knn_model_path, 'rb'))
