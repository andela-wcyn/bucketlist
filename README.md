# bucketlist

A Flask API Application Backend to manage bucketlists

## How to run this application

In order to run the bucketlist API backend, change directory into the project folder.
First of all, install all the requirements by running:
```
pip install -r requirements.txt
```

Run the flask application by typing:
```
python manage.py runserver
```
This will start the server at `http://127.0.0.1:5000/`

## How to test this application
In order to test this application locally, ensure to first install the developer requirements by running:
First of all, install all the requirements by running:
```
pip install -r requirements_devel.txt
```
Run the following `nosetest` command to run the tests with coverage:
```
nosetests --rednose --with-coverage
```
