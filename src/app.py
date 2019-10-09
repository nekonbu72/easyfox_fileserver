from flask import Flask, request, make_response
from directory import directory_tree_JSON
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

ROOT = "C:\\easyfox_test"


@app.route('/dirtree')
def dirtree():
    resp = make_response(directory_tree_JSON(ROOT))
    resp.headers['Content-Type'] = 'application/json'
    return resp


if __name__ == "__main__":
    app.run()
