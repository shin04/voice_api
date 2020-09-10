from flask import Flask, request, jsonify, abort
import json

api = Flask(__name__)

@api.route('/', methods=['GET'])
def hello():
    return jsonify({'message': 'hello world'})

api.run()