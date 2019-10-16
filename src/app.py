import os
import pathlib
from flask import Flask, make_response, request, abort

from directory import DirTree

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

ROOT = "C:\\easyfox_test"


@app.route('/dirtree')
def dirtree():
    dir_tree = DirTree(ROOT)
    if not dir_tree.exists:
        abort(404, "Root Not Found")
    resp = make_response(dir_tree.to_JSON())
    resp.headers['Content-Type'] = 'application/json'
    return resp


@app.route('/textfile/<path:relative>', methods=['GET', 'POST'])
def textfile(relative):
    root_path = pathlib.Path(ROOT)
    if not root_path.exists():
        abort(404, "Root Not Found")

    full_path = root_path.joinpath(relative)
    if not full_path.exists():
        abort(404, "File Not Found")

    if request.method == 'GET':
        with open(str(full_path)) as f:
            try:
                read_data = f.read()
            except(UnicodeDecodeError):
                abort(415, "File Not Readable")

        return str(read_data)

    elif request.method == 'POST':
        with open(str(full_path), "w") as f:
            # try:
            l = f.write(request.get_data(as_text=True))
            # except():
            #     abort(415, "File Not Readable")

        return str(l)


if __name__ == "__main__":
    app.run()
