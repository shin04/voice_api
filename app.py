from flask import Flask, request, jsonify, abort

import json
import os

from middleware.check_file import allwed_file
from middleware import extract_info

app = Flask(__name__)

app.config.from_json('config/app_config.json')

@app.route('/', methods=['GET'])
def hello():
    return jsonify({'message': 'hello world'})

@app.route('/analyze', methods=['POST'])
def analyze():
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
        file.save(os.path.join('voices/', filename))
        res = extract_info.main(filename, app.config)
        res['success'] = True
        res['message'] = 'success'
        return jsonify(res)

# app.run()
app.run(debug=True)