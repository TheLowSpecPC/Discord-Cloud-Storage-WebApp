from  flask import Blueprint, render_template, jsonify, request, redirect, send_from_directory
import os, json, threading
from subprocess import call
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
        with open(path_cwd+'/backend/sample.json', 'r') as openfile:
            json_object = json.load(openfile)

        json_object[0][file[0]][1] = folder[0]

        with open(path_cwd+'/backend/sample.json', "w") as outfile:
            json.dump(json_object, outfile)

        if json_object[0][file[0]][1] == 'null':
            return redirect('/')
        else:
            return redirect('/folder?name='+folder[0])

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

@Views.route('/delfolder', methods=['GET','POST'])
def deleteFolder():
    name = request.args.getlist('folderdel')

    def Thread(folderName, json_object):
        for key in json_object[0].keys():
            if json_object[0][key][1] == folderName and json_object[0][key][2] == 'inDoscord':
                call(['python', 'website/backend/dbot.py', 'delete', key, json_object[0][key][0]])

            if json_object[0][key][1] == folderName and json_object[0][key][2] == 'inServer':
                os.remove(path_cwd + '/backend/download/' + key)
                call(['python', 'website/backend/dbot.py', 'delete', key, json_object[0][key][0]])

        json_update.folderDelete(folderName)

    if name != []:
        with open(path_cwd+'/backend/sample.json', 'r') as openfile:
            json_object = json.load(openfile)

        if name[0] in json_object[1]:
            json_update.folderUpdate(name[0], 'deleting')
            t = threading.Thread(target=Thread, args=(name[0],json_object,))
            t.start()

    return redirect('/')


@Views.route('/upload', methods=['GET','POST'])
def upload():
    upFile = request.files.get('uptoser')
    upFolder = request.args.getlist('folder')
    current_chunk = int(request.form['dzchunkindex'])
    total_chunks = int(request.form['dztotalchunkcount'])

    def Thread(fileName, fileDir):
        call(['python', 'website/backend/dbot.py', 'send', fileName, fileDir])

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
            t = threading.Thread(target=Thread, args=(name,save_path,))
            t.start()

        return redirect('/')

@Views.route('/downfromdis', methods=['GET',"POST"])
def downFromDis():
    name = request.args.getlist('file')

    def Thread(fileName, chunks):
        call(['python', 'website/backend/dbot.py', 'download', fileName, chunks])

    with open(path_cwd + '/backend/sample.json', 'r') as openfile:
        json_object = json.load(openfile)

    dictKeys = []
    for i in json_object[0]:
        dictKeys.append(i)

    if name == []:
        return redirect('/')

    if name[0] not in dictKeys:
        return redirect('/')
    else:
        fileName = name[0]
        folderName = json_object[0][fileName][1]
        chunks = json_object[0][fileName][0]

        json_update.fileUpdate(fileName, chunks, 'downfromdis', 2)

        t = threading.Thread(target=Thread, args=(fileName, chunks,))

        if folderName == 'null':
            t.start()
            return redirect('/')
        else:
            t.start()
            return redirect('/folder?name=' + folderName)

@Views.route('/downfromser', methods=['GET','POST'])
def downFromSer():
    name = request.args.getlist('file')

    with open(path_cwd + '/backend/sample.json', 'r') as openfile:
        json_object = json.load(openfile)

    dictKeys = []
    for i in json_object[0]:
        dictKeys.append(i)

    if name == []:
        return redirect('/')

    if name[0] not in dictKeys:
        return redirect('/')
    else:
        return send_from_directory(path_cwd + '/backend/download', name[0])

@Views.route('/delfromdis', methods=['GET','POST'])
def delFromDis():
    name = request.args.getlist('file')

    def Thread(fileName, chunks):
        call(['python', 'website/backend/dbot.py', 'delete', fileName, chunks])

    with open(path_cwd + '/backend/sample.json', 'r') as openfile:
        json_object = json.load(openfile)

    dictKeys = []
    for i in json_object[0]:
        dictKeys.append(i)

    if name == []:
        return redirect('/')

    if name[0] not in dictKeys:
        return redirect('/')
    else:
        fileName = name[0]
        folderName = json_object[0][fileName][1]
        chunks = json_object[0][fileName][0]

        json_update.fileUpdate(fileName, chunks, 'deleting', 2)

        t = threading.Thread(target=Thread, args=(fileName, chunks,))
        print(fileName)

        if folderName == 'null':
            t.start()
            return redirect('/')
        else:
            t.start()
            return redirect('/folder?name=' + folderName)

@Views.route('/delfromser', methods=['GET','POST'])
def delFromSer():
    name = request.args.getlist('file')

    with open(path_cwd + '/backend/sample.json', 'r') as openfile:
        json_object = json.load(openfile)

    dictKeys = []
    for i in json_object[0]:
        dictKeys.append(i)

    if name == []:
        return redirect('/')

    if name[0] not in dictKeys:
        return redirect('/')
    else:
        fileName = name[0]
        chunks = json_object[0][fileName][0]
        folderName = json_object[0][fileName][1]

        os.remove(path_cwd + '/backend/download/' + fileName)
        json_update.fileUpdate(fileName, chunks, 'inDiscord', 0)

        if folderName == 'null':
            return redirect('/')
        else:
            return redirect('/folder?name=' + folderName)