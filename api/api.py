import random
from flask import Flask, request
from flask_cors import CORS, cross_origin
import math
import numpy as np
from model_utils import load_binary_eeg_net
from inference_preprocessing import load_batched_file

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

    # TODO: Convert data to .edf file!
    filename = '/Users/robert/Desktop/s002_2003_07_21/00000258_s002_t002.edf'

    bin_width = int(request.form['binWidth'])
    bin_interval = int(request.form['binInterval'])

    # TODO: Eventually this dummy classifications array replaced w/ real deal
    edf_length = int(request.form['edfLength'])
    num_of_bins = math.floor(((edf_length - (bin_width / 1000)) * 1000)/bin_interval) + 1
    print("num_bins:", num_of_bins)

    # TODO: Call preprocessing here!
    processed_data, times = load_batched_file(filename, bin_width, num_of_bins)

    # results = []
    # for i in range(num_of_bins):
    #     # Lower bound random range at 0.06
    #     prob = random.random()
    #     if (prob < 0.06):
    #         prob = 0.06
    #     results.append(prob)
    # return {'result': results}

    results = []
    for i in range(num_of_bins):
        curr_samp = processed_data[i]  # TODO: Wrong shape, change dynamically
        prob = eeg_net.predict(curr_samp)
        results.append(prob)
    return {'result': results}
