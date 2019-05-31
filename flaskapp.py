from flask import Flask, request, render_template, redirect

import web 
from request import Request

app = Flask(__name__)

# in case we want to add some more bells and whistles
def create_request (request_type):
    file_id = request.form["file_id"]
    return (request_type, file_id)

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

@app.route('/download_file', methods=['POST'])
def download():
    return redirect('/')

@app.route('/remove_file', methods=['POST'])
def remove():
    web.handle_web_request(create_request(Request.REMOVE_FILE))
    return redirect('/')

@app.route('/play_file', methods=['POST'])
def play_file():
    web.handle_web_request(create_request(Request.PLAY_FILE))
    return redirect('/')

@app.route('/order', methods=['POST'])
def order():
    web.handle_web_request(create_request(Request.ORDER))
    return redirect('/')

@app.route('/play', methods=['POST'])
def player():
    web.handle_web_request(create_request(Request.PLAY))
    return redirect('/')

@app.route('/pause', methods=['POST'])
def pause():
    web.handle_web_request(create_request(Request.PAUSE))
    return redirect('/')




