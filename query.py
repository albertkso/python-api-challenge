
from datetime import datetime

import csv
import requests


def filter_results(results, cutoff_date, category):

    filtered_results = []
    date_filter = datetime.strptime(cutoff_date, '%Y-%m-%d')

    for item in results: 

        item_category = item['category']
        date_start = datetime.strptime(item['start_date'], '%Y-%m-%d')

        if date_start > date_filter and item_category == category:        
            filtered_results.append(item)

    return filtered_results


def get_departures():

    dep_url = 'http://localhost:8000/departures'
    response_raw = requests.get(dep_url)
    response_json = response_raw.json()
    results = response_json['results']

    return results


def create_csv(dataset):

    with open('filtered.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(['Name', 'Start Date', 'Finish Date', 'Category'])

        for item in dataset:
            csvwriter.writerow([
                item['name'], 
                item['start_date'], 
                item['finish_date'], 
                item['category']]
            )
            

if __name__ == '__main__':

    cutoff_date = '2018-06-01'
    category = 'Adventurous'

    results = get_departures()
    filtered_results = filter_results(results, cutoff_date, category)
    create_csv(filtered_results)

