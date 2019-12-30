import os

from google_auth_oauthlib.flow import InstalledAppFlow

from video.management.commands.youtube import Youtube


class Command(Youtube):

    def handle(self, *args, **options):
        client_secret_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.CLIENT_SECRET_FILE)
        oauth_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.OAUTH_FILE)
        flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file=client_secret_file, scopes=self.SCOPES)
        credentials = flow.run_console()
        with open(oauth_file, "w") as file:
            file.write(credentials.to_json())

    def __init__(self):
        super().__init__()
