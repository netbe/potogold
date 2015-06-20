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



payment = paypalrestsdk.Payment({
  "intent": "sale",
  "payer": {
    "payment_method": "credit_card",
    "funding_instruments": [{
      "credit_card": {
        "type": "visa",
        "number": "4417119669820331",
        "expire_month": "11",
        "expire_year": "2018",
        "cvv2": "874",
        "first_name": "Joe",
        "last_name": "Shopper" }}]},
  "transactions": [{
    "item_list": {
      "items": [{
        "name": "item",
        "sku": "item",
        "price": "1.00",
        "currency": "USD",
        "quantity": 1 }]},
    "amount": {
      "total": "1.00",
      "currency": "USD" },
    "description": "This is the payment transaction description." }]})

if payment.create():
  print("Payment created successfully")
else:
  print(payment.error)
