import random
from flask import Flask, request
from flask_cors import CORS, cross_origin
import math

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/result', methods=['POST'])
@cross_origin()
def get_result():
    # Access the passed data in this manner. 
    data = request.form['filedata']
    bin_width = int(request.form['binWidth'])
    bin_interval = int(request.form['binInterval'])
    # TODO: Eventually this dummy classifications array replaced w/ real deal
    edf_length = int(request.form['edfLength'])
    num_of_bins = math.floor(((edf_length - (bin_width / 1000)) * 1000)/bin_interval) + 1
    results = []
    for i in range(num_of_bins):
        # Lower bound random range at 0.06
        prob = random.random()
        if (prob < 0.06):
            prob = 0.06
        results.append(prob)
    return {'result': results}
