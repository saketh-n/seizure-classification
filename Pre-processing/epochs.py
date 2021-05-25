import os
import mne
import numpy as np
import matplotlib.pyplot as plt
from mne import Epochs, make_fixed_length_events
from mne.io import concatenate_raws, read_raw_edf
import mne
from mne.preprocessing import compute_proj_ecg
import os
from mne.time_frequency import tfr_morlet, psd_multitaper

def make_fixed_length_epochs(raw, duration=1., preload=False,
                             reject_by_annotation=True, proj=True, overlap=0.,
                             verbose=None):
    """Divide continuous raw data into equal-sized consecutive epochs.
    Parameters
    ----------
    raw : instance of Raw
        Raw data to divide into segments.
    duration : float
        Duration of each epoch in seconds. Defaults to 1.
    %(preload)s
    %(reject_by_annotation_epochs)s
        .. versionadded:: 0.21.0
    %(proj_epochs)s
        .. versionadded:: 0.22.0
    overlap : float
        The overlap between epochs, in seconds. Must be
        ``0 <= overlap < duration``. Default is 0, i.e., no overlap.
        .. versionadded:: 0.23.0
    %(verbose)s
    Returns
    -------
    epochs : instance of Epochs
        Segmented data.
    Notes
    -----
    .. versionadded:: 0.20
    """
    events = make_fixed_length_events(raw, 1, duration=duration,
                                      overlap=overlap)
    delta = 1. / raw.info['sfreq']
    return Epochs(raw, events, event_id=[1], tmin=0, tmax=duration - delta,
                  baseline=None, preload=preload,
                  reject_by_annotation=reject_by_annotation, proj=proj,
                  verbose=verbose)
#Load Data
filename = '00000258_s004_t000'
fileformat = '.edf'
load_path = 'C:/Users/User/Desktop/CSE 481C - Neruo Capstone/Project Repo/Data/TUSZ/v1.5.2/edf/dev/02_tcp_le/002/00000258/s004_2003_07_24/' \
            + filename + fileformat


# sample_data_folder = mne.datasets.sample.data_path()
# sample_data_raw_file = os.path.join(sample_data_folder, 'MEG', 'sample',
#                                     'sample_audvis_raw.fif')
#
# raw = mne.io.read_raw_fif(sample_data_raw_file)


print(load_path)
raw = read_raw_edf(load_path, preload=True)
print(raw.info)
epochs = make_fixed_length_epochs(raw, duration=100, preload = False)
print(epochs)

#Plotting epochs
epochs.plot_image()
plt.show()
