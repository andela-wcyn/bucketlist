import sqlalchemy
from flask import request
from flask import jsonify
from datetime import datetime

from bucketlist import app, db
from bucketlist.models import User, Bookmark

bucketlist_items = []


def store_item(url, description):
    bucketlist_items.append(dict(
        url=url,
        description=description,
        user="Cynthia",
        data=datetime.utcnow()
    ))


# Fake login
def logged_in_user():
    return User.query.filter_by(username='wcyn').first()


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
    data = {
        "error": "404",
        "message": "Page Not Found"
    }
    return jsonify(data), 404


@app.errorhandler(500)
def page_not_found(e):
    data = {
        "error": "500",
        "message": "Internal Server Error"
    }
    return jsonify(data), 500


@app.route('/add')
def add():
    user = User(username="wcyn", email="wasonga.cynthia@gmail.com")
    bm = Bookmark(user=logged_in_user(), url="https://learnmine.com",
                         date=datetime.utcnow(),
                         description="Some description")
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
