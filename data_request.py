import requests
import time
import pickle
import json
from datetime import datetime
from newsapi import NewsApiClient
NEWS_KEY = '324e8b378e9c44b2b4618956325d7307'
API_ENDPOINT = 'https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/Coronavirus_2019_nCoV_Cases/FeatureServer/2/query?where=1%3D1&outFields=Country_Region,Confirmed,Deaths,Recovered,Last_Update&outSR=4326&f=json'
TOTAL_CASES_ENDPOINT = 'https://corona-virus-stats.herokuapp.com/api/v1/cases/general-stats'

def request_data(endpoint):
    req = requests.get(endpoint)
    if req.status_code == 200:
        json_data = req.json()
        return json_data
    else:
        return False

def total_cases(d):
    try: 
        lst = [('Total Cases', d["data"]["total_cases"]),
                    ('Recovered Cases', d["data"]["recovery_cases"]),
                    ('Deaths', d["data"]["death_cases"]),
                    ('Last Updated', d["data"]["last_update"])]
    except TypeError:
        lst = False
    return lst

def request_news(query):
    newsapi = NewsApiClient(api_key=NEWS_KEY)
    top_headlines = newsapi.get_top_headlines(q=query, language='en', page_size=100)
    return top_headlines

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

def pickle_news(news_data):
    with open('covid_msrt_news.pkl', 'wb') as f_ptr:
        pickle.dump(news_data, f_ptr)


def return_top_k_news_results(data_ret, k):
    print(len(data_ret["articles"]))
    lst_of_articles = []
    top_k_articles = data_ret["articles"][:k]
    for article in top_k_articles:
        source = article["source"]["name"]
        title = article["title"]
        description = article["description"]
        url = article["url"]
        lst_of_articles.append([source, title, description, url])
    return lst_of_articles


if __name__ == '__main__':
    now = datetime.now()
    print("Current date and time : ")
    print(now.strftime("%Y-%m-%d %H:%M:%S"))
    most_recent_data = request_data(API_ENDPOINT)
    print('Original Data Acquired...')
    simplified_data = simplify_data_return(most_recent_data)
    print('Original Data Simplified...')
    pickle_data_api(simplified_data)
    print('API Data Pickled...')
    sorted_data = initial_sort(simplified_data)
    total_cases_lst = total_cases(request_data(TOTAL_CASES_ENDPOINT))
    if total_cases_lst:
        sorted_data.append(total_cases_lst)
    else:
        sorted_data.append(False)
    print(sorted_data[-1])
    print('Display Data Sorted...')
    pickle_data_sorted(sorted_data)
    print('Display Data Pickled...')
    simplify_news = return_top_k_news_results(request_news('COVID'), 20)
    print('News Data Acquired...')
    pickle_news(simplify_news)
    print('News & Total Cases Data Pickled...')
    # time.sleep(3000)