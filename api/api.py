import random
from flask import Flask, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/result', methods=['POST'])
@cross_origin()
def get_result():
    # TODO: Eventually can get actual data not just filename. Encrypt it
    file = request.files['file']
    filename = file.filename
    return {'result': bool(random.getrandbits(1))}