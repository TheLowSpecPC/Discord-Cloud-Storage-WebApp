from  flask import Blueprint, render_template, jsonify, request
import os, json

path_cwd = os.path.dirname(os.path.realpath(__file__))
path_static = os.path.join(path_cwd, "static")
path_templates = os.path.join(path_cwd, "templates")

Views = Blueprint('views', __name__, static_folder=path_static, template_folder=path_templates)

@Views.route('/', methods=['GET','POST'])
def index():
    return render_template("main.html")

@Views.route('/fetch')
def fetch():
    with open(f'{path_cwd}/sample.json', 'r') as openfile:
        dataReply = json.load(openfile)

    return jsonify(dataReply)