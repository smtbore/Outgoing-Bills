from application import db, login_manager
from flask_login import UserMixin
from datetime import datetime


class Users(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String(30), nullable=False)
  last_name = db.Column(db.String(30), nullable=False)
  email = db.Column(db.String(150), nullable=False, unique=True)
  password = db.Column(db.String(500), nullable=False)
  transactions = db.relationship(
      'Transactions', backref='TransactionOwner', lazy=True)


class Transactions(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   date_posted = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
   user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
   transaction_type = db.Column(db.String(10), nullable=False)
   amount = db.Column(db.Integer, nullable=False)


class OutgoingTransaction(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  OutgoingCategory = db.Column(db.String(13), nullable=True)

@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))
