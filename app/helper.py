from flask import jsonify, make_response
from app import app


def response(status, message, status_code):
    """
    Make an http response helper
    :param status: Status message
    :param message: Response Message
    :param status_code: Http response code
    :return: Http response
    """
    return make_response(jsonify({
        'status': status,
        'message': message
    })), status_code

def bad_request():
    """
    Make an http response helper for a bad request
    :return: Http response
    """
    return make_response(jsonify({
        'status': "failed",
        'message': "Bad request, check your data payload"
    })), 400