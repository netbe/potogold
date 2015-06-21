from sqlalchemy import Model, Column, Integer, String, Text, Float

class User(Model):
    id = Column(Integer, primary_key=True)
    email = Column(String(160))
    github_username = Column(String(80))
    github_auth_token = Column(Text())
    github_refresh_token = Column(Text())
    braintree_customer_id = Column(Text())
    braintree_payment_token = Column(Text())
    merchant_account_id = Column(Text())
    nonce = Column(Text())

    def __init__(self, email, github_username, github_auth_token, github_refresh_token, braintree_customer_id, braintree_payment_token, nonce, merchant_account_id):
        self.email = email
        self.github_username = github_username
        self.github_auth_token = github_auth_token
        self.github_refresh_token = github_refresh_token
        self.braintree_customer_id = braintree_customer_id
        self.braintree_payment_token = braintree_payment_token
        self.nonce = nonce
        self.merchant_account_id = merchant_account_id

    def __repr__(self):
        return '<git username %r>' % self.github_username


class Reward(Model):
    id = Column(Integer, primary_key=True)
    github_issue_url = Column(Text())
    amount = Column(Float())
    sender_github_username = Column(String(80))
    recipient_github_username = Column(String(80))
    auth_transaction_id = Column(Text())
    transaction_id = Column(Text())

    def __init__(self, github_issue_url, amount, sender_github_username, recipient_github_username, auth_transaction_id, transaction_id):
        self.github_issue_url = github_issue_url
        self.amount = amount
        self.sender_github_username = sender_github_username
        self.recipient_github_username = recipient_github_username
        self.auth_transaction_id = auth_transaction_id
        self.transaction_id = transaction_id

    def __repr__(self):
        return '<sender %r, recipient %r, amount %f>' % (self.sender_github_username, self.recipient_github_username, self.amount)


class SeenComment(Model):
    id = Column(Integer, primary_key=True)
    github_comment_url = Column(Text())

    def __init__(self, github_comment_url):
        self.github_comment_url = github_comment_url

    def __repr__(self):
        return '<comment %r>' % self.github_comment_url

