from flask import Flask
import os
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)


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
