import os
from flask import Blueprint, jsonify, request, render_template as view
from app.helper import response
import pandas as pd
import dill as pickle


model = Blueprint('model', __name__)

@model.route('/predict', methods=['POST'])
def predict():
	"""
	Receives input parameters to return a prediction by loading the previously trained model.
	:return: Http Response
	"""
	try:
		test_json = request.get_json()
		return response("OK", test_json, 200)
		test = pd.read_json(test_json, orient='records')
		print(test)


		#To resolve the issue of TypeError: Cannot compare types 'ndarray(dtype=int64)' and 'str'
		test['Dependents'] = [str(x) for x in list(test['Dependents'])]

		#Getting the Loan_IDs separated out
		loan_ids = test['Loan_ID']

	except Exception as e:
		raise e

	clf = 'model_v1.pk'
	
	if test.empty:
		return(bad_request())
	else:
		#Load the saved model
		print("Loading the model...")
		loaded_model = None
		with open('./model/models/' + clf,'rb') as f:
			loaded_model = pickle.load(f)

		print("The model has been loaded...doing predictions now...")
		predictions = loaded_model.predict(test)
		
		"""Add the predictions as Series to a new pandas dataframe
								OR
		   Depending on the use-case, the entire test data appended with the new files
		"""
		prediction_series = list(pd.Series(predictions))

		final_predictions = pd.DataFrame(list(zip(loan_ids, prediction_series)))
		
		"""We can be as creative in sending the responses.
		   But we need to send the response codes as well.
		"""
		responses = jsonify(predictions=final_predictions.to_json(orient="records"))
		responses.status_code = 200

		return (responses)
