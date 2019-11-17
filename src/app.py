from os import chdir, getcwd
from pathlib import Path
from typing import Optional

from flask import Flask, abort, make_response, request
from flask_cors import CORS

from directory import DirTree
from puppeteer.download import setup_download_folder
from puppeteer.puppet import Puppet
from puppeteer.userprofile import profile_dir

app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False

ROOT = "src\\puppeteer\\scripts\\"
root = Path(ROOT)
if not root.exists():
    abort(404, "Root Not Found")

if not root.is_dir():
    abort(404, "Root Not Directory")

ALLOWED_SUFFIXES = [".py"]
LIMIT_DEPTH = 3
BINARY = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"


@app.route('/dirtree')
def dirtree():
    dir_tree = DirTree(ROOT,
                       suffixes=ALLOWED_SUFFIXES,
                       limit_depth=LIMIT_DEPTH)

    if not dir_tree.is_allowed_suffix:
        abort(415, "Root Suffix Not Allowed")

    resp = make_response(dir_tree.to_JSON())
    resp.headers['Content-Type'] = 'application/json'
    return resp


@app.route('/file/<path:relative>', methods=['GET', 'PUT', 'DELETE'])
def file(relative: str):
    path_from_root = root.joinpath(relative)
    if not path_from_root.suffix in ALLOWED_SUFFIXES:
        abort(415, "File Suffix Not Allowed")

    if request.method == 'GET':
        if not path_from_root.is_file():
            abort(404, "File Not Found")

        with open(str(path_from_root)) as f:
            try:
                read_data = f.read()
            except:
                abort(415, "File Not Readable")

        resp = make_response(str(read_data))
        resp.headers['Content-Type'] = 'text/plain'
        return resp

    elif request.method == 'DELETE':
        if not path_from_root.is_file():
            abort(404, "File Not Found")

        path_from_root.unlink()
        resp = make_response("ok")
        resp.headers['Content-Type'] = 'text/plain'
        return resp

    elif request.method == 'PUT':
        if not path_from_root.is_file():
            try:
                path_from_root.touch(exist_ok=False)
            except FileExistsError:
                abort(500, "File Exists Error")

        with open(str(path_from_root), "w") as f:
            try:
                length = f.write(request.get_data(as_text=True))
            except:
                abort(415, "File Not Writable")

        resp = make_response(str(length))
        resp.headers['Content-Type'] = 'text/plain'
        return resp


@app.route('/exe', methods=['POST'])
def execute():
    script = request.get_data(as_text=True)
    if script == "":
        abort(400, "Empty Script")

    profile = profile_dir()
    if profile is None:
        abort(500, "Firefox Default Profile Not Found")

    puppet = Puppet(BINARY, profile)
    if not puppet.has_session:
        abort(500, "Marionette Session Not Started")

    cwd = getcwd()
    chdir(ROOT)
    err = puppet.exec(script)
    chdir(cwd)

    if not err is None:
        if puppet.has_session:
            puppet.quit()
        abort(500, f"Invalid Script: {err}")

    if puppet.has_session:
        puppet.quit()

    resp = make_response("The execution was succeeded.")
    resp.headers['Content-Type'] = 'text/plain'
    return resp


if __name__ == "__main__":
    app.run()
