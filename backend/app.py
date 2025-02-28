from flask import Flask
import boto3

app = Flask(__name__)

@app.route('/')
def main_page():
    return 'Drake\'s Site'



if __name__ == '__main__':
    app.run(debug=True)

