from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)


class User(db.Model):
    """ Users """
    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                           nullable=False,
                           unique=True)
    last_name = db.Column(db.String(50),
                          nullable=False,
                          unique=True)
    image_url = db.Column(db.Text,
                          nullable=True,
                          unique=False,
                          default="https://genslerzudansdentistry.com/wp-content/uploads/2015/11/anonymous-user.png")
    
    posts = db.relationship('Post')



class Post(db.Model):
    """ Posts """
    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(50),
                      nullable=False,
                      unique=True)
    content = db.Column(db.Text,
                        nullable=False,
                        unique=True)
    created_at = db.Column(db.DateTime,
                           default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User')
