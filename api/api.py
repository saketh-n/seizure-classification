import random
from flask import Flask, request
from flask_cors import CORS, cross_origin
import math
import numpy as np
from constants import load_edf, get_edf_length
from plot_single_channels import plot_channels
from inference_preprocessing import preprocess
from model_utils import load_binary_eeg_net, binary_classification

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Load model and weights on api start
eeg_net = load_binary_eeg_net()

@app.route('/result', methods=['POST'])
@cross_origin()

def get_result():
    # Access the passed data in this manner. 
    data = request.form['filedata']
    # Save passed data to file
    filename = request.form['filename']
    newFile = open("saved_data/" + filename, "w")
    newFile.write(data)
    newFile.close()

    raw = load_edf(filename)
    edf_length = get_edf_length(raw)

    prepr_edf_data = preprocess(raw)

    plot_channels(filename, raw)

    bin_width = int(request.form['binWidth'])
    bin_interval = int(request.form['binInterval'])

    num_of_bins = math.floor(((edf_length - (bin_width / 1000)) * 1000)/bin_interval) + 1
    results = []
    # bin width is always a multiple of 1000, so no need to math floor
    # But do it anyway to get an int
    bin_width_s = math.floor(bin_width / 1000)
    bin_int_s = bin_interval / 1000
    # Prediction for each bin
    for i in range(num_of_bins):
        # start of ith bin in milliseconds: i * bin_interval
        # Of course there are 128 data points in a second
        # So proper formula is i * bin_interval * 128/1000
        # Round down
        bin_start = math.floor(i * bin_int_s * 128)
        # end of ith bin = start of bin + bin width
        # Conversion: start of bin + (bin width * 128/1000)
        bin_end = bin_start + (bin_width_s * 128)
        curr_bin = prepr_edf_data[0:64, bin_start:bin_end]
        # bin_width > 1, but model expects 1 second each
        # Try passing batch of 1 sec
        batched_bins = np.zeros((bin_width_s, 64, 128, 1))
        # Make bin into batch of 1 second slices
        # Model expecting 1 second (128 samples)
        for i in range(bin_width_s):
            batch_start = i * 128
            batch_end = (i + 1) * 128
            batched_bins[i] = curr_bin[0:64, batch_start:batch_end]
        
        # See documentation: 
        # https://www.tensorflow.org/api_docs/python/tf/keras/Model#predict
        # FYI: second argument is batch_size, default is 32
        prob = eeg_net.predict(batched_bins, bin_width_s)
        # TODO: We are making 2nd class, seizure prob, make sure
        # this is reflected when you train model
        predictions = prob[0:bin_width_s, 1]
        # Aggregrate (Average) predictions for the batch
        results.append(np.mean(predictions).astype(float))

    return {'result': results}
