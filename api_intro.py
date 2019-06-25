# api_intro.py
# authorize and send requests using OSU's API
import json
import sys

import requests


def get_access_token(authUrl, id, secret):
    """Request access_token from osu api
    Read in consumer key and consumer secret from user"""

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


def get_person(access_token, api_url):
    """Make get request for information about a person at osu
    Read in ONID from user
    requires access_token retrieved in get_access_token()"""

    while True:
        onid = input('Enter Person\'s ONID: ')

        params = {'onid': onid}
        headers = {'Content-Type': 'application/json',
                   'Authorization': f'Bearer {access_token}'}

        request = requests.get(api_url, params=params, headers=headers)
        response = request.json()
        response_data = response['data']
        if response_data:
            return response_data
        else:
            print(f'No data found for \"{onid}\". '
                  f'Please try a different search query.')


def get_directory(access_token, apiUrl):
    """Requests OSU directory information using api
    requires an access token and api url to be passed in
    asks for search query from user
    returns data if the search query finds some.
    If no data is found the user is asked again to enter a query"""

    while True:
        query = input('Enter Directory Search Query: ')

        params = {'q': query}
        headers = {'Content-Type': 'application/json',
                   'Authorization': f'Bearer {access_token}'}

        request = requests.get(apiUrl, params=params, headers=headers)
        response = request.json()
        response_data = response['data']
        if response_data:
            return response['data']
        else:
            print(f'No data found for \"{query}\". '
                  f'Please try a different search query.')


if __name__ == '__main__':
    CONFIG_API = 'api'
    CONFIG_OAUTH = 'oauth2'

    config_path = sys.argv[1]
    with open(config_path, 'r') as configFile:
        config = json.load(configFile)
        persons_url = config[CONFIG_API]['persons_url']
        directory_url = config[CONFIG_API]['directory_url']
        auth_url = config[CONFIG_OAUTH]['auth_api_url']
        client_id = config[CONFIG_OAUTH]['client_id']
        client_secret = config[CONFIG_OAUTH]['client_secret']

    access_token = get_access_token(auth_url, client_id, client_secret)
    directory_data = get_directory(access_token, directory_url)

    for directory in directory_data:
        print(directory['attributes']['firstName'])
