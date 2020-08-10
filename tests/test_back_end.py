import unittest

from flask import url_for
from flask_testing import TestCase
from flask_login import login_user, current_user, logout_user, login_required
from application import app, db, bcrypt
from application.models import Users, Transactions, OutgoingTransaction
from os import getenv


class TestBase(TestCase):
  def create_app(self):

      # pass in configurations for test database
    config_name = 'testing'
    app.config.update(TEST_DATABASE_URI=getenv('mysql+pymysql://root:root@35.246.55.172/testdb'),
                      TEST_SECRET_KEY=getenv('smtb98'),
                      WTF_CSRF_ENABLED=False,
                      DEBUG=True
                      )
    return app

  def setUp(self):
    db.session.commit()
    db.drop_all()
    db.create_all()

    hashed_test_pw = bcrypt.generate_password_hash('Testing123Testing')
    userData = Users(
        first_name="Forename",
        last_name="Surname",
        email="test@testemail.co.uk",
        password=hashed_test_pw
    )
    db.session.add(userData)
    db.session.commit()

  def tearDown(self):
    db.session.remove()
    db.drop_all()


class TestViews(TestBase):
  def test_homepage_view(self):
    response = self.client.get(url_for('home'))
    self.assertEqual(response.status_code, 200)

  def test_register_view(self):
    response = self.client.get(url_for('register'))
    self.assertEqual(response.status_code, 200)

  def test_login_view(self):
    response = self.client.get(url_for('login'))
    self.assertEqual(response.status_code, 200)

  def test_add_outgoing_transaction(self):
    with self.client:
      self.client.post(
          url_for('login'),
          data=dict(
              email='test@testemail.co.uk',
              password='Testing123Testing'
          ),
          follow_redirects=True
      )
      response = self.client.get(url_for('outgoing_transaction'))
      self.assertEqual(response.status_code, 200)

  def test_add_incoming_transaction(self):
    with self.client:
      self.client.post(
          url_for('login'),
          data=dict(
              email='test@testemail.co.uk',
              password='Testing123Testing'
          ),
          follow_redirects=True
      )
      response = self.client.get(url_for('incoming_transaction'))
      self.assertEqual(response.status_code, 200)

  def test_account(self):
    with self.client:
      self.client.post(
          url_for('login'),
          data=dict(
              email='test@testemail.co.uk',
              password='Testing123Testing'
          ),
          follow_redirects=True
      )
      response = self.client.get(url_for('account'))
      self.assertEqual(response.status_code, 200)

  def test_new_transaction(self):
    with self.client:
      self.client.post(
          url_for('login'),
          data=dict(
              email='test@testemail.co.uk',
              password='Testing123Testing'
          ),
          follow_redirects=True
      )
      response = self.client.get(url_for('new_transaction'))
      self.assertEqual(response.status_code, 200)


class TestFunctionality(TestBase):
  def test_register_new_user(self):
    with self.client:
      response = self.client.post(
          '/register',
          data=dict(
              email="test2@test.com",
              password="Test2",
              first_name="John",
              last_name="Doe",
              confirm_password="Test2"
          ),
          follow_redirects=True
      )
      self.assertEqual(response.status_code, 200)

  def test_login_user(self):
    with self.client:
      self.client.post(
          '/login',
          data=dict(
              email="test@testemail.co.uk",
              password="Testing123Testing"
          ),
          follow_redirects=True
      )
      self.assertEqual(current_user.email, "test@testemail.co.uk")

  def test_logout_user(self):
    with self.client:
      self.client.get(
          '/logout',
          follow_redirects=True
      )
      self.assertFalse(current_user.is_authenticated)

  def test_new_incoming_transaction(self):
    self.client.post(url_for('login'), data=dict(email="test@testemail.co.uk", password="Testing123Testing"), follow_redirects=True)
    self.client.post(url_for('incoming_transaction'), data=dict(incoming_transaction_amount="100"), follow_redirects=True)
    response = self.client.get(url_for('home'))
    self.assertIn(b'100', response.data)

  def test_deleteuser(self):
    self.client.post(url_for('login'), data=dict(
        email="test@testemail.co.uk", password="Testing123Testing"), follow_redirects=True)
    response = self.client.post(
        url_for('account_delete'), follow_redirects=True)
    self.assertIn(b'Login', response.data)

  def test_add_new_outgoing_transaction(self):
    with self.client:
      self.client.post(
          '/login',
          data=dict(
              email="test@testemail.co.uk",
              password="Testing123Testing"
          ),
          follow_redirects=True
      )
      with self.client:
        self.client.post(
          '/newtransaction/outgoing',
          data=dict(
              outgoing_category="Bills",
              outgoing_transaction_amount="200"
          ),
          follow_redirects=True
      )
      response = self.client.get(url_for('home'))
      self.assertIn(b'Bills', response.data)
