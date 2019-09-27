Development (Ubuntu):
1. Install Python:

    `sudo apt install -y python3`
    
2. Install venv:

    `sudo apt install -y python3-venv`
    
3. Switch to a directory where the virtual environment is to be stored and create one:

    `python3 -m venv vcelnice-env`
    
4. Activate environment:

    `source vcelnice-env/bin/activate`

5. Switch to the project directory, install dependencies:
    
    `pip install -r requirements.txt`
    
6. Create folder for logs:

    `mkdir -m 777 <project folder>/vcelnice/logs`
    
7. Create administrator:

    `python manage.py createsuperuser`
    
7. Run server:

    `python manage.py runserver 0.0.0.0:2020 --settings=vcelnice.settings.development`
    
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
