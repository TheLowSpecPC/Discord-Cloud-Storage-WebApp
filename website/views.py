from  flask import Blueprint, render_template, jsonify, request, redirect
import os, json, threading, time
import website.backend.json_update as json_update

path_cwd = os.path.dirname(os.path.realpath(__file__))
path_templates = os.path.join(path_cwd, "templates")

Views = Blueprint('views', __name__, template_folder=path_templates)

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

@Views.route('/move', methods=['GET','POST'])
def move():
    file = request.args.getlist('file')
    folder = request.args.getlist('folder')

    if file != [] and folder != []:
        print(file)
        print(folder)
        with open(path_cwd+'/backend/sample.json', 'r') as openfile:
            json_object = json.load(openfile)

        json_object[0][file[0]][1] = folder[0]

        with open(path_cwd+'/backend/sample.json', "w") as outfile:
            json.dump(json_object, outfile)

        return redirect('/')

    elif file != [] and folder == []:
        return render_template("move.html")

    elif file == [] and folder == []:
        return redirect('/')

@Views.route('/fetch')
def fetch():
    with open(f'{path_cwd}/backend/sample.json', 'r') as openfile:
        dataReply = json.load(openfile)

    return jsonify(dataReply)

@Views.route('/folder_create', methods=['GET','POST'])
def createFolder():
    name = request.form.getlist('crefol')

    if name != []:
        with open(path_cwd+'/backend/sample.json', 'r') as openfile:
            json_object = json.load(openfile)

        if name[0] not in json_object[1]:
            json_update.folderCreate(name[0], 'saved')

    return redirect('/')

@Views.route('/upload', methods=['GET','POST'])
def upload():
    upFile = request.files.get('uptoser')
    upFolder = request.args.getlist('folder')
    current_chunk = int(request.form['dzchunkindex'])
    total_chunks = int(request.form['dztotalchunkcount'])

    def back(fileName, folderName):
        time.sleep(5)
        print(fileName)
        print(folderName)

    if upFile == None or upFile.filename == '' or upFolder == []:
        return redirect('/')

    else:
        name = upFile.filename

        with open(path_cwd+'/backend/sample.json', 'r') as openfile:
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

        save_path = path_cwd + '/backend/upload/' + name

        with open(save_path, 'ab') as f:
            f.seek(int(request.form['dzchunkbyteoffset']))
            f.write(upFile.stream.read())

        if current_chunk+1 == total_chunks:
            json_update.fileUptoDis(name,'Unknown',upFolder[0],'uptodis')
            t = threading.Thread(target=back, args=(name,upFolder[0],))
            t.start()

        return redirect('/')