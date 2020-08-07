from application import db
from application.models import Users, Transactions, IncomingTransaction, OutgoingTransaction

db.drop_all()
db.create_all()
