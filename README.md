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

    `django-admin makemessages -a` or `django-admin makemessages -l cs`
    
4. After all strings are translated, compile:

    `django-admin compilemessages`