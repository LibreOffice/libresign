import os
from flask import Flask, request, render_template, redirect

import web, config
from request import Request

app = Flask(__name__)

# in case we want to add some more bells and whistles
def create_request (request_type):
    file_id = None

    if request.form["file_id"]:
        file_id = request.form["file_id"]

    return {"type"      : request_type, 
            "file_id"   : file_id}

def push_request (request_type):
    web.push_request(create_request(request_type))

@app.route('/', methods=['GET'])
def index():
    playlist = [
            {'file': "file", 'id': 1}, 
            {'file': "file2", 'id': 2}]
    return render_template('index.html', playlist=playlist)

def upload_file (file):
    name = file.filename

    if name == '':
        print("no filename")
        return

    file.save(os.path.join(config.SAVE_FOLDER, name))

#    push_request(Request.ADD_FILE)
    print ("uploaded", name)

def check_filetype (filename):
    pass

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        if 'file' in request.files:
            upload_file(request.files['file'])
        else:
            print("no file")

    return redirect('/')

@app.route('/download_file', methods=['POST'])
def download():
    return redirect('/')

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




