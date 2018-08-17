# -*- coding: utf-8 -*-

# Imports ---------------------------------------------------------------------

import datetime
import json
import os
import pandas as pd
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

def get_mail_users():
    return json.loads(open(settings.recipient_file).read())


def get_mail_articles():
    return pd.DataFrame(download.download_entries()['items'])


def get_users_articles(users, articles):

    """
    Create a dictionary containing a dataframe of unique articles for each user
    indexed by their email address.

    """

    users_articles = {}

    for user in users:
        user_articles = articles.loc[articles['tag_id'].isin(user['tag_ids'])]
        unique_articles = user_articles.drop_duplicates(['article_id'])
        users_articles[user['email']] = unique_articles

    return users_articles


def create_mail_body(articles):

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

    with open(os.path.join('_production', 'test.html'), 'w') as test_mail:
        test_mail.write(mail)


def show_entries(entries):
    print(entries[['tag_label','title']].to_string())
