from flask import Blueprint, render_template as view
from app.helper import response

home = Blueprint('home', __name__)

@home.route('/')
def index():
    """
    Show an index Http response template
    :return: Http Response
    """
    return response("success", "Everything working fine!", 200)
