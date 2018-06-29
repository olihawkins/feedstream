# -*- coding: utf-8 -*-

# Imports ---------------------------------------------------------------------

import json
import requests
import urllib
import feedstream.settings as settings

# Functions -------------------------------------------------------------------

def fetch_tag_ids():

    """Fetch a list of all tag ids."""

    tag_url = 'http://cloud.feedly.com/v3/tags'
    headers = {'Authorization': 'OAuth {0}'.format(settings.access_token)}
    response = requests.get(tag_url, headers=headers)
    return json.loads(response.text)

def fetch_tag_entry_ids(tag_id):

    """Fetch a list of all entry ids for the given tag id."""

    id_url = 'http://cloud.feedly.com/v3/streams/ids?streamId='
    tag_id = urllib.parse.quote_plus(tag_id)
    url = '{0}{1}'.format(id_url, tag_id)
    headers = {'Authorization': 'OAuth {0}'.format(settings.access_token)}
    response = requests.get(url, headers=headers)
    return json.loads(response.text)

def fetch_tag_contents(tag_id):

    """Fetch a list of entries and their contents for the given tag id."""

    contents_url = 'http://cloud.feedly.com/v3/streams/contents?streamId='
    tag_id = urllib.parse.quote_plus(tag_id)
    url = '{0}{1}'.format(contents_url, tag_id)
    headers = {'Authorization': 'OAuth {0}'.format(settings.access_token)}
    response = requests.get(url, headers=headers)
    return json.loads(response.text)

def fetch_entry(entry_id):

    """Fetch an entry for the given entry id."""

    entry_url = 'http://cloud.feedly.com/v3/entries/'
    entry_id = urllib.parse.quote_plus(entry_id)
    url = '{0}{1}'.format(entry_url, entry_id)
    headers = {'Authorization': 'OAuth {0}'.format(settings.access_token)}
    response = requests.get(url, headers=headers)
    return json.loads(response.text)
