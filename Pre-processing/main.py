from mne.io import concatenate_raws, read_raw_edf
from tfr_raw_psd import spectral_power, plot_tfr_and_raw_bin_width_all_channel, load

# ------------------------------------------------------

if __name__ == '__main__':
    load_path, filename = load()
    raw = read_raw_edf(load_path, preload=True)

    #Bandpass filter 0.1Hz - 50Hz
    raw = raw.filter(0.1, 50)

    # Resample to 100 Hz
    raw = raw.resample(100, npad='auto')

    print(raw.info)
    binNumber = 10

    #Plot TFR and RAW data for the corresponding time for all channels
    plot_tfr_and_raw_bin_width_all_channel(raw = raw, start=100, stop=350, filename=filename, binNumber=binNumber)

    #Plot Spectral Power Density Plot of all channels
    spectral_power(raw=raw, filename=filename)




