# api_intro.py
# authorize and send requests using OSU's API
import json
import sys

import requests


# Request access_token from osu api
# Read in consumer key and consumer secret from user
def get_access_token(authUrl, id, secret):
    data = {'client_id': id, 'client_secret': secret,
            'grant_type': 'client_credentials'}
    request = requests.post(authUrl, data=data)
    response = request.json()

    try:
        response['access_token']
        return response['access_token']
    except KeyError:
        if request.status_code != 200:
            print('Client Id or Client Secret invalid. '
                  f'Please check your configuration.json '
                  f'file and try again.')
        else:
            print('Unknown error occurred.')
        exit()


# Make get request for information about a person at osu
# Read in ONID from user
# requires access_token retrieved in get_access_token()
def get_person(access_token, api_url):
    response_data = []
    while len(response_data) < 1:
        onid = input('Enter Person\'s ONID: ')

        params = {'onid': onid}
        headers = {'Content-Type': 'application/json',
                   'Authorization': f'Bearer {access_token}'}

        request = requests.get(api_url, params=params, headers=headers)
        response = request.json()
        response_data = response['data']
        if len(response_data) < 1:
            print(f'No data found for \"{onid}\". '
                  f'Please try a different search query.')

    return response_data


# Requests OSU directory information using api
# requires an access token and api url to be passed in
# asks for search query from user
# returns data if the search query finds some.
# If no data is found the user is asked again to enter a query
def get_directory(access_token, apiUrl):
    response_data = []
    while len(response_data) < 1:
        query = input('Enter Directory Search Query: ')

        params = {'q': query}
        headers = {'Content-Type': 'application/json',
                   'Authorization': f'Bearer {access_token}'}

        request = requests.get(apiUrl, params=params, headers=headers)
        response = request.json()
        response_data = response['data']
        if len(response_data) < 1:
            print(f'No data found for \"{query}\". '
                  f'Please try a different search query.')
    return response['data']


if __name__ == '__main__':
    config_path = sys.argv[1]
    with open(config_path, 'r') as configFile:
        config = json.load(configFile)
        persons_url = config['api']['persons_url']
        directory_url = config['api']['directory_url']
        auth_url = config['oauth2']['auth_api_url']
        client_id = config['oauth2']['client_id']
        client_secret = config['oauth2']['client_secret']

    access_token = get_access_token(auth_url, client_id, client_secret)
    directory_data = get_directory(access_token, directory_url)

    for directory in directory_data:
        print(directory['attributes']['firstName'])
