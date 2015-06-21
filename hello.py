import os
import logging

import braintree
import json
import os.path
from inspect import getmembers
from pprint import pprint
from datetime import date, timedelta

from flask import Flask
from flask import render_template
from flask import request
from flask.ext.sqlalchemy import SQLAlchemy


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
  # create submerchant
  result = braintree.MerchantAccount.create({
    'individual': {
        'first_name': "Jane",
        'last_name': "Doe",
        'email': "jane@14ladders.com",
    },
    'funding': {
        'email': "funding@blueladders.com",
    },
    "tos_accepted": True,
    "master_merchant_account_id": mymerchandid
})
  #  result.merchant_account.id stores to user and use for rewarding
  if result.is_success:
    return render_template('payment.html')
  else:
    return render_template('register.html')


@app.route("/register/step3", methods=["POST"])
def add_payment():
  user_id = request.form["user_id"]
  nonce = request.form["payment_method_nonce"]
  print user_id
  print nonce
  # add nonce to db
  return "todo"

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
def hello():
  base_url = request.url_root
  print base_url
  return_url = request.url_root + "paypal_authenticated"
  return render_template('login.html', client_id=os.environ.get('PAYPAL_CLIENT_ID'), return_url=return_url, mode=os.environ.get('PAYPAL_MODE'))

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
    #recipient_github_username
  reward = Reward.query.filter_by(github_issue_url=github_issue, sender_github_username=sender_id)
  # find reward and then the customer attached
  # reward.transaction_id
  result = braintree.Transaction.void(transa)

def set_reward(github_user_id, price, issue_url):
  user = User.query.filter_by(github_username=github_user_id).first()
  if user is None:
      raise KeyError('user %s unknown' % github_user_id)
  customer = braintree.Customer.find(user.braintree_customer_id)
  payment_method = braintree.PaymentMethod.find(user.braintree_payment_token)
  # create reward
  reward = Reward(issue_url, price, github_user_id, '')
  db.session.add(reward)
  db.session.commit()
  # create transaction
  result = braintree.Transaction.sale({
    "amount": "10.00",
    "payment_method_token": payment_method.token,
    "customer_id": customer.id
  })


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(160))
    github_username = db.Column(db.String(80))
    github_auth_token = db.Column(db.Text())
    github_refresh_token = db.Column(db.Text())
    braintree_customer_id = db.Column(db.Text())
    braintree_payment_token = db.Column(db.Text())

    def __init__(self, email, github_username, github_auth_token, github_refresh_token, braintree_customer_id, braintree_payment_token):
        self.email = email
        self.github_username = github_username
        self.github_auth_token = github_auth_token
        self.github_refresh_token = github_refresh_token
        self.braintree_customer_id = braintree_customer_id
        self.braintree_payment_token = braintree_payment_token

    def __repr__(self):
        return '<git username %r>' % self.github_username


class Reward(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    github_issue_url = db.Column(db.Text())
    amount = db.Column(db.Float())
    sender_github_username = db.Column(db.String(80))
    recipient_github_username = db.Column(db.String(80))

    def __init__(self, github_issue_url, amount, sender_github_username, recipient_github_username):
        self.github_issue_url = github_issue_url
        self.amount = amount
        self.sender_github_username = sender_github_username
        self.recipient_github_username = recipient_github_username

    def __repr__(self):
        return '<sender %r, recipient %r, amount %f>' % (self.sender_github_username, self.recipient_github_username, self.amount)


if __name__ == "__main__":
    app.run(debug=True)
    # set_reward_example()
