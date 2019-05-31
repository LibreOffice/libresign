from flask import Flask, request, render_template, redirect

import web 
from request import Request, create_request

app = Flask(__name__)

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

        print(request.files)

    return redirect('/')

@app.route('/remove', methods=['POST'])
def remove():
    web.handle_web_request(create_request(Request.REMOVE_FILE, 1))
    return redirect('/')

@app.route('/action', methods=['POST'])
def action():
    web.handle_web_request(create_request(Request.PLAY, 1))
    return redirect('/')







