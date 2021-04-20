import random
from flask import Flask
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/result')
@cross_origin()
def get_result():
    return {'result': bool(random.getrandbits(1))}