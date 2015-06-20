import os
from flask import Flask
from flask import render_template
import logging
import paypalrestsdk

paypalrestsdk.configure({
  "mode": os.environ.get('PAYPAL_MODE'), # sandbox or live
  "client_id": 'AcAdwD6mfFztdmJKaEbZCdGvQGakZPsGQnDKG5g0PpjiPgSRpXo7qGf_oN5gdRVmOAC1G3WGoahony-I',
  "client_secret": 'EJH0voy76bYLfzc9vcy6r7-2FjdeuAMc-6xeWcXZIA09OiqQ0Ynup8Rd-7BRhfEfcqSsC7u1ENjkTBrq'
   })

# paypalrestsdk.configure({
#   "mode": os.environ.get('PAYPAL_MODE'), # sandbox or live
#   "client_id": 'AcAdwD6mfFztdmJKaEbZCdGvQGakZPsGQnDKG5g0PpjiPgSRpXo7qGf_oN5gdRVmOAC1G3WGoahony-I' #os.environ.get('PAYPAL_CLIENT_ID'),
#   "client_secret": 'EJH0voy76bYLfzc9vcy6r7-2FjdeuAMc-6xeWcXZIA09OiqQ0Ynup8Rd-7BRhfEfcqSsC7u1ENjkTBrq' #os.environ.get('PAYPAL_CLIENT_SECRET')
#    })

app = Flask(__name__)

@app.route('/')
def hello():
  return_url="https://potogold.herokuapp.com/paypal_authenticated"
  # return_url = "http://127.0.0.1:5000/paypal_authenticated"
  return render_template('login.html', client_id='AcAdwD6mfFztdmJKaEbZCdGvQGakZPsGQnDKG5g0PpjiPgSRpXo7qGf_oN5gdRVmOAC1G3WGoahony-I', return_url=return_url, mode=os.environ.get('PAYPAL_MODE'))

def paypal_authenticated():
  return "yeah!"




# @app.route('/')
# def login():



# def set_reward():

if __name__ == "__main__":
    app.run(debug=True)
