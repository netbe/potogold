import os
from flask import Flask
from flask import render_template
import logging
import paypalrestsdk
from paypalrestsdk.openid_connect import Tokeninfo, Userinfo

from flask import request

# server
# paypalrestsdk.configure({
#   "mode": os.environ.get('PAYPAL_MODE'), # sandbox or live
#   "client_id": 'AcAdwD6mfFztdmJKaEbZCdGvQGakZPsGQnDKG5g0PpjiPgSRpXo7qGf_oN5gdRVmOAC1G3WGoahony-I',
#   "client_secret": 'EJH0voy76bYLfzc9vcy6r7-2FjdeuAMc-6xeWcXZIA09OiqQ0Ynup8Rd-7BRhfEfcqSsC7u1ENjkTBrq'
#    })

paypalrestsdk.configure({
  "mode": os.environ.get('PAYPAL_MODE'), # sandbox or live
  "client_id": os.environ.get('PAYPAL_CLIENT_ID'),
  "client_secret": os.environ.get('PAYPAL_CLIENT_SECRET')
   })

app = Flask(__name__)

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



# def set_reward():

if __name__ == "__main__":
    app.run(debug=True)
