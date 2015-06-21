import os
from flask import Flask
from flask import render_template
import logging
from flask import request

import braintree
import json
import os.path
from inspect import getmembers
from pprint import pprint
from datetime import date, timedelta

braintree.Configuration.configure(braintree.Environment.Sandbox,
                                  merchant_id=os.environ.get('BRAINTREE_MERCHANT_ID'),
                                  public_key=os.environ.get('BRAINTREE_PUBLIC_KEY'),
                                  private_key=os.environ.get('BRAINTREE_PRIVATE_KEY'))


app = Flask(__name__)


@app.route("/register/step1", methods=["GET"] )
def register():
  return render_template('register.html')

@app.route("/register/step2", methods=["POST"])
def create_user():
  import pdb; pdb.set_trace()
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

  # import pdb; pdb.set_trace()

# @app.route('/')
# def login():

##########################Payment###########################################

def set_reward(github_user_id, price, issue_url):
  # find user from github
  customer = braintree.Customer.find("35653229")
  payment_method = braintree.PaymentMethod.find("kysd7w")
  # create reward
  # create transaction
  result = braintree.Transaction.sale({
    "amount": "10.00",
    "payment_method_token": payment_method.token,
    "customer_id": customer.id
  })

def set_reward_example():
  # find user from github
  customer = braintree.Customer.find("35653229")
  payment_method = braintree.PaymentMethod.find("kysd7w")
  # create reward
  # create transaction
  result = braintree.Transaction.sale({
    "amount": "10.00",
    "payment_method_token": payment_method.token,
    "customer_id": customer.id
  })
  print result
  if result.is_success:
    print "yeah!!"

  else:
    print "nooooo!"

if __name__ == "__main__":
    app.run(debug=True)
    # set_reward_example()
