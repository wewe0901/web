from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

blueprint = Blueprint(__name__, __name__)

@blueprint.route('/', methods=['GET'])
def home(tab=2):
    return render_template('home.html')