[![Build Status](https://travis-ci.org/andela-wcyn/bucketlist.svg?branch=develop)](https://travis-ci.org/andela-wcyn/bucketlist)
# Bucketlist API Backend

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
## API Endpoints
| Endpoint  | Functioanlity  |
|---|---|
| POST /auth/login  |  Log a user in |
| POST /auth/register | Register a user  |
| POST /bucketlists/  | Create a new bucketlist |
| GET /bucketlists/ |  List all the created bucket lists |
| GET /bucketlists/\<id> | Get single bucket list |
| PUT /bucketlists/\<id> | Update this bucket list |
| DELETE /bucketlists/\<id> | Delete this single bucket list |
| POST /bucketlists/\<id>/items/ | Create a new item in bucket list |
| PUT /bucketlists/\<id>/items/<item_id> | Update a bucket list item |
| DELETE /bucketlists/\<id>/items/<item_id> | Delete an item in a bucket list |

### Bucketlist JSON Format
```
"bucketlist": {
      "_links": {
        "collection": "/api/v1/bucketlists/",
        "self": "/api/v1/bucketlists/<id>"
      },
      "description": "Food Festival",
      "id": <id>,
      "item_count": 0,
      "items": [],
      "user": {
        "username": "molly"
      }
    }
```

### Bucketlist Item JSON Format
```
{
  "_links": {
    "collection": "/api/v1/bucketlists/<id>",
    "self": "/api/v1/bucketlists/<id>/<item_id>"
  },
  "bucketlist_id": <id>,
  "description": "Bucketlist item",
  "done": false,
  "id": <item_id>
}
```
