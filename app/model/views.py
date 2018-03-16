import os, json
from flask import Blueprint, jsonify, request
from app.helper import response, bad_request
import pandas as pd
import dill as pickle
import sklearn


model = Blueprint('model', __name__)

@model.route('/predict', methods=['POST'])
def predict():
	"""
	Receives input parameters to return a prediction 
	by loading the previously trained model.
	:return: Http response
	"""
	# Read request data
	request_json = json.dumps(request.get_json())
	test = pd.read_json(request_json, orient="records")
	test = test[["CRIM", "ZN", "INDUS", "CHAS", "NOX", "RM", "AGE", "DIS", "RAD", "TAX", "PTRATIO", "B", "LSTAT"]]

	# Load model
	model_name = 'model_example.pk'
	with open('./app/model/models/' + model_name, 'rb') as file:
		model = pickle.load(file)

	# Make predictions
	predictions = model.predict(test)

	# Arrange response data
	final_predictions = [{"price": p[0]} for p in predictions]
	
	responses = jsonify(predictions=final_predictions)
	responses.status_code = 200

	return responses
