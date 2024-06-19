from  flask import Blueprint, render_template

views = Blueprint('views', __name__)

def test(temp):
    print(temp+"!!!!!!!!!!!!!")

@views.route('/')
def index():
    return render_template("meme_index.html"), test("Done")