"""tusz_subset dataset."""

import tensorflow_datasets as tfds
import tensorflow as tf
import mne
import os
import numpy as np
import math
from pathlib import Path

# TODO(tusz_subset): Markdown description  that will appear on the catalog page.
_DESCRIPTION = """
Description is **formatted** as markdown.

It should also contain any processing which has been applied (if any),
(e.g. corrupted example skipped, images cropped,...):
"""

# TODO(tusz_subset): BibTeX citation
_CITATION = """
"""


def _preprocess_data(file_path):
    raw_data = mne.io.read_raw_fif(file_path, preload=True)
    samp_freq = raw_data.info['sfreq']
    nchannels = raw_data.info['nchan']
    nyquist_freq = int(samp_freq / 2)
    freqs = range(60, nyquist_freq, 60)
    # Notch filter
    notch_filtered = mne.filter.notch_filter(raw_data._data, samp_freq, freqs)
    # TODO: Bandpass filter
    # TODO: Referencing op
    # Downsampling
    notch_filtered = mne.io.RawArray(notch_filtered, raw_data.info)
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
    downsampled.reshape(64, num_samples, 1)
    signals = []
    for i in range(int(num_samples / 128)):
        local_start = 128*i
        local_end = local_start + 128
        signals.append(downsampled[:, local_start:local_end].reshape(64, 128, 1))
    return signals


class TuszSubset(tfds.core.GeneratorBasedBuilder):
    """DatasetBuilder for tusz_subset dataset."""

    VERSION = tfds.core.Version('1.0.0')
    RELEASE_NOTES = {
        '1.0.0': 'Initial release.',
    }

    def _info(self) -> tfds.core.DatasetInfo:
        """Returns the dataset metadata."""
        # TODO(tusz_subset): Specifies the tfds.core.DatasetInfo object
        return tfds.core.DatasetInfo(
            builder=self,
            description=_DESCRIPTION,
            features=tfds.features.FeaturesDict({
                # These are the features of your dataset like images, labels ...
                'eeg_signal': tfds.features.Tensor(shape=(64, 128, 1), dtype=tf.float64),
                'label': tfds.features.ClassLabel(names=['bckg', 'seiz']),
            }),
            # If there's a common (input, target) tuple from the
            # features, specify them here. They'll be used if
            # `as_supervised=True` in `builder.as_dataset`.
            supervised_keys=('eeg_signal', 'label'),  # Set to `None` to disable
            homepage='https://dataset-homepage/',
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager: tfds.download.DownloadManager):
        """Returns SplitGenerators."""
        # TODO(tusz_subset): Downloads the data and defines the splits
        path = '/Users/robert/Desktop/School/Grad/481c/seizure-classification/training/data_subset/'

        # TODO(tusz_subset): Returns the Dict[split names, Iterator[Key, Example]]
        return {
            'train': self._generate_examples(Path(os.path.join(path, 'train'))),
            'dev': self._generate_examples(Path(os.path.join(path, 'dev'))),
        }

    def _generate_examples(self, path):
        """Yields examples."""
        # TODO(tusz_subset): Yields (key, example) tuples from the dataset
        total_idx = 0
        for idx, f in enumerate(path.glob('*.fif')):
            string_path = str(f)
            label = string_path.split('.')[-2].split('_')[-2]
            signals = _preprocess_data(string_path)
            for signal in signals:
                yield total_idx, {
                    'eeg_signal': signal,
                    'label': label,
                }
                total_idx += 1
