from flask import Flask
from flask_cors import CORS
import boto3
import json
from dynamo import get_weights
from scoreboard import get_scoreboard


app = Flask(__name__)
CORS(app)

@app.route('/scoreboard')
def games():
    return get_scoreboard()

@app.route('/weights')
def weights():
    return get_weights()





if __name__ == '__main__':
    app.run(debug=True)

