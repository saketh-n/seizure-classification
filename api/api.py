import os
import pickle
import numpy as np
import math
from constants import TRAINED_SCALER_PATH
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO
from inference_preprocessing import preprocess
from model_utils import load_knn_model, load_edf, get_edf_length

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Load model and weights on api start
knn = load_knn_model()
scaler = pickle.load(open(TRAINED_SCALER_PATH, 'rb'))

@app.route('/<path:filename>')
@cross_origin()
def send_image(filename):
    return send_file(filename, mimetype='image/png')

@app.route('/was-cached', methods=['POST'])
@cross_origin()
def was_cached():
    filename = request.form['filename']
    saved_results = "saved_data/" + filename.split('.')[0] + "_results.txt"
    was_cached = os.path.isfile(saved_results)
    return {'result': was_cached}

@app.route('/result', methods=['POST'])
@cross_origin()
def get_result():
    # Access the passed data in this manner.
    filename = request.form['filename']
    print('files_attr', request.files)
    edf_file = request.files['file']
    print('filetype', type(edf_file))
    data = request.form['filedata']
    print('datatype', type(data))
    # Save passed data to file

    print('filename', filename)
    results = []
    saved_results = "saved_data/" + filename.split('.')[0] + "_results.txt"
    saved_seizure_bins = "saved_data/" + filename.split('.')[0] + "_bins.txt"
    saved_channels = "saved_data/" + filename.split('.')[0] + "_channels.txt"

    filepath = "saved_data/" + filename
    if not os.path.isdir("saved_data"):
        os.mkdir("saved_data")
    was_cached = os.path.isfile(saved_results)
    if not was_cached:
        edf_file.save(filepath)
        socketio.emit('dataReceipt', {'value': True})

        raw = load_edf(filename)
        channels = raw.info['ch_names']
        edf_length = get_edf_length(raw)

        prepr_edf_data = preprocess(raw)
        print('prepr_edf_data shape', prepr_edf_data.shape)

        bin_width = int(request.form['binWidth'])
        print('bin_width', bin_width)
        bin_interval = int(request.form['binInterval'])
        print('bin_interval', bin_interval)
        threshold = int(request.form['threshold']) / 100

        print('edf_length', edf_length)
        num_of_bins = math.floor(((edf_length - (bin_width / 1000)) * 1000) / bin_interval) + 1
        socketio.emit('numberBins', {'value': num_of_bins})
        print('num_of_bins', num_of_bins)

        # Save results to file
        results_file = open(saved_results, "w")
        bins_file = open(saved_seizure_bins, "w")
        channels_file = open(saved_channels, "w")
        for chan in channels:
            channels_file.write(str(chan) + "\n")
        channels_file.close()
        # bin width is always a multiple of 1000, so no need to math floor
        # But do it anyway to get an int
        bin_width_s = math.floor(bin_width / 1000)
        print('bin_width_s', bin_width_s)
        bin_int_s = bin_interval / 1000
        print('bin_int_s', bin_int_s)
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
            for j in range(bin_width_s):
                batch_start = j * 128
                batch_end = batch_start + 128
                batch_tmp = curr_bin[0:64, batch_start:batch_end]
                if batch_tmp.shape[1] == 128:
                    batched_bins[j] = curr_bin[0:64, batch_start:batch_end]
                else:
                    batched_bins[j][:, 0:batch_tmp.shape[1], :] = curr_bin[0:64, batch_start:batch_end]

            bins_squeezed = batched_bins.squeeze(-1)
            combined_samples = np.zeros((bin_width_s, 128))
            for idx in range(bin_width_s):
                temp_bin = bins_squeezed[idx]
                if temp_bin.shape[1] == 128:
                    combined_samples[idx] = bins_squeezed[idx].mean(axis=0)
                else:
                    combined_samples[idx][:, 0:temp_bin.shape[1], :] = bins_squeezed[idx].mean(axis=0)

            combined_samples_tf = scaler.transform(combined_samples)
            predictions = knn.predict(combined_samples_tf)
            result = np.mean(predictions).astype(float)
            if (result > threshold):
                seizure_bins.append(i)
                bins_file.write(str(i) + "\n")
                plot_tfr_and_raw_bin_width_all_channel(raw, i*bin_int_s, (i+1)*bin_int_s, filename, i)
            results.append(result)
            results_file.write(str(result) + "\n")
            socketio.emit('modelPass', {'value': i})
        results_file.close()
        bins_file.close()
        socketio.emit('classificationComplete', {'value': filename}) 

    # Read results from file, if it was previously cached
    if was_cached:
        results_file = open(saved_results, "r")
        bins_file = open(saved_seizure_bins, "r")
        channels_file = open(saved_channels, "r")
        lines = results_file.readlines()
        for line in lines:
            results.append(float(line))
        lines = bins_file.readlines()
        for line in lines:
            seizure_bins.append(int(line))
        lines = channels_file.readlines()
        for line in lines:
            channels.append(str(line))

    return jsonify(results=results, seizureBins=seizure_bins, channels=channels)
