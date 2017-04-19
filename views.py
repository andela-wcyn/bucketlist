import sqlalchemy
from flask import render_template
from flask import request
from flask import jsonify
from datetime import datetime

from config import app, db
import models

bucketlist_items = []


def store_item(url, description):
    bucketlist_items.append(dict(
        url=url,
        description=description,
        user="Cynthia",
        data=datetime.utcnow()
    ))


@app.route('/')
@app.route('/index')
def index():
    data = {
        "text": "hello there",
        "color": "blue"
    }
    return jsonify(data)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


@app.route('/add')
def add():
    user = models.User(username="wcyn", email="wasonga.cynthia@gmail.com")
    bm = models.Bookmark(url="https://learnmine.com", date=datetime.utcnow(),
                         description="Some description", user_id=1)
    try:
        db.session.add(bm)
        db.session.add(user)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as error:
        print("Error committing to db: ", error)
    return None
    # return render_template('add.html')


@app.route('/furniture/<int:id>', methods=['POST', 'GET'])
def furniture(id):
    if request.method == 'GET':
        # return a list of furniture
        return []
    elif request.method == 'POST':
        # return a list of furniture
        return "Created", 201

    # return render_template('add.html')


def new_item(num):
    return sorted(bucketlist_items, key=lambda bl: bl['date'], reverse=True)[
           :num]
