from flask import Flask, request, render_template, redirect

app = Flask(__name__)

def upload_file (file):
    name = file.filename

    if name == '':
        print("no filename")
        return

    print "uploaded", name

def check_filetype (filename):
    pass

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        if 'file' in request.files:
            upload_file(request.files['file'])
        else:
            print "no file"

        print request.files

    return redirect('/')

@app.route('/remove', methods=['POST'])
def remove():
    # remove from list
    return redirect('/')

@app.route('/action', methods=['POST'])
def action():
    # play, change position in list, stop
    return redirect('/')

if __name__ == '__main__':
        app.run(debug=True)

