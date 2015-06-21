import requests
import time
import json
import re
from requests.auth import HTTPBasicAuth
import hello

#FIXME need to add the checking for closed issues, to trigger the sending of the email
POLL_DELAY = 1.5
BASE = 'https://api.github.com'
#FIXME make env var
USERNAME = 'potogold'
PASSWORD = 'JrX4vav7?yoh'

ADD_CRIB = r'^\@%s add \$([0-9]+(|.[0-9]{0,2}))\.{0,1}$' % USERNAME
REWARD_CRIB = r'^\@%s reward \@((\w|-)*)\.{0,1}$' % USERNAME

session = requests.Session()
session.auth = HTTPBasicAuth(USERNAME, PASSWORD)

def mentions():
    """
    Return a generator over the notifications which are mentions.
    """
    for notification in session.get(BASE + '/notifications').json():
        if notification['reason'] == u'mention':
            #print json.dumps(notification, indent=2)
            yield notification

def instructions():
    seen_ids = hello.get_seen_comment_urls()
    for mention in mentions():
        issue_url = mention[u'subject'][u'url']
        for comment in session.get(issue_url + u'/comments').json():
            if comment[u'body'].startswith('@%s' % USERNAME) and comment[u'url'] not in seen_ids:
                session.patch(mention['url']) # mark notification read on GitHub
                hello.mark_comment_url_seen(comment[u'url']) # mark the comment read in the database
                author = comment[u'user'][u'login']
                yield (author, issue_url, comment['body'].strip())

def set_bounty(author, issue_url, amount):
    comment(issue_url, '@%s offers $%.2f' % (author, amount))
    hello.set_reward(author, amount, issue_url)

def release_bounty(author, issue_url, recipient):
    comment(issue_url, '@%s released funds to @%s' % (author, recipient))
    hello.pay(author, recipient, issue_url)

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

def refresh():
    for bits in instructions():
        print bits
        perform(*bits)
    for issue_url, bounty_setter in hello.get_bounties():
        issue = session.get(issue_url).json()
        if issue['state'] == u'closed':
            print '%s is CLOSED, so notify %s' % (issue_url, bounty_setter)

if __name__ == "__main__":
    while True:
        refresh()
        time.sleep(POLL_DELAY)
