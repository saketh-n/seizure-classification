import mne
import numpy as np
from constants import POWER_LINE_FREQ


def load_batched_file(filename: str, num_bins: int, bin_width: int):
    """
    :param filename: Name of .edf file to load
    :param num_bins: Number of bins to divide data into
    :param bin_width: Size of bins that data are segmented into
    """
    raw_data = mne.io.read_raw_edf(filename)
    notch_filtered = notch_filter_power_line_noise(raw_data)
    low_pass_and_decimate_data = low_pass_and_decimate(notch_filtered)
    picks = mne.pick_types(low_pass_and_decimate_data.info, eeg=True, exclude='bads')
    bin_width_seconds = bin_width / 1000
    batched_data = []
    batched_times = []
    for i in range(num_bins):
        start_time = i * bin_width_seconds
        end_time = min((i + 1) * bin_width_seconds, len(low_pass_and_decimate_data))
        time_idx = low_pass_and_decimate_data.time_as_index([start_time, end_time])
        data_slice, time_slice = low_pass_and_decimate_data[picks, time_idx[0]:time_idx[1]]
        batched_data.append(data_slice)
        batched_times.append(time_slice)
    return batched_data, batched_times


def notch_filter_power_line_noise(raw: mne.io.edf.edf.RawEDF):
    raw.load_data()
    freqs = get_power_line_freqs(raw.info['sfreq'])
    raw_notch = raw.copy().notch_filter(freqs=freqs)
    return raw_notch


def get_power_line_freqs(samp_freq: int):
    nyquist_freq = int(samp_freq / 2)
    return [x for x in range(POWER_LINE_FREQ, nyquist_freq, POWER_LINE_FREQ)]


def low_pass_and_decimate(raw: mne.io.edf.edf.RawEDF):
    current_samp_freq = raw.info['sfreq']
    desired_samp_freq = 90  # Hz
    decim = np.round(current_samp_freq / desired_samp_freq).astype(int)
    obtained_sfreq = current_samp_freq / decim
    lowpass_freq = obtained_sfreq / 3.

    raw_filtered = raw.copy().filter(l_freq=None, h_freq=lowpass_freq)
    return raw_filtered


if __name__ == '__main__':
    file_name = '/Users/robert/Desktop/s002_2003_07_21/00000258_s002_t002.edf'
    second_file = '/Users/robert/Desktop/s003_2003_07_23/00000629_s003_t000.edf'
    # raw_data = mne.io.read_raw_edf(file_name)
    # raw_notch_filtered = notch_filter_power_line_noise(raw_data)
    # raw_notch_low_pass_decim = low_pass_and_decimate(raw_notch_filtered)
    # print(type(raw_notch_low_pass_decim))
    # print(len(raw_notch_low_pass_decim))
    # picks = mne.pick_types(raw_notch_low_pass_decim.info, eeg=True, exclude='bads')
    # print(picks)
    # t_idx = raw_notch_low_pass_decim.time_as_index([10., 20.])
    # data, times = raw_notch_low_pass_decim[picks, t_idx[0]:t_idx[1]]
    # print(data)
    # print(times)
    # data_batched, data_times = load_batched_file(file_name, 10, 10000)
    # print(type(data_batched))
    # print(data_times)
    raw_data_1 = mne.io.read_raw_edf(file_name)
    print(raw_data_1.info)
    raw_data_2 = mne.io.read_raw_edf(second_file)
    print(raw_data_2.info)
