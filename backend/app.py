from flask import Flask
import boto3

app = Flask(__name__)

@app.route('/')
def main_page():
    return 'Drake\'s Site'

@app.route('/hi')
def hello_world():
    return 'Hello World!'

@app.route('/bye')
def goodbye_world():
    return 'Goodbye World!'


if __name__ == '__main__':
    app.run(debug=True)

