from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/iws.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
engine = create_engine('sqlite://', echo=False)
Base = declarative_base()

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    firstname = db.Column(db.String(120), unique=True, nullable=False)
    surname = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

class Clients(db.Model):
    id = db.Column(db.Integer,primary_key=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    def __repr__(self):
        return '<Clients %r>' % self.name

class Features(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.Float, nullable=False, default=time.time())
    date_expected = db.Column(db.String, nullable=False)
    product_area = db.Column(db.String, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'),nullable=False)
    client = db.relationship('Clients',backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return '<Features %r>' % self.title
