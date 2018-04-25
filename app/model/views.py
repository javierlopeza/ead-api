import os, json
from flask import Blueprint, jsonify, request
from app.helper import response, bad_request
import pandas as pd
import dill as pickle
import sklearn


model = Blueprint('model', __name__)

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