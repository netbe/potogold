import os
import logging

import mailer
import sms

import braintree
import json
import os.path
from models import User, Reward, SeenComment, Base
from inspect import getmembers
from pprint import pprint
from datetime import date, timedelta
import github
from flask import Flask
from flask import render_template
from flask import request
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(os.environ['DATABASE_URL'])
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

mymerchandid=os.environ.get('MERCHANT_ID')
braintree.Configuration.configure(braintree.Environment.Sandbox,
                                  merchant_id=os.environ.get('BRAINTREE_MERCHANT_ID'),
                                  public_key=os.environ.get('BRAINTREE_PUBLIC_KEY'),
                                  private_key=os.environ.get('BRAINTREE_PRIVATE_KEY'))


app = Flask(__name__)

@app.route("/refresh", methods=["GET"] )
def runBot():
  github.refresh()
  return 'OK'


@app.route("/register/step1", methods=["GET"] )
def register():
  return render_template('register.html')

@app.route("/register/step2", methods=["POST"])
def create_user():
  firstname = request.form["firstname"]
  lastname = request.form["lastname"]
  email = request.form["email"]
  github = request.form["github"]
  result = braintree.Customer.create({
    "first_name": firstname,
    "last_name": lastname,
    "email": email
  })
  if result.is_success:
    customer_id = result.customer.id
    # create submerchant
    result = braintree.MerchantAccount.create({
      'individual': {
          'first_name': firstname,
          'last_name': lastname,
          'email': email,
          'date_of_birth': '07/11/1984',
          'address': {
            'street_address': "111 Main St",
            'locality': "Chicago",
            'region': "IL",
            'postal_code': "60622"
        }
      },
      'funding': {
          'email': email,
          'destination': 'email'
      },
      "tos_accepted": True,
      "master_merchant_account_id": mymerchandid
    })
    #  result.merchant_account.id stores to user and use for rewarding
    if result.is_success:
      client_token = braintree.ClientToken.generate({})
      user = User(email=email,
                  github_username=github,
                  github_auth_token='',
                  github_refresh_token='',
                  braintree_customer_id=customer_id,
                  braintree_payment_token='', #FIXME needed?
                  merchant_account_id=result.merchant_account.id,
                  nonce='')
      session.add(user)
      session.commit()

      if user:
        return render_template('payment.html', client_token=client_token, user_id=user.github_username)

    return render_template('register.html', errortitle="create merchant error",error=result.errors.deep_errors)
  else:
      return render_template('register.html',  errortitle="create customer", error=result.errors.deep_errors)

@app.route("/register/step3", methods=["POST"])
def add_payment():
  github_username = request.args.get("user_id")
  nonce = request.form["payment_method_nonce"]
  user = session.query(User).filter_by(github_username=github_username).first()
  if user is None:
      raise KeyError('user %s not known' % github_username)
  user.nonce = nonce
  session.commit()
  return render_template('success.html')

@app.route("/client_token", methods=["GET"])
def client_token():
  result = braintree.Customer.create({
    "id": "customer_143",
    "first_name": "Katrina"
  })
  if result.is_success:
    token = braintree.ClientToken.generate({
      "customer_id": result.customer.id
    })
    return render_template('register.html', client_token=token)
  else:
    return "no"


@app.route('/')
def index():
  return render_template('index.html')

@app.route('/home')
def home():
  return render_template('home.html')

@app.route('/paypal_authenticated')
def paypal_authenticated():
  print request
  code = request.args.get('code')
  tokeninfo = Tokeninfo.create(code)
  # save tokeninfo to user db
  print tokeninfo
  if tokeninfo:
    userinfo  = tokeninfo.userinfo()
    print userinfo
    return "yeah!"
  else:
    return "could not login"


##########################Payment###########################################
def pay(sender_id, receiver_id, github_issue):
  reward = session.query(Reward).filter_by(github_issue_url=github_issue, sender_github_username=sender_id, recipient_github_username='')
  reward.recipient_github_username = receiver_id
  session.add(reward)
  session.commit()
  # void the authorization transaction
  result = braintree.Transaction.void(reward.auth_transaction_id)
  # make the transaction between the users
  payer = session.query(User).filter_by(github_username=sender_id).first()
  payee = session.query(User).filter_by(github_username=receiver_id).first()
  result = braintree.Transaction.sale({
    "amount": str(reward.amount), # FIXME why a string?
    'options': {'submit_for_settlement': True},
    "payment_method_token": payer.braintree_payment_token,
    "merchant_account_id": payee.merchant_account_id,
    "customer_id": payer.braintree_customer_id
  })

def set_reward(github_user_id, price, issue_url):
  user = session.query(User).filter_by(github_username=github_user_id).first()
  if user is None:
      raise KeyError('user %s unknown' % github_user_id)
  customer = braintree.Customer.find(user.braintree_customer_id)
  payment_method = braintree.PaymentMethod.find(user.nonce)
  # create transaction
  result = braintree.Transaction.sale({
    "amount": str(price), # FIXME why a string?
    "payment_method_token": payment_method.token,
    "customer_id": customer.id
  })
  # create reward
  auth_transaction_id = result.transaction.id
  reward = Reward(github_issue_url=issue_url,
                  amount=price,
                  sender_github_username=github_user_id,
                  recipient_github_username='',
                  auth_transaction_id=auth_transaction_id,
                  transaction_id='')
  session.add(reward)
  session.commit()

def get_seen_comment_urls():
    comments = session.query(SeenComment).all()
    return set([comment.github_comment_url for comment in comments])

def mark_comment_url_seen(url):
    comment = SeenComment(github_comment_url=url)
    session.add(comment)
    session.commit()

if __name__ == "__main__":
    app.run(debug=True)
