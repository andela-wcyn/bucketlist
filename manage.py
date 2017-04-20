from bucketlist import app, db
from flask_script import Manager, prompt_bool

from bucketlist.models import User

manager = Manager(app)


@manager.command
def initdb():
    db.create_all()
    db.session.add(User(username="wcyn", email="cynthia.abura@andela.com"))
    db.session.add(User(username="paul", email="paul@andela.com"))
    db.session.commit()
    print("Initialized the database")


@manager.command
def dropdb():
    if prompt_bool("Are you sure you want to lose all your data"):
        db.drop_all()
        print("Dropped the database")

if __name__ == "__main__":
    manager.run()
    db.create_all()
