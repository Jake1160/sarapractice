# This is where all the database collections are defined. A collection is a place to hold a defined 
# set of data like Users, Blogs, Comments. Collections are defined below as classes. Each class name is 
# the name of the data collection and each item is a data 'field' that stores a piece of data.  Data 
# fields have types like IntField, StringField etc.  This uses the Mongoengine Python Library. When 
# you interact with the data you are creating an onject that is an instance of the class.

from sys import getprofile
from tokenize import String
from typing import KeysView
from xmlrpc.client import Boolean

from setuptools import SetuptoolsDeprecationWarning
from app import app
from flask import flash
from flask_login import UserMixin
from mongoengine import FileField, EmailField, StringField, IntField, ReferenceField, DateTimeField, BooleanField, FloatField, CASCADE
from flask_mongoengine import Document
import datetime as dt
import jwt
from time import time
from bson.objectid import ObjectId

class User(UserMixin, Document):
    createdate = DateTimeField(defaultdefault=dt.datetime.utcnow)
    gid = StringField(sparse=True, unique=True)
    gname = StringField()
    gprofile_pic = StringField()
    username = StringField()
    fname = StringField()
    lname = StringField()
    email = EmailField()
    image = FileField()
    prononuns = StringField()
    adult_fname = StringField()
    adult_lname = StringField()
    adult_email = StringField()
    consent = BooleanField(default=False)

    meta = {
        'ordering': ['lname','fname']
    }


class Workout(Document):
    excercise = StringField()
    weight = StringField()
    sets= StringField()
    reps = StringField()

    meta = {
        'ordering': ['-createdate']
    }
