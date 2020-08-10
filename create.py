from application import db
from application.models import Users, Transactions, OutgoingTransaction 
db.drop_all()
db.create_all()

