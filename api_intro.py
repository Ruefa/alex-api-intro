# api_intro.py
# authorize and send requests using OSU's API
import requests

personsUrl = "https://api.oregonstate.edu/v1/persons"
authUrl = "https://api.oregonstate.edu/oauth2/token"

def get_access_token():
    key = input("Enter Consumer Key: ")
    secret = input("Enter Consumer Secret: ")