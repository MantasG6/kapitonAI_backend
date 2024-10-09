from prompt import generate
from flask import Flask, jsonify
import ngrok
from flask_cors import CORS
from extractData import getConditionsArray
import vertexai

conditionsArray = getConditionsArray()

ngrok.set_auth_token("2n1OFB4fL3R4uwURDH8YYFfboEc_7ZVXN8veCgB7B41BoBsNu")

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)


@app.route('/data', methods=['GET'])
def simulate():

    i = 0
    with open('data/counter.txt', 'r') as f:
        i=int(f.read())

    if i >= len(conditionsArray):
        i = 0

    data = generate(conditionsArray[i])

    with open('data/counter.txt', 'w') as f:
        f.write(str(i+1))
    
    # Returning the data as JSON
    return data

if __name__ == '__main__':
    vertexai.init(project="tesonet-aihack24vil-6123", location="europe-central2")
    app.run(port=5000, debug=True)