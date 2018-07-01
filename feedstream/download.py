# -*- coding: utf-8 -*-

# Imports ---------------------------------------------------------------------

import csv
import datetime
import os
import feedstream.fetch as fetch
import feedstream.data as data
import feedstream.settings as settings

# Constants -------------------------------------------------------------------

TIMESTAMP_FILE = os.path.join(settings.data_dir, settings.timestamp_file)
# 1530313200000

# Functions -------------------------------------------------------------------

def download_entries():

    """Download entries from each tag to a csv."""

    fieldnames = [
        'board',
        'pub_date',
        'add_date',
        'add_time',
        'publisher',
        'url',
        'title',
        'author',
        'summary',
        'keywords',
        'article_id']

    entries = []
    since = get_last_downloaded() if settings.download_new else None
    downloaded = data.get_timestamp_from_datetime(datetime.datetime.now())
    tag_ids = fetch.fetch_tag_ids()

    for tag_id in tag_ids:

        continuation = None
        while True:

            contents = fetch.fetch_tag_contents(tag_id['id'],
                since=since, continuation=continuation, count=10000)

            for item in contents['items']:

                entry = {}
                entry['board'] = tag_id['label']
                entry['article_id'] = item['id']
                entry['url'] = data.get_entry_url(item)
                entry['title'] = data.get_opt_key(item, 'title')
                entry['author'] = data.get_opt_key(item, 'author')
                entry['publisher'] = data.get_opt_key(item, 'origin', 'title')

                pub_date = data.get_opt_key(item, 'published')
                if pub_date is not None:
                    entry['pub_date'] = data.get_date_from_timestamp(pub_date)

                add_date = data.get_opt_key(item, 'actionTimestamp')
                if add_date is not None:
                    entry['add_date'] = data.get_date_from_timestamp(add_date)
                    entry['add_time'] = data.get_time_from_timestamp(
                        add_date).strftime('%H:%M:%S')

                summary = data.get_opt_key(item, 'summary', 'content')
                if summary is not None:
                    entry['summary'] = data.remove_tags(summary)

                keywords = data.get_opt_key(item, 'keywords')
                if keywords is not None:
                    entry['keywords'] = ' : '.join(keywords)

                entries.append(entry)

            continuation = data.get_opt_key(contents, 'continuation')
            if continuation is None:
                break

    entries = {
        'downloaded': downloaded,
        'fieldnames': fieldnames,
        'entries': entries}

    return entries

def write_entries_csv(entries):

    """Write entries to a csv."""

    downloaded = entries['downloaded']
    fieldnames = entries['fieldnames']
    entries = entries['entries']

    try:

        filename = '{0}-{1}-{2}.csv'.format(
            settings.download_title,
            data.get_date_from_timestamp(downloaded),
            data.get_time_from_timestamp(downloaded).strftime('%H-%M-%S'))

        filepath = os.path.join(settings.data_dir, filename)

        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for entry in entries:
                writer.writerow(entry)

        set_last_downloaded(downloaded)

    except:
        raise

def get_last_downloaded():

    """Get the timestamp for the last time data was downloaded."""

    try:
        with open(TIMESTAMP_FILE) as f:
            timestamp_str = f.read()
            return int(timestamp_str)
    except FileNotFoundError:
        return None

def set_last_downloaded(timestamp):

    """Set the timestamp for the last time data was downloaded."""

    with open(TIMESTAMP_FILE, 'w') as f:
        f.write('{0}'.format(timestamp))
