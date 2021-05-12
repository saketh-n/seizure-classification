import numpy as np
import matplotlib.pyplot as plt
from mne.io import concatenate_raws, read_raw_edf


#Load Data
load_path = 'C:/Users/User/Desktop/CSE 481C - Neruo Capstone/Project Repo/Data/TUH/00003010_s003_t000.edf'
print(load_path)
raw = read_raw_edf(load_path, preload=True)

#Inspect the .edf file
print(raw.info['ch_names'])
ch_name = raw.info['ch_names']
print("Total Channels: ", len(ch_name))

#Select the required Channel
#requiredChannel = ch_name[1]
#raw.pick(requiredChannel)

#Plotting begins!
#Raw data
#raw.plot()
#plt.show()


#Better plot of one channel
data, times = raw[1:2, :]
fig = plt.subplots(figsize=(10,8))
plt.plot(times, data.T);
plt.xlabel('Seconds')
plt.ylabel('$\mu V$')
plt.title('Channels: 1-5');
plt.legend(raw.ch_names[1:2]);
plt.show()

requiredChannel = ch_name[1]
raw.pick(requiredChannel)


#Power spectrum
raw.plot_psd(tmax=np.inf)
plt.show()


