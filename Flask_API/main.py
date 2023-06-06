# Imports
from flask import Flask, request, abort, jsonify, send_from_directory
from flask_restful import Resource, Api
import os
import sys
from predictions.Predict import Predict
from scheduling.Schedule import Schedule
sys.path.append('../')

UPLOAD_FOLDER = 'Flask_API/uploads'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
for filename in os.listdir(UPLOAD_FOLDER):
    print(filename)
    path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.isfile(path):
        os.remove(path)

# Create Flask app
app = Flask(__name__)
api = Api(app)
# Añadimos Predict como recurso
api.add_resource(Predict, '/predict')
api.add_resource(Schedule, '/schedule')
if __name__ == '__main__':
    # Run the app
    print("Running Flask API")
    app.run(debug=True)

