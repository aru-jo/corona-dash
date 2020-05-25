import flask
from flask import request, jsonify, render_template
import data_request
import pickle
import os
from datetime import datetime
from dateutil import tz
import time

if __name__ == '__main__':
	app = flask.Flask(__name__)
	app.config["DEBUG"] = True

	@app.route('/', methods=['GET'])
	def home_page():
		if os.path.isfile(os.path.join(os.getcwd(), 'covid_msrt_sort.pkl')):
			with open('covid_msrt_sort.pkl', 'rb') as f_ptr:
				countries_list = pickle.load(f_ptr)
				total_cases = countries_list[-1]
		return render_template('index.html', total_cases=total_cases) 

	@app.route('/display', methods=['GET'])
	def display_data():
		local_time = False
		from_zone = tz.gettz('UTC')
		to_zone = tz.tzlocal()
		if os.path.isfile(os.path.join(os.getcwd(), 'covid_msrt_sort.pkl')):
			with open('covid_msrt_sort.pkl', 'rb') as f_ptr:
				countries_list = pickle.load(f_ptr)
				del countries_list[-1]
		for row in countries_list:
			# TO-DO : A more robust way to deal with variable order for .values()
			if row[0].strip() == 'US':
				converted_time = row[-1] / 1000
				last_time = datetime.utcfromtimestamp(converted_time).replace(tzinfo=from_zone)
				local_time = last_time.astimezone(to_zone).strftime('%d %b %Y %H:%M')
			if row[1]:
				row.append(round((row[3] / row[1]) * 100, 2))
				row.append(round((row[2] / row[1]) * 100, 2))
			else:
				row.append(0)
				row.append(0)
		return render_template('table_view.html', table=countries_list, last_updated=local_time)

	@app.route('/api', methods=['GET'])
	def display_api_page():
		return render_template('api.html')

	@app.route('/api/v1/countries', methods=['GET'])
	def return_data():
		if os.path.isfile(os.path.join(os.getcwd(), 'covid_msrt_api.pkl')):
			with open('covid_msrt_api.pkl', 'rb') as f_ptr:
				covid_data = pickle.load(f_ptr)
		else:
			return "<h2> PICKLE FILE NOT PRESENT IN DIRECTORY </h2>"
		return jsonify(covid_data)
	
	@app.route('/news', methods=['GET'])
	def get_news():
		if os.path.isfile(os.path.join(os.getcwd(), 'covid_msrt_news.pkl')):
			with open('covid_msrt_news.pkl', 'rb') as f_ptr:
				covid_news_data = pickle.load(f_ptr)
		else:
			return "<h2> PICKLE FILE NOT PRESENT IN DIRECTORY </h2>"
		return render_template('news_view.html', news_data = covid_news_data, length=len(covid_news_data))
	app.run(host='0.0.0.0')
