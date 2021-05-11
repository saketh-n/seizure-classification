import random
from flask import Flask, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/result', methods=['POST'])
@cross_origin()
def get_result():
    # Access the passed data in this manner. 
    data = request.form['filedata']
    # TODO: Eventually this dummy classifications array replaced w/ real deal
    results = []
    for i in range(10):
        # Lower bound random range at 0.06
        prob = random.random()
        if (prob < 0.06):
            prob = 0.06
        results.append(prob)
    return {'result': results}
