from flask import Blueprint, render_template as view
from app.helper import response

predictions = Blueprint('predictions', __name__)

@predictions.route('/predict')
def predict():
    """
    Show an index template
    :return:
    """
    return response("OK", "EAD REST API - Predictions", 200)
