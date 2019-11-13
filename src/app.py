import pathlib
from os import getcwd, chdir

from flask import Flask, abort, make_response, request
from flask_cors import CORS

from directory import DirTree
from puppeteer.download import setup_download_folder
from puppeteer.puppet import Puppet
from puppeteer.userprofile import profile_dir

app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False

# ROOT = "C:\\easyfox_test"
ROOT = "src\\puppeteer\\scripts"
# chdir(ROOT)
ALLOWED_SUFFIXES = [".py"]
LIMIT_DEPTH = 3
BINARY = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"


@app.route('/dirtree')
def dirtree():
    dir_tree = DirTree(ROOT,
                       suffixes=ALLOWED_SUFFIXES,
                       limit_depth=LIMIT_DEPTH)

    if not dir_tree.exists:
        abort(404, "Root Not Found")

    if not dir_tree.is_allowed_suffix:
        abort(415, "Root Suffix Not Allowed")

    resp = make_response(dir_tree.to_JSON())
    resp.headers['Content-Type'] = 'application/json'
    return resp


@app.route('/file/<path:relative>', methods=['GET', 'POST'])
def file(relative: str):
    full_path = __valid_full_path(relative)

    if request.method == 'GET':
        with open(full_path) as f:
            try:
                read_data = f.read()
            except:
                abort(415, "File Not Readable")

        resp = make_response(str(read_data))
        resp.headers['Content-Type'] = 'text/plain'
        return resp

    elif request.method == 'POST':
        with open(full_path, "w") as f:
            try:
                length = f.write(request.get_data(as_text=True))
            except:
                abort(415, "File Not Writable")

        resp = make_response(str(length))
        resp.headers['Content-Type'] = 'text/plain'
        return resp


@app.route('/newfile/<path:relative>', methods=['POST'])
def newfile(relative: str):
    pass


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


def __valid_full_path(relative: str) -> str:
    root_path = pathlib.Path(ROOT)
    if not root_path.exists():
        abort(404, "Root Not Found")

    full_path = root_path.joinpath(relative)
    if not full_path.exists():
        abort(404, "File Not Found")

    if not full_path.suffix in ALLOWED_SUFFIXES:
        abort(415, "File Suffix Not Allowed")

    return str(full_path)


if __name__ == "__main__":
    app.run()
