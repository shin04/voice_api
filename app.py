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


@app.route('/', methods=['GET'])
def hello():
    return jsonify({'message': 'hello world'})


@app.route('/analyze', methods=['POST'])
def analyze():
    people_num = int(request.form['people_num'])

    if 'files' not in request.files:
        print('file not found')
        res = {'success': True, 'message': 'file not found'}
        return jsonify(res)

    file = request.files['files']

    if file.filename == '':
        print('file not found')
        res = {'success': True, 'message': 'file not found'}
        return jsonify(res)

    if file and allwed_file(file.filename, app.config):
        filename = file.filename
        file.save(os.path.join(app.config['FILE_PATH'], filename))
        res = extract_info.main(filename, app.config, people_num)
        res['success'] = True
        res['message'] = 'success'
        return jsonify(res)


if __name__ == '__main__':
    # app.run()
    app.run(host='0.0.0.0', debug=True)
