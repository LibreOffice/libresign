import os
from flask import Flask, request, render_template, redirect, send_file

import web, config
from request import Request

app = Flask(__name__)

# in case we want to add some more bells and whistles
def create_request (request_type):
    file_id = None

    if request.form.get("file_id"):
        file_id = request.form.get("file_id")

    return {"type"      : request_type, 
            "file_id"   : file_id}

def push_request (request_type):
    web.push_request(create_request(request_type))

def upload_file (file):
    name = file.filename

    # TODO name = make_safe(name)
    # TODO avoid duplicate names

    if name == '':
        print("no filename")
        return

    file.save(os.path.join(config.SAVE_FOLDER, name))

    push_request(Request.ADD_FILE)
    print ("uploaded", name)

def check_filetype (filename):
    # TODO
    pass

@app.route('/', methods=['GET'])
def index():
    playlist = web.get_playlist()
    return render_template('index.html', playlist=playlist)

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
    push_request(Request.REMOVE_FILE)
    return redirect('/')

@app.route('/play_file', methods=['POST'])
def play_file():
    push_request(Request.PLAY_FILE)
    return redirect('/')

@app.route('/order', methods=['POST'])
def order():
    push_request(Request.ORDER)
    return redirect('/')

@app.route('/play', methods=['POST'])
def player():
    push_request(Request.PLAY)
    return redirect('/')

@app.route('/pause', methods=['POST'])
def pause():
    push_request(Request.PAUSE)
    return redirect('/')




