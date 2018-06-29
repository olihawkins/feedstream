# -*- coding: utf-8 -*-

# Imports ---------------------------------------------------------------------

import csv
import feedstream.fetch as fetch
import feedstream.clean as clean

# Functions -------------------------------------------------------------------

def download_entries():

    """Download items from each tag to a csv."""

    fieldnames = [
        'board',
        'pub_date',
        'add_date',
        'publisher',
        'url',
        'title',
        'author',
        'summary',
        'keywords']

    rows = []
    tag_ids = fetch.fetch_tag_ids()

    for tag_id in tag_ids:

        contents = fetch.fetch_tag_contents(tag_id['id'])

        for entry in contents['items']:

            row = {}

            row['board'] = tag_id['label']
            row['publisher'] = clean.get_optional_key(entry, 'origin', 'title')
            row['url'] = clean.get_entry_url(entry)
            row['title'] = clean.get_optional_key(entry, 'title')
            row['author'] = clean.get_optional_key(entry, 'author')

            pub_date = clean.get_optional_key(entry, 'published')
            if pub_date is not None:
                row['pub_date'] = clean.get_timestamp_date(pub_date)

            add_date = clean.get_optional_key(entry, 'actionTimestamp')
            if add_date is not None:
                row['add_date'] = clean.get_timestamp_date(add_date)

            summary = clean.get_optional_key(entry, 'summary', 'content')
            if summary is not None:
                row['summary'] = clean.remove_tags(summary)

            keywords = clean.get_optional_key(entry, 'keywords')
            if keywords is not None:
                row['keywords'] = ' : '.join(keywords)

            rows.append(row)

    with open('data.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
