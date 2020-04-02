import requests
import time
import pickle
import requests
import json
from datetime import datetime

API_ENDPOINT = 'https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/Coronavirus_2019_nCoV_Cases/FeatureServer/2/query?where=1%3D1&outFields=Country_Region,Confirmed,Deaths,Recovered,Last_Update&outSR=4326&f=json'


def request_data():
    req = requests.get(API_ENDPOINT)
    if req.status_code == 200:
        json_data = req.json()
        return json_data
    else:
        return False


def simplify_data_return(data_ret):
    countries_dict = data_ret["features"]
    return [country_dict["attributes"] for country_dict in countries_dict]


def initial_sort(countries_dict):
    lst = [list(country_dict.values()) for country_dict in countries_dict]
    lst.sort(key=lambda x: x[1], reverse=True)
    return lst


def pickle_data_sorted(sorted_datum):
    with open('covid_msrt_sort.pkl', 'wb') as f_ptr:
        pickle.dump(sorted_datum, f_ptr)


def pickle_data_api(data):
    with open('covid_msrt_api.pkl', 'wb') as f_ptr:
        pickle.dump(data, f_ptr)


if __name__ == '__main__':
    while True:
        now = datetime.now()
        print("Current date and time : ")
        print(now.strftime("%Y-%m-%d %H:%M:%S"))
        most_recent_data = request_data()
        print('Data Acquired...')
        simplified_data = simplify_data_return(most_recent_data)
        print('Data Simplified...')
        pickle_data_api(simplified_data)
        print('API Data Pickled...')
        sorted_data = initial_sort(simplified_data)
        print('Data Sorted...')
        pickle_data_sorted(sorted_data)
        print('Data Pickled...')
        time.sleep(3600)
