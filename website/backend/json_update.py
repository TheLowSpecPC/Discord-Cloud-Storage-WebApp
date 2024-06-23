import json, os

path_cwd = os.path.dirname(os.path.realpath(__file__))
jsonPath = path_cwd+'/sample.json'

def fileUptoDis(name, size, folder, status):
    with open(jsonPath, 'r') as openfile:
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


    json_object[0].update({name: [size, folder, status, 0]})

    with open(jsonPath, "w") as outfile:
        json.dump(json_object, outfile)

def fileUpdate(name, size, status, progress):
    with open(jsonPath, 'r') as openfile:
        json_object = json.load(openfile)

    json_object[0][name][0] = size
    json_object[0][name][2] = status
    json_object[0][name][3] = progress

    with open(jsonPath, "w") as outfile:
        json.dump(json_object, outfile)

def fileDelete(name):
    with open(jsonPath, 'r') as openfile:
        json_object = json.load(openfile)

    json_object[0].pop(name)

    with open(jsonPath, "w") as outfile:
        json.dump(json_object, outfile)

def folderCreate(name, status):
    with open(jsonPath, 'r') as openfile:
        json_object = json.load(openfile)

    json_object[1].update({name: status})

    with open(jsonPath, "w") as outfile:
        json.dump(json_object, outfile)

def folderUpdate(name, status):
    with open(jsonPath, 'r') as openfile:
        json_object = json.load(openfile)

    json_object[1][name] = status

    with open(jsonPath, "w") as outfile:
        json.dump(json_object, outfile)

def folderDelete(name):
    with open(jsonPath, 'r') as openfile:
        json_object = json.load(openfile)

    json_object[1].pop(name)

    with open(jsonPath, "w") as outfile:
        json.dump(json_object, outfile)