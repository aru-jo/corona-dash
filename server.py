import flask
from flask import request, jsonify, render_template
import data_request
import pickle
import os
import pandas as pd
from datetime import datetime

# a script to prettify json return from esri arcgis covid data
# to provide a much clearer endpoint for critical data than arcGIS
# updated as soon as it is updated in the covid-19 api
# server script flask api 

if __name__ == '__main__':
	app = flask.Flask(__name__)
	app.config["DEBUG"] = True

	@app.route('/', methods=['GET'])
	def home_page():
		return "<h1> NOW SERVING COVID-19 FLASK PYTHON API </h1>"


	@app.route('/display', methods=['GET'])
	def display_data():
		last_time = False
		if os.path.isfile(os.path.join(os.getcwd(), 'covid_msrt_sort.pkl')):
			with open('covid_msrt_sort.pkl', 'rb') as f_ptr:
				countries_list = pickle.load(f_ptr)
		for row in countries_list:
			# TO-DO : A more robust way to deal with variable order for .values()
			if row[0].strip() == 'US':
				converted_time = row[-1] / 1000
				last_time = datetime.utcfromtimestamp(converted_time).strftime('%Y-%m-%d %H:%M:%S')
			if row[1]:
				row.append(round((row[3] / row[1]) * 100, 2))
				row.append(round((row[2] / row[1]) * 100, 2))
			else:
				row.append(0)
				row.append(0)
		return render_template('table_view.html', table=countries_list, last_updated=last_time)

	@app.route('/api', methods=['GET'])
	def return_data():
		if os.path.isfile(os.path.join(os.getcwd(), 'covid_msrt_api.pkl')):
			with open('covid_msrt_api.pkl', 'rb') as f_ptr:
				covid_data = pickle.load(f_ptr)
		else:
			return "<h2> PICKLE FILE NOT PRESENT IN DIRECTORY </h2>"
		return jsonify(covid_data)

	app.run(host='0.0.0.0')

