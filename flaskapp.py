import os
from flask import Flask, request, render_template, redirect, send_file

import web, config
from request import Request

app = Flask(__name__)

# in case we want to add some more bells and whistles
def file_request (request_type):
    file_id = None

    if request.form.get("file_id"):
        file_id = request.form.get("file_id")

    push_request({"type"    : request_type, 
                 "file_id"  : file_id})

def push_request (request):
    web.push_request(request)

def upload_file (file):
    name = file.filename

    # TODO name = make_safe(name)
    # TODO avoid duplicate names

    if name == '':
        print("no filename")
        return

    file.save(os.path.join(config.SAVE_FOLDER, name))

    file_request(Request.ADD_FILE)
    print ("uploaded", name)

def check_filetype (filename):
    # TODO
    pass

@app.route('/', methods=['GET'])
def index():
    playlist    = web.get_playlist()
    files       = web.get_all_files()
    return render_template('index.html', playlist=playlist, files=files)

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        if 'file' in request.files:
            upload_file(request.files['file'])
        else:
            print("no file")

    return redirect('/')

@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    return send_file(os.path.join(config.SAVE_FOLDER, filename))

@app.route('/remove_file', methods=['POST'])
def remove():
    file_request(Request.REMOVE_FILE)
    return redirect('/')

@app.route('/play_file', methods=['POST'])
def play_file():
    file_request(Request.PLAY_FILE)
    return redirect('/')

@app.route('/order', methods=['POST'])
def order():
    from_index  = request.form.get("from")
    to_index    = request.form.get("to")

    if from_index and to_index:
        push_request({"type"    : Request.ORDER, 
                      "from"    : int(from_index),
                      "to"      : int(to_index)})

    return redirect('/')

@app.route('/queue_file', methods=['POST'])
def queue_file():
    to_index    = request.form.get("to")
    filename    = request.form.get("file")

    if to_index and filename:
        push_request({"type"    : Request.QUEUE_FILE, 
                      "to"      : int(to_index),
                      "file"    : filename})

    return redirect('/')

@app.route('/play', methods=['POST'])
def player():
    file_request(Request.PLAY)
    return redirect('/')

@app.route('/pause', methods=['POST'])
def pause():
    file_request(Request.PAUSE)
    return redirect('/')

