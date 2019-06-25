# api_intro.py
# authorize and send requests using OSU's API
import requests

personsUrl = "https://api.oregonstate.edu/v1/persons"
authUrl = "https://api.oregonstate.edu/oauth2/token"

# Request access_token from osu api
# Read in consumer key and consumer secret from user
def get_access_token():
    key = input("Enter Consumer Key: ")
    secret = input("Enter Consumer Secret: ")

    data = {"client_id": key, "client_secret": secret, "grant_type": "client_credentials"}
    request = requests.post(authUrl, data=data)
    response = request.json()

    return response["access_token"]

# Make get request for information about a person at osu
# Read in ONID from user
# requires access_token retrieved in get_access_token()
def get_person(access_token):
    onid = input("Enter Person's ONID: ")

    params = {'onid': onid}
    headers = {"Content-Type": "application/json", "Authorization": "Bearer " + access_token}

    request = requests.get(personsUrl, params=params, headers=headers)
    response = request.json()
    return response["data"]


if __name__ == "__main__":
    access_token = get_access_token()
    personData = get_person(access_token)
    
    for person in personData:
        print("Person's Name: " + person["attributes"]["firstName"])