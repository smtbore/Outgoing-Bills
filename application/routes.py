from application import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from application.models import Users, Transactions, IncomingTransaction, OutgoingTransaction
from datetime import datetime
from application.forms import RegistrationForm, LoginForm, UpdateAccountForm, OutgoingTransactionForm, IncomingTransactionForm
from flask import render_template, redirect, url_for, request


@app.route('/')
@app.route('/home')
def home():
  transactionData=Transactions.query.all()
  return render_template('home.html', title='Home', outgoing=transactionData)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hash_pw = bcrypt.generate_password_hash(form.password.data)

        user = Users(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=hash_pw
        )

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        db.session.commit()
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)


@app.route("/account/delete", methods=["GET", "POST"])
@login_required
def account_delete():
    user = current_user.id
    account = Users.query.filter_by(id=user).first()
    logout_user()
    db.session.delete(account)
    db.session.commit()
    return redirect(url_for('register'))

@app.route("/newtransaction")
@login_required
def new_transaction():
  return render_template('newTransaction.html', title='New Transaction')


@app.route("/newtransaction/outgoing", methods=["GET", "POST"])
@login_required
def outgoing_transaction():
  form = OutgoingTransactionForm()
  if form.validate_on_submit():
    transactionData = Transactions(
        date_posted=datetime.now(),
        TransactionOwner=current_user,
        transaction_type="Outgoing",
        amount=form.outgoing_transaction_amount.data
    )
    outgoingTransactionData = OutgoingTransaction(
        OutgoingCategory=form.outgoing_category.data
    )

    db.session.add(transactionData)
    db.session.add(outgoingTransactionData)
    db.session.commit()
    return redirect(url_for('home'))
  else:
    print(form.errors)

  return render_template('outgoingTransaction.html', title='New Outgoing', form=form)

@app.route("/newtransaction/incoming", methods=["GET", "POST"])
@login_required
def incoming_transaction():
  form = IncomingTransactionForm()
  if form.validate_on_submit():
    transactionData = Transactions(
        date_posted=datetime.now(),
        TransactionOwner=current_user,
        transaction_type="Incoming",
        amount=form.incoming_transaction_amount.data
    )
    db.session.add(transactionData)
    db.session.commit()
    return redirect(url_for('home'))
  else:
    print(form.errors)

  return render_template('incomingTransaction.html', title='New Incoming', form=form)
