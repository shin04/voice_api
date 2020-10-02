from flask import Flask, request, jsonify, abort
from flask_cors import CORS

import json
import os

from middleware.check_file import allwed_file
from middleware import extract_info

app = Flask(__name__)
CORS(app)

app.config.from_json('config/app_config.json')

os.makedirs(app.config['FILE_PATH'], exist_ok=True)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '../voice-recognition-288501-df448cb420f2.json'


@app.errorhandler(400)
def error_handler(error):
    res = jsonify({
        'error': {
            'message': error.description['message']
        },
        'code': error.code
    })
    return res, error.code


@app.route('/', methods=['GET'])
def hello():
    return jsonify({'message': 'hello world'})


@app.route('/analyze', methods=['POST'])
def analyze():
    if 'people_num' not in request.form:
        abort(400, {'message': 'parameter [people_num] is not found'})
    elif request.form['people_num'] == '':
        abort(400, {'message': 'people_num is not found'})
    people_num = int(request.form['people_num'])

    if 'files' not in request.files:
        abort(400, {'message': 'parameter [file] is not found'})
    file = request.files['files']

    if file.filename == '':
        abort(400, {'message': 'file is not found'})

    if file and allwed_file(file.filename, app.config):
        filename = file.filename
        file.save(os.path.join(app.config['FILE_PATH'], filename))
        res = extract_info.extract_info(filename, app.config, people_num)
        return jsonify(res)
    elif allwed_file(file.filename, app.config):
        abort(400, {'message': 'extension is invalid'})
    else:
        abort(400, {'message': 'unknown error'})


if __name__ == '__main__':
    # app.run()
    app.run(host='0.0.0.0', debug=True)
