# -*- coding: utf-8 -*-

# Imports ---------------------------------------------------------------------

import json
import requests
import urllib
import feedstream.exceptions as exceptions
from feedstream.config import settings

# Functions -------------------------------------------------------------------

def fetch_tag_ids():

    """Fetch a list of all tag ids."""

    if settings.enterprise:
        tag_url = 'https://cloud.feedly.com/v3/enterprise/tags'
    else:
        tag_url = 'https://cloud.feedly.com/v3/tags'

    headers = {'Authorization': 'OAuth {0}'.format(settings.access_token)}
    response = requests.get(tag_url, headers=headers)
    rjson = json.loads(response.text)

    if response.ok is not True:
        raise exceptions.ApiError(
            response.status_code,
            rjson['errorId'],
            rjson['errorMessage'])

    return rjson


def fetch_tag_entry_ids(tag_id, since=None, continuation=None, count=None):

    """
    Fetch a list of all entry ids for the given tag id. This function makes
    one request. If the result contains a continuation it must be called again
    to retrieve additional entries with the continuation argument.

    """

    id_url = 'https://cloud.feedly.com/v3/streams/ids?streamId='
    tag_id = urllib.parse.quote_plus(tag_id)
    params = ''

    if since is not None:
        params = '{0}&newerThan={1}'.format(params, since)

    if continuation is not None:
        params = '{0}&continuation={1}'.format(params, continuation)

    if count is not None:
        params = '{0}&count={1}'.format(params, count)

    url = '{0}{1}{2}'.format(id_url, tag_id, params)
    headers = {'Authorization': 'OAuth {0}'.format(settings.access_token)}
    response = requests.get(url, headers=headers)
    rjson = json.loads(response.text)

    if response.ok is not True:
        raise exceptions.ApiError(
            response.status_code,
            rjson['errorId'],
            rjson['errorMessage'])

    return rjson


def fetch_entry(entry_id):

    """Fetch an entry for the given entry id."""

    entry_url = 'https://cloud.feedly.com/v3/entries/'
    entry_id = urllib.parse.quote_plus(entry_id)
    url = '{0}{1}'.format(entry_url, entry_id)
    headers = {'Authorization': 'OAuth {0}'.format(settings.access_token)}
    response = requests.get(url, headers=headers)
    rjson = json.loads(response.text)

    if response.ok is not True:
        raise exceptions.ApiError(
            response.status_code,
            rjson['errorId'],
            rjson['errorMessage'])

    return rjson[0]


def fetch_tag_entries(tag_id, since=None, continuation=None, count=None):

    """
    Fetch a list of all entries for the given tag. This function makes one
    request. If the result contains a continuation it must be called again to
    retrieve additional entries with the continuation argument.

    """

    contents_url = 'https://cloud.feedly.com/v3/streams/contents?streamId='
    tag_id = urllib.parse.quote_plus(tag_id)
    params = ''

    if since is not None:
        params = '{0}&newerThan={1}'.format(params, since)

    if continuation is not None:
        params = '{0}&continuation={1}'.format(params, continuation)

    if count is not None:
        params = '{0}&count={1}'.format(params, count)

    url = '{0}{1}{2}'.format(contents_url, tag_id, params)
    headers = {'Authorization': 'OAuth {0}'.format(settings.access_token)}
    response = requests.get(url, headers=headers)
    rjson = json.loads(response.text)

    if response.ok is not True:
        raise exceptions.ApiError(
            response.status_code,
            rjson['errorId'],
            rjson['errorMessage'])

    return rjson


def fetch_access_token():

    """
    Fetches a new access token from the API and saves it to the config file.
    Note that refreshing access tokens through the API only works with
    enterprise accounts. Calling this function when settings.enterprise is
    set to false will raise a FetchError.

    """

    if not settings.enterprise:
        raise exceptions.AccountTypeError(
            'fetch_access_token requires an enterprise account')

    token_url = 'https://cloud.feedly.com/v3/auth/token'

    data = {
        'refresh_token': settings.refresh_token,
        'client_id': 'feedlydev',
        'client_secret': 'feedlydev',
        'grant_type': 'refresh_token'
    }

    response = requests.post(token_url, data=data)
    response_data = json.loads(response.text)
    settings.access_token = response_data['access_token']
    settings.save()
