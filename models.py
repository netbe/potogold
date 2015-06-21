import os
import sys
from sqlalchemy import Column, Integer, String, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(160))
    github_username = Column(String(80))
    github_auth_token = Column(Text())
    github_refresh_token = Column(Text())
    braintree_customer_id = Column(Text())
    braintree_payment_token = Column(Text())
    merchant_account_id = Column(Text())
    nonce = Column(Text())

class Reward(Base):
    __tablename__ = 'rewards'
    id = Column(Integer, primary_key=True)
    github_issue_url = Column(Text())
    amount = Column(Float())
    sender_github_username = Column(String(80))
    recipient_github_username = Column(String(80))
    auth_transaction_id = Column(Text())
    transaction_id = Column(Text())

class SeenComment(Base):
    __tablename__ = 'seen_comments'
    id = Column(Integer, primary_key=True)
    github_comment_url = Column(Text())

engine = create_engine(os.environ['DATABASE_URL'])
Base.metadata.create_all(engine)
