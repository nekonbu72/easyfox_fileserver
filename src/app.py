from flask import Flask, request, make_response
from directory import directory_tree_byJSON, directory_tree
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/dirtree', methods=["POST"])
def dirtree():
    body = request.get_data()
    root = body.decode('utf-8')
    resp = make_response(directory_tree_byJSON(root))
    resp.headers['Content-Type'] = 'application/json'
    return resp


if __name__ == "__main__":
    app.run()
