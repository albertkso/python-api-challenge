
from datetime import datetime

import csv
import requests
import sys


# Gets raw list of departures and returns filtered list of departures
# which come after 'cutoff_date' and match 'category'

def filter_results(results, cutoff_date, category):

    filtered_results = []
    date_filter = datetime.strptime(cutoff_date, '%Y-%m-%d')

    for item in results: 

        item_category = item['category']
        date_start = datetime.strptime(item['start_date'], '%Y-%m-%d')

        if date_start > date_filter and item_category == category:        
            filtered_results.append(item)

    return filtered_results


# Queries for and returns departure information

def get_departures(query_url):

  # Get departures data
    results = None
    try:
        response_raw = requests.get(query_url)
        response_json = response_raw.json()
        results = response_json['results']
        next_page = response_json['next']
    except:
        print(f'error: exception {sys.exc_info()[0]}')

  # Get next page of departure data, if necessary
    if next_page:
        results = results + get_departures(next_page)

    return results


# Creates CSV file based on contents of 'dataset' and outputs to 'csvfile'

def create_csv(dataset, csv_file):

    with open(csv_file, 'w', newline='') as csvfile:
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
    api_url = 'http://localhost:8000/departures'
    csv_file = 'output.csv'

    results = get_departures(api_url)
    if not results: sys.exit(1)

    filtered_results = filter_results(results, cutoff_date, category)
    create_csv(filtered_results, csv_file)

    sys.exit(0)
