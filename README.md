# Alex API Intro ![python](https://img.shields.io/badge/python-3.7-blue.svg)

Introduction to using OSU's APIs

## Configuration

1. Register an application on [OSU Developer Portal](https://developer.oregonstate.edu/)
2. Get `client_id` and `client_secret` from your app, then copy[configuration-example.json](./configuration-example.json) as `configuration.json` and fill in the oauth2 section:

    ```json
    "oauth2": {
        "auth_api_url": "https://api.oregonstate.edu/oauth2/token",
        "client_id": "your_client_id",
        "client_secret": "your_client_secret"
    }
    ```

## Usage

1. Install dependencies via pip:

    ```shell
    $ pip install -r requirements.txt
    ```
2. Run the script:

    ```shell
    $ python api_intro.py --config path/to/configuration.json
    ```