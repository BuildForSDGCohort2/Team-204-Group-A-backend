# Team-204-Group-A-backend

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/9179bdde292d4fc1b7e8fb9847318687)](https://app.codacy.com/gh/BuildForSDGCohort2/Team-204-Group-A-backend?utm_source=github.com&utm_medium=referral&utm_content=BuildForSDGCohort2/Team-204-Group-A-backend&utm_campaign=Badge_Grade_Dashboard)

## PrescibeMe
```
PrescribeMe helps patient (client) get prescription or Book a meeting in hospital. Patient gets to contact provider for quick diagnosis and prescription and can order medication only or book a appointment with the doctor.
```

# PrescribeMe API Endpoints
|Endpoint                                 | Functionality                    |HTTP method 
|-----------------------------------------|----------------------------------|-------------
|/api/v1/user/signup                      |Signup account                    |POST 

## Technologies

* Python 3.5

## Requirements

* Install [Python](https://www.python.org/downloads/)
* Run `pip install virtualenv` on command prompt
* Run `pip install virtualenvwrapper-win` on command prompt

## Setup

* Run `git clone` this repository and `cd Team-204-Group-A-backend` .
* Run `python3 -m venv env` on command prompt
* Run `source env/bin/activate` on command prompt
* Run `pip install -r requirements.txt` on command prompt
* Run `export FLASK_CONFIG=development` on command prompt
* Run `export FLASK_APP=run.py` on command prompt
* Run `export export DATABASE_URL= "postgresql://<username>:<password>@localhost/prescribeme"` on command prompt
* Run `flask run` on command prompt
* View the app on `http://127.0.0.1:5000/`

## PSQL Set up
* `Install postgreSQL`
* `Create database prescribeme`
* Run `python manage.py db init`
* Run `python manage.py db migrate`
* Run `python manage.py db upgrade`

* Test endpoints on [POSTMAN](https://www.postman.com/)
