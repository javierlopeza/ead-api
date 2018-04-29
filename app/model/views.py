import os, json
from flask import Blueprint, jsonify, request
from app.helper import response, bad_request
import pandas as pd
import dill as pickle
import sklearn


model = Blueprint('model', __name__)

def risk_level(asd_prob):
	low = 0.33
	medium = 0.66
	high = 1.0
	if asd_prob < low: return "Low Risk"
	if asd_prob < medium: return "Medium Risk"
	if asd_prob <= high: return "High Risk"


@model.route('/predict_ead', methods=['POST'])
def predict_ead():
	# Read request data to pandas dataframe
	request_json = json.dumps(request.get_json())
	data = pd.read_json(request_json)
	columns = ['age_months', 'anxiety', 'hand_finger_mannerisms', 'imagination_creativity', 'immediate_echolalia', 'quality_social_overtures', 'self_injurious_behavior', 'shared_enjoyment_interaction', 'tantrums_aggression_disruptive_behavior', 'unusual_eye_contact', 'is_male']
	data = data[columns]

	# Load model 
	model_name = 'model_v4.pk'
	with open('./app/model/models/' + model_name, 'rb') as file:
		model = pickle.load(file)

	# Make predictions
	predictions = model.predict(data)
	probabilities = model.predict_proba(data)
	print("PROBABILITY:", probabilities)
	print("PREDICTIONS:", predictions)

	# Arrange response data
	has_asd = int(predictions[0])
	asd_prob = float(probabilities[0][1])
	risk_lvl = risk_level(asd_prob)
	asd_percentage = "{:.0%}".format(asd_prob)
	response = jsonify(asd_probability=asd_prob, has_asd=has_asd, asd_percentage=asd_percentage, risk_level=risk_lvl)
	response.status_code = 200

	print(response.data)

	return response