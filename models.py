import os
from peewee import *
import datetime 
from flask_login import UserMixin
from playhouse.db_url import connect

DATABASE = connect(os.environ.get('DATABASE_URL') or 'sqlite:///posts.sqlite')

class User(UserMixin,Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()
    class Meta:
        database = DATABASE
        
class Post(Model):
    text = CharField()
    user = ForeignKeyField(User, backref='posts')
    class Meta:
        database=DATABASE

        
def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Post], safe=True)
    print("Connected to the DB and created tables if they don't already exist")
    DATABASE.close()