import requests
import time
import json
import re
from requests.auth import HTTPBasicAuth
#FIXME need to add the checking for closed issues, to trigger the sending of the email
POLL_DELAY = 1
BASE = 'https://api.github.com'
#FIXME make env var
username = 'potogold'
password = 'JrX4vav7?yoh'

ADD_CRIB = r'^\@%s add \$([0-9]+(|.[0-9]{0,2}))\.{0,1}$' % username
REWARD_CRIB = r'^\@%s reward \@((\w|-)*)\.{0,1}$' % username

session = requests.Session()
session.auth = HTTPBasicAuth(username, password)

"""
implementation note: there doesn't seem to be a link to the comment in the notification, so we have to iterate over all the comments in an issue, skipping over the comments that we've already processed.
"""
#seen_comments = set() # FIXME should be in DB
seen_comments = set([u'https://api.github.com/repos/netbe/potogold/issues/comments/113826443', u'https://api.github.com/repos/netbe/potogold/issues/comments/113805378', u'https://api.github.com/repos/netbe/potogold/issues/comments/113799706', u'https://api.github.com/repos/netbe/potogold/issues/comments/113834735', u'https://api.github.com/repos/netbe/potogold/issues/comments/113825783'])

def mentions():
    """
    Return a generator over the notifications which are mentions.
    """
    for notification in session.get(BASE + '/notifications').json():
        if notification['reason'] == u'mention':
            #print json.dumps(notification, indent=2)
            yield notification

def is_unseen(comment_url):
    return comment_url not in seen_comments

def mark_seen(comment_url):
    seen_comments.add(comment_url)

def instructions():
    for mention in mentions():
        issue_url = mention[u'subject'][u'url']
        for comment in session.get(issue_url + u'/comments').json():
            if comment[u'body'].startswith('@%s' % username) and is_unseen(comment[u'url']):
                session.patch(mention['url']) # mark notification read
                mark_seen(comment[u'url'])
                author = comment[u'user'][u'login']
                yield (author, issue_url, comment['body'].strip())
 
def set_bounty(author, issue_url, amount):
    comment(issue_url, '@%s offers $%.2f' % (author, amount))

def release_bounty(author, issue_url, recipient):
    comment(issue_url, '@%s released funds to @%s' % (author, recipient))

def comment(issue_url, text):
    url = issue_url + u'/comments'
    post_body = json.dumps({'body': text})
    request = session.post(url, data=post_body)
    if request.status_code != 201:
        raise Exception('URL %s status code %i' % (url, request.status_code))
        
def perform(author, issue_url, command):
    if re.match(REWARD_CRIB, command):
        recipient = re.match(REWARD_CRIB, command).groups()[0]
        release_bounty(author, issue_url, recipient)
    elif re.match(ADD_CRIB, command):
        amount = round(float(re.match(ADD_CRIB, command).groups()[0]), 2)
        set_bounty(author, issue_url, amount)
    else:
        comment(issue_url, "@%s I don't understand" % author)

while True:
    for bits in instructions():
        print bits
        perform(*bits)
    time.sleep(POLL_DELAY)
