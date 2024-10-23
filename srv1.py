from flask import Flask, jsonify
from flask_cors import CORS
from extractData import getConditionsArray
from trial_v2 import get_result

conditionsArray = getConditionsArray()

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)


@app.route('/data', methods=['GET'])
def get_data():
    
    data = get_result()
    # Returning the data as JSON
    return data

if __name__ == '__main__':
    app.run(port=80, debug=True)