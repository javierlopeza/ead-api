from flask import Blueprint, render_template as view
from app.helper import response

docs = Blueprint('docs', __name__)

@docs.route('/')
def index():
    """
    Show an index template
    :return:
    """
    return response("OK", "EAD REST API", 200)
