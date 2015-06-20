# paypal stuff
import paypalrestsdk
import logging
import os

paypalrestsdk.configure({
  "mode": os.environ.get('PAYPAL_MODE'), # sandbox or live
  "client_id": os.environ.get('PAYPAL_CLIENT_ID'),
  "client_secret": os.environ.get('PAYPAL_CLIENT_SECRET') })

logging.basicConfig(level=logging.INFO)

# Include Headers and Content by setting logging level to DEBUG, particularly for
# Paypal-Debug-Id if requesting PayPal Merchant Technical Services for support



# payment = paypalrestsdk.Payment({
#     "intent": "sale",
#     "payer": {
#         "payment_method": "paypal"
#     },
#     "transactions": [
#         {
#             "amount": {
#                 "currency": "USD",
#                 "total": "110.54"
#             },
#             "description": "This is the payment transaction description."
#         }
#     ],
#     "redirect_urls": {
#         "return_url": "http://www.ebay.com",
#         "cancel_url": "http://www.milo.com"
#     }
# })

# if payment.create():
#   print("Payment[%s] created successfully" % (payment.id))
#   # PayerID is required to approve the payment.
#   if payment.execute({"payer_id": "DUFRQ8GWYMJXC"}):  # return True or False
#     print("Payment[%s] execute successfully" % (payment.id))
#   else:
#     print(payment.error)

# else:
#   print(payment.error)

from paypalrestsdk.openid_connect import Tokeninfo, Userinfo


# Generate login url
login_url = Tokeninfo.authorize_url({ "scope": "openid profile"})

# Create tokeninfo with Authorize code
tokeninfo = Tokeninfo.create("Replace with Authorize code")

# Refresh tokeninfo
tokeninfo = tokeninfo.refresh()

# Create tokeninfo with refresh_token
tokeninfo = Tokeninfo.create_with_refresh_token("Replace with refresh_token")

# Get userinfo
userinfo  = tokeninfo.userinfo()

# Get userinfo with access_token
userinfo  = Userinfo.get("Replace with access_token")

# Generate logout url
logout_url = tokeninfo.logout_url()
