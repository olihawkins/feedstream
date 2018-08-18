# -*- coding: utf-8 -*-

# Imports ---------------------------------------------------------------------

import csv
import datetime
import os
import pandas
import pathlib
import feedstream.fetch as fetch
import feedstream.data as data
from feedstream.config import settings

# Constants -------------------------------------------------------------------

TIMESTAMP_FILE = os.path.join(settings.timestamp_file)

# Download functions ----------------------------------------------------------

def download_entries(flatten=False):

    """Download entries for each tag and return a dict of the parsed items."""

    items = []
    since = get_last_downloaded() if settings.download_new else None
    downloaded = data.get_timestamp_from_datetime(datetime.datetime.now())
    tag_ids = fetch.fetch_tag_ids()

    for tag_id in tag_ids:

        continuation = None

        while True:

            contents = fetch.fetch_tag_entries(tag_id['id'],
                since=since, continuation=continuation)

            for item in contents['items']:

                item = data.parse_item(tag_id['id'],
                    tag_id['label'], item, flatten)
                items.append(item)

            continuation = data.get_opt_key(contents, 'continuation')
            if continuation is None:
                break

    entries = {
        'timestamp': downloaded,
        'fieldnames': data.FIELDNAMES,
        'items': items}

    return entries

def download_entries_df():

    """
    Download entries for each tag and return a dataframe of the items. Nested
    fields are flattened into a single field with items separated using the
    separator string defined in the data module. The function returns a tuple
    containing the timestamp of the download and the dataframe itself.

    """

    entries = download_entries(flatten=True)
    timestamp = entries['timestamp']
    df = pandas.DataFrame(entries['items'])
    return (timestamp, df)

def download_entries_csv():

    """Download entries to a csv"""

    entries = download_entries(flatten=True)
    downloaded = entries['timestamp']
    fieldnames = entries['fieldnames']
    items = entries['items']

    try:

        pathlib.Path(settings.data_dir).mkdir(exist_ok=True)

        filename = '{0}-{1}-{2}.csv'.format(
            settings.download_prefix,
            data.get_date_from_timestamp(downloaded),
            data.get_time_from_timestamp(downloaded).strftime('%H-%M-%S'))

        filepath = os.path.join(settings.data_dir, filename)

        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames,
                quoting=csv.QUOTE_NONNUMERIC)
            writer.writeheader()
            for item in items:
                writer.writerow(item)

        set_last_downloaded(downloaded)
        return filename

    except:
        raise

# Timestamp functions ---------------------------------------------------------

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

    pathlib.Path(settings.data_dir).mkdir(exist_ok=True)

    with open(TIMESTAMP_FILE, 'w') as f:
        f.write('{0}'.format(timestamp))
