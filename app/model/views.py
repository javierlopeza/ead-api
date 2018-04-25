import os, json
from flask import Blueprint, jsonify, request
from app.helper import response, bad_request
import pandas as pd
import dill as pickle
import sklearn


model = Blueprint('model', __name__)

@model.route('/predict', methods=['POST'])
def predict_example():
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

@model.route('/predict_ead', methods=['POST'])
def predict_ead():
	# Read request data to pandas dataframe
	request_json = json.dumps(request.get_json())
	data = pd.read_json(request_json)
	columns = ['age_months', 'anxiety', 'hand_finger_mannerisms', 'imagination_creativity', 'immediate_echolalia', 'quality_social_overtures', 'self_injurious_behavior', 'shared_enjoyment_interaction', 'tantrums_aggression_disruptive_behavior', 'unusual_eye_contact', 'is_male']
	data = data[columns]

	# Load model 
	model_name = 'model_v1.pk'
	with open('./app/model/models/' + model_name, 'rb') as file:
		model = pickle.load(file)

	# Make predictions
	predictions = model.predict(data)

	# Arrange response data
	final_prediction = int(predictions[0])
	response = jsonify(has_asd=final_prediction)
	response.status_code = 200

	return response


from random import randint
@model.route('/predict2', methods=['POST'])
def predict2():
	response = jsonify(results=[randint(0,10) for _ in range(10)])
	response.status_code = 200
	return response