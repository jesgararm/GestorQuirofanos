# Imports
from flask import Flask, request, abort, jsonify, send_from_directory
import os
import sys

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

# Creamos un recurso para ver los archivos subidos
@app.route("/files", methods=["GET"])
def list_files():
    """Endpoint to list files on the server."""
    files = []
    for filename in os.listdir(UPLOAD_FOLDER):
        path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.isfile(path):
            files.append(filename)
    return jsonify(files)


@app.route("/files/<path:path>", methods=["GET"])
def get_file(path):
    """Download a file."""
    return send_from_directory(UPLOAD_FOLDER, path, as_attachment=True)


@app.route("/upload", methods=["POST"])
def post_file():
    # Guardamos el archivo
    file = request.files['file']
    file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    # Return 201 CREATED
    return "", 201


if __name__ == '__main__':
    # Run the app
    print("Running Flask API")
    app.run(debug=True)

