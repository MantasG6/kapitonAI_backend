from flask import Flask
from flask_cors import CORS
from prompt import get_result

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)


@app.route('/data')
def get_data():
    
    data = get_result()
    # Returning the data as JSON
    return data

if __name__ == '__main__':
    app.run(port=5000, debug=True)