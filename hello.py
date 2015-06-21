import os
import logging

import braintree
import json
import os.path
from models import User, Reward, SeenComment
from inspect import getmembers
from pprint import pprint
from datetime import date, timedelta

from flask import Flask
from flask import render_template
from flask import request
from flask.ext.sqlalchemy import SQLAlchemy

mymerchandid=os.environ.get('MERCHANT_ID')
braintree.Configuration.configure(braintree.Environment.Sandbox,
                                  merchant_id=os.environ.get('BRAINTREE_MERCHANT_ID'),
                                  public_key=os.environ.get('BRAINTREE_PUBLIC_KEY'),
                                  private_key=os.environ.get('BRAINTREE_PRIVATE_KEY'))


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

@app.route("/register/step1", methods=["GET"] )
def register():
  return render_template('register.html')

@app.route("/register/step2", methods=["POST"])
def create_user():
  firstname = request.form["firstname"]
  lastname = request.form["lastname"]
  email = request.form["email"]
  github = request.form["github"]
  # create user
  result = braintree.Customer.create({
   "first_name": firstname,
   "last_name": lastname,
   "email": email
  })
  if result.is_success:
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
      return render_template('payment.html', client_token=client_token, user_id=user.id)
    else:
      return render_template('register.html', errortitle="create merchant error",error=result.errors.deep_errors)
  else:
      return render_template('register.html',  errortitle="create customer", error=result.errors.deep_errors)

@app.route("/register/step3", methods=["POST"])
def add_payment():
  user_id = request.form["user_id"]
  nonce = request.form["payment_method_nonce"]
  user = db.session.query(User).filter_by(id=user_id)
  user.nonce = nonce
  db.session.commit()
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
  reward = db.session.query(Reward).filter_by(github_issue_url=github_issue, sender_github_username=sender_id, recipient_github_username='')
  reward.recipient_github_username = receiver_id
  db.session.commit()
  # void the authorization transaction
  result = braintree.Transaction.void(reward.auth_transaction_id)
  #FIXME make the transaction between the users
  payer = db.session.query(User).filter_by(github_username=sender_id).first()
  payee = db.session.query(User).filter_by(github_username=receiver_id).first()

def set_reward(github_user_id, price, issue_url):
  user = db.session.query(User).filter_by(github_username=github_user_id).first()
  if user is None:
      raise KeyError('user %s unknown' % github_user_id)
  customer = braintree.Customer.find(user.braintree_customer_id)
  payment_method = braintree.PaymentMethod.find(user.braintree_payment_token)
  # create transaction
  result = braintree.Transaction.sale({
    "amount": str(price), # FIXME why a string?
    "payment_method_token": payment_method.token,
    "customer_id": customer.id
  })
  # create reward
  auth_transaction_id = result.transaction.id
  reward = Reward(issue_url, price, github_user_id, '', auth_transaction_id, '')
  db.session.add(reward)
  db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)
