from  flask import Blueprint, render_template, jsonify, request, redirect
import os, json, threading, time

path_cwd = os.path.dirname(os.path.realpath(__file__))
path_static = os.path.join(path_cwd, "static")
path_templates = os.path.join(path_cwd, "templates")

Views = Blueprint('views', __name__, static_folder=path_static, template_folder=path_templates)

@Views.route('/', methods=['GET','POST'])
def index():
    return render_template("main.html")

@Views.route("/folder")
def folder():
    name = request.args.getlist("name")

    if name != []:
        return render_template("folder.html")
    else:
        return redirect("/")

@Views.route('/fetch')
def fetch():
    with open(f'{path_cwd}/sample.json', 'r') as openfile:
        dataReply = json.load(openfile)

    return jsonify(dataReply)

@Views.route('/upload', methods=['GET','POST'])
def upload():
    upFile = request.files.get('uptoser')
    upFolder = request.args.get('folder')
    current_chunk = int(request.form['dzchunkindex'])
    total_chunks = int(request.form['dztotalchunkcount'])

    def back(fileName, folderName):
        time.sleep(5)
        print(fileName)
        print(folderName)

    if upFile == None or upFile.filename == '':
        return redirect('/')

    else:
        name = upFile.filename

        with open(path_cwd+'/sample.json', 'r') as openfile:
            json_object = json.load(openfile)

        dictKeys = []
        for i in json_object[0]:
            dictKeys.append(i)

        if name in dictKeys:
            base, extension = os.path.splitext(name)
            ii = 1
            while True:
                name = os.path.join(base + "(" + str(ii) + ")" + extension)
                if name not in dictKeys:
                    break
                ii += 1

        save_path = path_cwd + '/upload/' + name

        with open(save_path, 'ab') as f:
            f.seek(int(request.form['dzchunkbyteoffset']))
            f.write(upFile.stream.read())

        if current_chunk+1 == total_chunks:
            t = threading.Thread(target=back, args=(name,upFolder,))
            t.start()

        return redirect('/')