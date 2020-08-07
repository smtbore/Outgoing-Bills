from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from os import getenv

app=Flask(__name__)

#Database Setup
app.config['SQLALCHEMY_DATABASE_URI'] = str(os.getenv('DATABASE_URI'))
app.config['SECRET_KEY'] = str(os.getenv('MY_SECRET_KEY'))
db = SQLAlchemy(app)

from application import routes