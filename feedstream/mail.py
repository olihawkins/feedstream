# -*- coding: utf-8 -*-

# Imports ---------------------------------------------------------------------

import datetime
import json
import os
import requests
import feedstream.data as data
import feedstream.download as download
from feedstream.config import settings

# Constants -------------------------------------------------------------------

TEMPLATE_PATH_MAIL = os.path.join(settings.template_dir, 'mail.html')
TEMPLATE_PATH_TAG = os.path.join(settings.template_dir, 'tag.html')
TEMPLATE_PATH_ITEM = os.path.join(settings.template_dir, 'item.html')

TEMPLATE_MAIL = open(TEMPLATE_PATH_MAIL).read()
TEMPLATE_TAG = open(TEMPLATE_PATH_TAG).read()
TEMPLATE_ITEM = open(TEMPLATE_PATH_ITEM).read()

# Functions -------------------------------------------------------------------

def get_users():
    return json.loads(open(settings.recipient_file).read())


def get_articles():
    timestamp, entries = download.download_entries_df()
    return entries


def get_articles_by_user(users, articles):

    """
    Create a dictionary containing a dataframe of unique articles for each user
    indexed by their email address.

    """

    users_articles = {}

    for user in users:
        user_articles = articles.loc[articles['tag_id'].isin(user['tag_ids'])]
        unique_articles = user_articles.drop_duplicates(['article_id'])
        users_articles[user['email_address']] = unique_articles

    return users_articles


def get_emails_by_user(users_articles):

    """
    Create a dictionary containing the content of the email for each user
    indexed by their email address.

    """

    users_emails = {}
    for email_address, articles in users_articles.items():
        users_emails[email_address] = create_email_body(articles)
    return users_emails


def create_email_body(articles):

    """
    Create the body of an email which shows all articles by tag based on the
    given dataframe of articles.

    """

    if (len(articles) == 0):
        return None

    # Create containers for the data
    tags = []
    items = []

    # Set current tag values to data in first row
    tag_id = articles.iloc[1]['tag_id']
    tag_label = articles.iloc[1]['tag_label']

    for index, row in articles.iterrows():

        if tag_id != row['tag_id']:
            tags.append(TEMPLATE_TAG.format(
                tag_label=tag_label,
                items=''.join(items)))
            items = []

        items.append(TEMPLATE_ITEM.format(
            url=row['url'],
            title=row['title'],
            short_content=row['short_content']))

        tag_id = row['tag_id']
        tag_label = row['tag_label']

    tags.append(TEMPLATE_TAG.format(
        tag_label=tag_label,
        items=''.join(items)))

    date = datetime.date.today().strftime('%A %d %B %Y')
    mail = TEMPLATE_MAIL.format(
        date=date,
        tags=''.join(tags))

    # with open(os.path.join('_production', 'test.html'), 'w') as test_mail:
    #     test_mail.write(mail)

    return mail


def get_mailshot_data(subject, users_emails):

    """
    Create the json payload for a mailshot given the email subject and the
    email body by recipient address.

    """

    recipients = []
    for email_address, body in users_emails.items():
        recipients.append({'email': email_address, 'body': body})

    mailshot_data = {'subject': subject, 'recipients': recipients}
    return json.dumps(mailshot_data)


def send_mailshot(mailshot_data):

    """Send a mailshot with the given data."""

    url = settings.mailer_endpoint
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=mailshot_data)


def run_mailshot(subject):

    """Downloads article data from feedly and mails it to all users."""

    users = get_users()
    articles = get_articles()
    users_articles = get_articles_by_user(users, articles)
    users_emails = get_emails_by_user(users_articles)
    mailshot_data = get_mailshot_data(subject, users_emails)
    send_mailshot(mailshot_data)
