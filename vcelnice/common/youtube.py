#!/usr/bin/python
# Code samples:
# https://developers.google.com/youtube/v3/code_samples/python#retrieve_my_uploads
import argparse
import json
import sys
from google_auth_oauthlib.flow import Flow
from google_auth_oauthlib.flow import InstalledAppFlow

import httplib2
import logging
import random
import re
import requests
import time
from vcelnice.settings import *
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from oauth2client.file import Storage
from oauth2client.client import flow_from_clientsecrets
from oauth2client.tools import run_flow, argparser


class Youtube:
    # Google API key
    # https://developers.google.com/api-client-library/python/guide/aaa_apikeys
    VIDEO_CATEGORIES_URL = 'https://www.googleapis.com/youtube/v3/videoCategories'
    API_KEY = 'AIzaSyAyatqlKdkU13xmdJMNr0xPSEdqnT-WLs8'
    CREDENTIALS_DIR = '.credentials'
    CLIENT_SECRET_FILE = 'youtube-python-vcelnice.json'
    CLIENT_OAUTH2_FILE = 'youtube-oauth2.json'

    # Maximum number of times to retry before giving up.
    MAX_RETRIES = 10

    # Always retry when these exceptions are raised.
    RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError)

    # Always retry when an apiclient.errors.HttpError with one of these status
    # codes is raised.
    RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

    VALID_PRIVACY_STATUSES = ('public', 'private', 'unlisted')

    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"
    YOUTUBE_SCOPE = 'https://www.googleapis.com/auth/youtube'
    SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']

    # This variable defines a message to display if the CLIENT_SECRETS_FILE is
    # missing.
    MISSING_CLIENT_SECRETS_MESSAGE = """
    WARNING: Please configure OAuth 2.0
    To make this sample run you will need to populate the client_secrets.json file
    found at:
       %s
    with information from the APIs Console
    https://console.developers.google.com
    For more information about the client_secrets.json file format, please visit:
    https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
    """ % os.path.abspath(os.path.join(os.path.dirname(__file__), CREDENTIALS_DIR, CLIENT_SECRET_FILE))

    def __init__(self):
        self.cwd = os.path.dirname(os.path.abspath(__file__))
        self.CLIENT_CREDENTIALS = os.path.join(self.cwd, 'auth.dat')
        self.logger = logging.getLogger('vcelnice.info')
        # self.youtube = self.get_authenticated_service()

    def get_credentials_files(self, client_config=None):
        # Define files
        cred_dir = os.path.dirname(os.path.abspath(__file__))
        credential_dir = os.path.join(cred_dir, self.CREDENTIALS_DIR)
        # Create .credentials dir, if not exist
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        client_secret = os.path.join(credential_dir, self.CLIENT_SECRET_FILE)
        oauth = os.path.join(credential_dir, self.CLIENT_OAUTH2_FILE)
        # Write client file, if defined
        if client_config is not None:
            key = "installed"
            data = {}
            out = {}
            config_data = client_config[key]
            for line in config_data:
                data[line] = config_data[line]
            out[key] = data
            with open(client_secret, "w") as file:
                json.dump(out, file)
        return client_secret, oauth

    def get_authorization_url(self, client_config):
        credentials_file, oauth_file = self.get_credentials_files(client_config)
        # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
        flow = Flow.from_client_secrets_file(credentials_file, scopes=self.YOUTUBE_SCOPE)
        # The URI created here must exactly match one of the authorized redirect URIs
        # for the OAuth 2.0 client, which you configured in the API Console. If this
        # value doesn't match an authorized URI, you will get a 'redirect_uri_mismatch'
        # error.
        flow.redirect_uri = "urn:ietf:wg:oauth:2.0:oob"

        authorization_url, state = flow.authorization_url(
            # Enable offline access so that you can refresh an access token without
            # re-prompting the user for permission. Recommended for web server apps.
            access_type='offline',
            # Enable incremental authorization. Recommended as a best practice.
            include_granted_scopes='true')
        return authorization_url

    def authorize(self, code):
        credentials_file, oauth_file = self.get_credentials_files()
        flow = InstalledAppFlow.from_client_secrets_file(credentials_file, self.YOUTUBE_SCOPE)
        credentials = flow.run_console()
        print("Code: ", build(self.YOUTUBE_API_SERVICE_NAME, self.YOUTUBE_API_VERSION, credentials=credentials))
        # flow = Flow.from_client_config(credentials_file, scopes=self.YOUTUBE_SCOPE, state=state)
        # flow.redirect_uri = redirect_uri
        # os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
        # flow.fetch_token(authorization_response=request_url)
        # os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '0'
        # credentials = flow.credentials
        # youtube_credentials = {
        #     'token': credentials.token,
        #     'refresh_token': credentials.refresh_token,
        #     'token_uri': credentials.token_uri,
        #     'client_id': credentials.client_id,
        #     'client_secret': credentials.client_secret,
        #     'scopes': credentials.scopes
        # }
        # print("Credentials: ", youtube_credentials)
        return None

    def get_credentials_storage(self):
        credentials_file, oauth_file = self.get_credentials_files()
        storage = Storage(oauth_file)
        return storage.get()

    def is_authorized(self):
        credentials = self.get_credentials_storage()
        return credentials is not None and credentials.valid

    # https://github.com/youtube/api-samples/blob/master/python/captions.py
    def get_authenticated_service(self):
        credentials_file, oauth_file = self.get_credentials_files()
        flow = flow_from_clientsecrets(credentials_file, scope=self.YOUTUBE_SCOPE,
                                       message=self.MISSING_CLIENT_SECRETS_MESSAGE)
        storage = Storage(oauth_file)
        credentials = storage.get()

        if credentials is None or credentials.invalid:
            flags = argparser.parse_args(args=[])
            auth_data = run_flow(flow, storage, flags=flags)
            print('Auth Data: ', auth_data)
        return None

        # store = Storage(credential_path)
        # credentials = store.get()
        #
        # if credentials is None:
        #     self.logger.critical('Unable to find Youtube credentials storage %s' % self.CLIENT_CREDENTIALS)
        #     return None
        #
        # if credentials.invalid:
        #     self.logger.critical('Youtube credentials are invalid %s' % self.CLIENT_CREDENTIALS)
        #     return None
        #
        # return build(self.YOUTUBE_API_SERVICE_NAME,
        #              self.YOUTUBE_API_VERSION,
        #              http=credentials.authorize(httplib2.Http()))

    def get_categories(self):
        payload = {'part': 'snippet', 'regionCode': 'CZ', 'key': self.API_KEY}
        request = requests.get(self.VIDEO_CATEGORIES_URL, payload)
        data = request.json()

        if 'items' in data:
            return [(item['id'], item['snippet']['title']) for item in data['items']]
        else:
            return []

    def get_uploaded_video(self, video_id):
        try:
            result = self.youtube.videos().list(
                part='snippet',
                id=video_id
            ).execute()
            return result['items'][0]['snippet']
        except HttpError as e:
            self.logger.critical('Error retrieving video %s, reason: %s' % (video_id, e.content))
            return None

    def get_uploaded_videos(self):
        response = []
        channel_response = self.youtube.channels().list(
            mine=True,
            part='contentDetails'
        ).execute()

        for channel in channel_response['items']:
            # From the API response, extract the playlist ID that identifies the list
            # of videos uploaded to the authenticated user's channel.
            uploads_list_id = channel["contentDetails"]["relatedPlaylists"]["uploads"]

            # Retrieve the list of videos uploaded to the authenticated user's channel.
            playlistitems_list_request = self.youtube.playlistItems().list(
                playlistId=uploads_list_id,
                part="snippet",
                maxResults=50
            )

            while playlistitems_list_request:
                playlistitems_list_response = playlistitems_list_request.execute()

                for playlist_item in playlistitems_list_response['items']:
                    response.append(playlist_item["snippet"]["resourceId"]["videoId"])

                playlistitems_list_request = self.youtube.playlistItems().list_next(
                    playlistitems_list_request, playlistitems_list_response)

        return response

    def upload(self, video):
        # Explicitly tell the underlying HTTP transport library not to retry, since
        # we are handling retry logic ourselves.
        httplib2.RETRIES = 1

        try:
            self.upload_file(video)
        except HttpError as e:
            self.logger.critical("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))

    def upload_file(self, video):
        # Get data from model
        if video.tags is not None:
            tags = [tag.strip() for tag in video.tags.split(',')]
        else:
            tags = None
        file_path = os.path.join(MEDIA_ROOT, video.file.name)
        body = dict(
            snippet=dict(
                title=video.caption,
                description=video.description,
                tags=tags
            ),
            status=dict(
                privacyStatus='public'
            )
        )

        # Call the API's videos.insert method to create and upload the video.
        insert_request = self.youtube.videos().insert(
            part=",".join(body.keys()),
            body=body,
            # The chunksize parameter specifies the size of each chunk of data, in
            # bytes, that will be uploaded at a time. Set a higher value for
            # reliable connections as fewer chunks lead to faster uploads. Set a lower
            # value for better recovery on less reliable connections.
            #
            # Setting "chunksize" equal to -1 in the code below means that the entire
            # file will be uploaded in a single HTTP request. (If the upload fails,
            # it will still be retried where it left off.) This is usually a best
            # practice, but if you're using Python older than 2.6 or if you're
            # running on App Engine, you should set the chunksize to something like
            # 1024 * 1024 (1 megabyte).
            media_body=MediaFileUpload(file_path, chunksize=-1, resumable=True)
        )
        self.resumable_upload(insert_request, video)

    # This method implements an exponential backoff strategy to resume a failed upload.
    def resumable_upload(self, request, video):
        response = None
        error = None
        retry = 0

        while response is None:
            try:
                status, response = request.next_chunk()

                if response is not None:
                    if 'id' in response:
                        video.youtube_id = response['id']
                        video.save()
                        video.save_upload_status()
                        self.upload_video_thumbnail(response['id'], video.thumb.name)
                        self.logger.info("Video id '%s' was successfully uploaded." % response['id'])
                    else:
                        self.logger.error('The upload failed with an unexpected response: %s' % response)
                        exit()
            except HttpError as e:
                if e.resp.status in self.RETRIABLE_STATUS_CODES:
                    error = 'A retriable HTTP error %d occurred:\n%s' % (e.resp.status, e.content)
                else:
                    raise
            except self.RETRIABLE_EXCEPTIONS as e:
                error = 'A retriable error occurred: %s' % e

            if error is not None:
                self.logger.error(error)
                retry += 1
                if retry > self.MAX_RETRIES:
                    self.logger.error('Youtube upload interrupted, reason: number of attempts exceeded')
                    exit()

                max_sleep = 2 ** retry
                sleep_seconds = random.random() * max_sleep
                self.logger.info("Sleeping %f seconds and then retrying..." % sleep_seconds)
                time.sleep(sleep_seconds)

    def upload_video_thumbnail(self, video_id, filename):
        if filename == '':
            return

        file_path = os.path.join(MEDIA_ROOT, filename)

        if not os.path.exists(file_path):
            return self.logger.error('Thumbnail %s for youtube video %i not found' % (filename, video_id))

        try:
            self.youtube.thumbnails().set(
                videoId=video_id,
                media_body=os.path.join(MEDIA_ROOT, filename)
            ).execute()
            self.logger.info("Thumbnail %s updated for video %s" % (filename, video_id))
        except HttpError as e:
            self.logger.critical(
                "An HTTP error %d occurred while uploading video thumbnail: %s" % (e.resp.status, e.content))

    def update_video(self, video):
        try:
            tags = [tag.strip() for tag in video.tags.split(',')]
            self.youtube.videos().update(
                part='snippet',
                body=dict(
                    snippet=dict(
                        title=video.caption,
                        description=video.description,
                        tags=tags,
                        categoryId=int(video.category)
                    ),
                    id=video.youtube_id
                )
            ).execute()
            self.upload_video_thumbnail(video.youtube_id, video.thumb.name)
            return True
        except HttpError as e:
            self.logger.critical(
                "An HTTP error %d occurred while updating video %s: %s" % (video.youtube_id, e.resp.status, e.content))
        return False

    def delete_video(self, video_id):
        try:
            self.youtube.videos().delete(id=video_id).execute()
            self.logger.info('Youtube video %s was successfully deleted' % video_id)
            return True
        except HttpError as e:
            self.logger.critical(
                "An HTTP error %d occurred while deleting video: %s" % (e.resp.status, e.content))
        return False

    @staticmethod
    def validate_embed_link(link):
        regex = re.compile(r'^.*(youtu.be/|v/|u/\w/|embed/|watch\?v=|&v=)([^#&\?]*).*')
        return regex.match(link)
