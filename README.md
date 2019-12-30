# NYC Park Alerts

You can sign up for free at https://parks.simon.codes/ to receive alerts about locations you frequent.

The rest of this page is intended for developers.

## dev 

one time:
* install heroku: https://devcenter.heroku.com/articles/heroku-cli
* install postgres: https://devcenter.heroku.com/articles/heroku-postgresql#local-setup
* set up and activate a new venv
* `pip install -r requirements.txt`
* createdb notices
* `export DATABASE_URL=postgres:///notices`
* python manage.py migrate
* python manage.py collectstatic

to run:
* ensure DATABASE_URL is set
* `python manage.py runserver`
* to run the scrape/notify job once: `python manage.py runscript -v2 parkalerts.core.scrape`: 
