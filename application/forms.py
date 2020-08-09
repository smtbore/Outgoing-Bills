from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField, DecimalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from application.models import Users
from flask_login import current_user


class RegistrationForm(FlaskForm):
  email = StringField('Email',
                      validators=[
                          DataRequired(),
                          Email()
                      ]
                      )
  password = PasswordField('Password',
                           validators=[
                               DataRequired(),
                           ]
                           )
  first_name = StringField('First Name',
                           validators=[
                               DataRequired(),
                               Length(min=2, max=30)
                           ]
                           )
  last_name = StringField('Last Name',
                          validators=[
                              DataRequired(),
                              Length(min=2, max=100)
                          ]
                          )
  confirm_password = PasswordField('Confirm Password',
                                   validators=[
                                       DataRequired(),
                                       EqualTo('password')
                                   ]
                                   )
  submit = SubmitField('Sign Up')

  def validate_email(self, email):
    user = Users.query.filter_by(email=email.data).first()

    if user:
      raise ValidationError('Email already in use')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[
                            DataRequired(),
                            Email()
                        ]
                        )

    password = PasswordField('Password',
                             validators=[
                                 DataRequired()
                             ]
                             )

    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    first_name = StringField('First Name',
                             validators=[
                                 DataRequired(),
                                 Length(min=4, max=30)
                             ])
    last_name = StringField('Last Name',
                            validators=[
                                DataRequired(),
                                Length(min=4, max=30)
                            ])
    email = StringField('Email',
                        validators=[
                            DataRequired(),
                            Email()
                        ])
    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = Users.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already in use')


class OutgoingTransactionForm(FlaskForm):
  outgoing_category = SelectField(
      u'Category', 
      choices=[('Bills'), ('Entertainment'), ('Family'), ('General')],
      validators=[
          DataRequired()
      ])
  outgoing_transaction_amount = DecimalField('Amount',
    places=2, 
    validators=[
        DataRequired()
      ])
  submit = SubmitField('Create transaction')  

class IncomingTransactionForm(FlaskForm):
  incoming_transaction_amount = DecimalField('Amount',
    places=2,
    validators=[
      DataRequired()
    ])
  submit = SubmitField('Create transaction')  
