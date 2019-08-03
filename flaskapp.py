# Version: MPL 1.1
#
# This file is part of the LibreOffice project.
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# Contributor(s):
# Rasmus P J <wasmus@zom.bi>
#
import os
from flask import Flask, request, render_template, redirect, send_file

import web, config
from request import Request

app = Flask(__name__)

# in case we want to add some more bells and whistles
def file_request (request_type):
    file_id = None

    if request.form.get("file"):
        file_id = request.form.get("file")

    push_request({"type"    : request_type, 
                 "file"  : file_id})

def push_request (request):
    web.push_request(request)

def upload_file (file):
    name = safe_filename(file.filename)

    if check_filetype(file) != 0:
        return

    if name == '':
        print("no filename")
        return

    file.save(os.path.join(config.SAVE_FOLDER, name))

    file_request(Request.ADD_FILE)
    print ("uploaded", name)

def file_exists (filename):
    return 0

# replace all non-alphanumerics with _ which is quite extreme but:
# TODO this ruins a lot of file names, especially parentheses, brackets and hyphens
#      are likely to be used in the names of files that we are handling, i think
# https://en.wikipedia.org/wiki/Filename#Comparison_of_filename_limitations
def safe_filename (filename):
    def clean(c):
        if c.isalnum() or c == '.':
            return c
        else:
            return '_'

    parts   = ''.join([clean(c) for c in filename.rstrip(' ')]).split('.')
    end     = '' 

    if len(parts) > 1:
        end = '.' + parts[-1]
        parts = parts[0:-1]

    safe    = ''.join(parts) + end

    return safe

def check_filetype (filename):
    # TODO
    return 0

@app.route('/', methods=['GET'])
def index():
    playlist    = web.get_playlist()
    files       = web.get_all_files()
    playing     = web.get_current_playlist_item()
    return render_template('index.html', playlist=playlist, files=files, currently_playing=playing)

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

# Change playlist order of a file already in the playlist
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

