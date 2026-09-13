Install:
1. Install Python:

    `sudo apt install -y python3`
    
2. Install venv:

    `sudo apt install -y python3-venv`
    
Run: 

1. Switch to a directory where the virtual environment is to be stored and create one:

    `python3 -m venv .venv`
    
2. Activate environment:

    `source .venv/bin/activate`

3. Switch to the project directory, install dependencies:
    
    `pip install -r requirements.txt`
    
4. Create folder for logs:

    `mkdir -m 777 <project folder>/vcelnice/logs`
    
5. Create administrator:

    `python manage.py createsuperuser`
    
6. Change password: 
    
    `python manage.py changepassword <user_name>`
    
7. Run server:

    `python manage.py runserver 0.0.0.0:8888 --settings=vcelnice.settings.development`
    
Client:

1. Install Node.js:

    `curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -`
    
    `sudo apt-get install -y nodejs`

2. Install Angular CLI:

    `npm install -g @angular/cli`
    
3. Install dependencies:

    `npm install`
    
4. Install Fancyapps:

    `npm i @fancyapps/fancybox`
    
Deployment:
    
1. Build client:
    
    `npm run build`
    
2. Collect static files, from project directory:

    `python manage.py collectstatic`
    
Localizing:

1. Import translator:
    
    `from django.utils.translation import ugettext_lazy as _`

2. Localize fields:

    - Model names: `name = models.TextField(_("Some help text"))`

3. Update translation files:

    `django-admin makemessages -a` or `django-admin makemessages -l cs --ignore={node_modules,dist,static_root}`
    
4. After all strings are translated, compile:

    `django-admin compilemessages`

Deploying to PythonAnywhere:

1. Build project with Docker:
   
   `docker compose up`

2. Upload to PythonAnywhere:

   `scp vcelnice.zip <username>@ssh.pythonanywhere.com:~/vcelnice`

3. Login to web interface, unzip archive overwriting the files:

   `unzip -o vcelnice.zip`

4. Reload the app, if necessary. No need to collect static, as all directories are updated during build

## Video administration: manual YouTube links

Upload videos through YouTube directly, then add a Video in Django admin with its
caption, optional description/thumbnail and the 11-character **YouTube video ID**
(for example, `qH6i5JsntCw`, not a full URL). Leave the ID blank to keep the record
off the website. There is no original video-file upload control or field; playback
uses only the YouTube ID. An optional thumbnail can still be uploaded.

Saving or deleting a Video now changes only the local record. It never updates or
deletes anything on YouTube. Manage the actual YouTube video manually. Django's
normal deletion does not remove the original media files from storage.

The public `/api/v1/videos/` endpoint still supplies `youtube_id`, `caption`,
`description` and `thumb` for the current Angular player. The removed `file`,
`category`, `tags` and `youtube_status` fields are no longer returned; there are no changes to
the Angular player or the production referrer policy.

### Deploying the upload-workflow removal

1. Disable any external scheduled jobs invoking `youtube_authorize`,
   `youtube_categories`, `youtube_upload`, `youtube_update` or `youtube_delete`.
   No scheduler configuration is stored in this repository.
2. Back up the database and media before applying migration
   `video.0004_remove_youtube_upload_workflow`. It drops `category`, `tags`,
   `youtube_status` and the `VideoCategory` table. Existing Video records, YouTube
   IDs and media paths are retained. Reversing the schema migration cannot restore
   data from the removed columns/table; recovering that data requires the backup.
   Review any records with a nonblank `youtube_id` and an old `youtube_status`
   of NULL or <=1: these were previously hidden. The migration deliberately stops
   if it finds them, before removing any fields. After review, clear their ID to
   keep them hidden, or set the old status to uploaded (2) only if they should be
   public. The migration never clears IDs or publishes such drafts automatically.
   The following migration, `video.0005_remove_video_file`, drops the original
   file-path column. It preserves Video records, YouTube IDs, thumbnails and
   timestamps, and does not delete any existing media files from storage. Back
   up the database if you need to retain the old file-to-video associations;
   reversing this migration cannot recover those paths.
3. Deploy the updated code and dependencies, apply the migration, then reload
   Django. Do not serve the old code against the new schema. Using the appropriate
   environment settings, run:

   ```bash
   python -m pip install -r requirements.txt
   python manage.py migrate
   python manage.py compilemessages -l cs
   ```

4. Deploy into a clean release directory, or explicitly remove the retired files
   from the old deployment. **`unzip -o` does not remove files absent from the new
   archive.** Retired files are `vcelnice/common/youtube.py` and the former
   `video/management/` package, including `youtube.py`, `youtube_authorize.py`,
   `youtube_categories.py`, `youtube_upload.py`, `youtube_update.py`,
   `youtube_delete.py`, `client_secret.json` and `youtube-oauth2.json` under
   `video/management/commands/`. Do not remove Gmail's credential directory.
5. Check Video admin add/edit/list/delete and `/api/v1/videos/`, then verify video
   playback in the UI. The Google API/HTTP dependencies used by Gmail remain;
   only the uploader-specific `google-auth-oauthlib` requirement was removed.
   Removing the original-file field also removes the unused filename-normalization
   helper and its `transliterate` dependency.

The retired YouTube credential files were tracked in Git. Removing them from the
current tree does not erase history or revoke access. Revoke the obsolete YouTube
authorization and rotate any reusable exposed credentials as appropriate; keep
Gmail authorization separate. No credentials are revoked automatically.
