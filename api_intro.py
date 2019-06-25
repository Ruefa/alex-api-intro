# api_intro.py
# authorize and send requests using OSU's API
import sys

import json
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
        if response["ErrorCode"] == "invalid_client":
            print("Client Id or Client Secret invalid. "
                  + "Please check your configuration.json "
                  + "file and try again.")
        else:
            print("Unknown error occurred.")
        exit()


# Make get request for information about a person at osu
# Read in ONID from user
# requires access_token retrieved in get_access_token()
def get_person(access_token, apiUrl):
    responseData = []
    while len(responseData) < 1:
        onid = input('Enter Person\'s ONID: ')

        params = {'onid': onid}
        headers = {'Content-Type': 'application/json',
                   'Authorization': f'Bearer {access_token}'}

        request = requests.get(apiUrl, params=params, headers=headers)
        response = request.json()
        responseData = response['data']
        if len(responseData) < 1:
            print(f'No data found for \"{onid}\". '
                  + 'Please try a different search query.')

    return responseData


def get_directory(access_token, apiUrl):
    osuId = input('Enter Directory Search Query: ')

    # params = {'q': onid}
    headers = {'Content-Type': 'application/json',
               'Authorization': f'Bearer {access_token}'}

    request = requests.get(f'{apiUrl}/{osuId}', headers=headers)
    response = request.json()
    print(response)
    return response['data']


if __name__ == '__main__':
    configPath = sys.argv[1]
    with open(configPath, 'r') as configFile:
        config = json.load(configFile)
        personsUrl = config['api']['persons_url']
        directoryUrl = config['api']['directory_url']
        authUrl = config['oauth2']['auth_api_url']
        clientId = config['oauth2']['client_id']
        clientSecret = config['oauth2']['client_secret']

    access_token = get_access_token(authUrl, clientId, clientSecret)
    personsData = get_person(access_token, personsUrl)

    for person in personsData:
        print(f'Name: {person["attributes"]["firstName"]}')
