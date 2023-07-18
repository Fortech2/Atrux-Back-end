from flask import Flask, jsonify, request
from flask_restful import Api

app = Flask(__name__)
api = Api(app)


@app.route('/<string:name>', methods=['GET'])
def get(name):
    return jsonify('Hello world!' + name)


@app.route('/', methods=['GET'])
def get_all():
    return jsonify('Hello world!')


@app.route('/', methods=['POST'])
def post():
    title = request.json['title']
    content = request.json['content']
    return {'message': 'Hello, World! POST' + title + content}


if __name__ == '__main__':
    app.run(debug=True)
