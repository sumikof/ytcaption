import os
import pickle

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.auth.transport.requests import Request

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
client_secrets_file = "client_secret.json"
api_service_name = "youtube"
api_version = "v3"
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


def get_oauth_cred():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                client_secrets_file, scopes)
            creds = flow.run_console()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return googleapiclient.discovery.build(
        api_service_name, api_version, credentials=creds)


if __name__ == '__main__':
    get_oauth_cred()
