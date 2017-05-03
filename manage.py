import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, prompt_bool

from api import create_app, db
from api.models import User, Bucketlist, BucketlistItem

app = create_app(os.getenv('BUCKETLIST_ENV') or 'dev')
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@manager.command
def initdb():
    db.create_all()
    user1 = User(username="wcyn", email="cynthia.abura@andela.com",
                 password="1234567")
    user2 = User(username="paul", email="paul@andela.com", password="1234567")
    bucketlist = Bucketlist(description="My Bucketlist", user=user1)
    bucketlist_item = BucketlistItem(description="An item",
                                     bucketlist=bucketlist)
    print("db: ", db)
    # db.session.add(user1)
    # db.session.add(user2)
    # db.session.add(bucketlist)
    # db.session.add(bucketlist_item)
    # db.session.commit()
    print("Initialized the database")


@manager.command
def create_tables():
    db.create_all()
    print("Created model tables")


@manager.command
def dropdb():
    if prompt_bool("Are you sure you want to lose all your data?"):
        db.drop_all()
        print("Dropped the database")

if __name__ == "__main__":
    manager.run()
    db.create_all()
