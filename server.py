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

if __name__ == '__main__':
	app = flask.Flask(__name__)
	app.config["DEBUG"] = True

	@app.route('/', methods=['GET'])
	def home_page():
		return "<h1> NOW SERVING COVID-19 FLASK PYTHON API </h1>"


	@app.route('/display', methods=['GET'])
	def display_data():
		lst = []
		if os.path.isfile(os.path.join(os.getcwd(), 'covid_msrt.pkl')):
			with open('covid_msrt.pkl', 'rb') as f_ptr:
				countries_dict = pickle.load(f_ptr)
		for country_dict in countries_dict:
			row = list(country_dict.values())
			# TO-DO : A more robust way to deal with variable order for .values()
			row[-1] /= 1000
			row[-1] = datetime.utcfromtimestamp(row[-1]).strftime('%Y-%m-%d %H:%M:%S')
			row.append(round((row[3]/row[1])*100, 2))
			row.append(round((row[2]/row[1])*100, 2))
			lst.append(row)
		lst.sort(key=lambda x: x[1], reverse=True)
		# return jsonify(lst)
		return render_template('table_view.html', table=lst)


	@app.route('/api', methods=['GET'])
	def return_data():
		if os.path.isfile(os.path.join(os.getcwd(), 'covid_msrt.pkl')):
			with open('covid_msrt.pkl', 'rb') as f_ptr:
				covid_data = pickle.load(f_ptr)
		else:
			return "<h2> PICKLE FILE NOT PRESENT IN DIRECTORY </h2>"
		return jsonify(covid_data)

	app.run(host='0.0.0.0')



