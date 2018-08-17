# -*- coding: utf-8 -*-

# Imports ---------------------------------------------------------------------

import json
import requests
import urllib
from feedstream.config import settings

# Exceptions ------------------------------------------------------------------

class Error(Exception):

    """Base class for exceptions in this module."""
    pass


class ApiError(Error):

    """
    Exception raised for API responses whose status code is not 200.

    Attributes:
        status_code -- status code of the response
        api_id -- API error id
        api_msg -- API error message
    """

    def __init__(self, status_code, api_id, api_msg):
        self.status_code = status_code
        self.api_id = api_id
        self.api_msg = api_msg

# Personal API ----------------------------------------------------------------

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
        raise ApiError(
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
        raise ApiError(
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
        raise ApiError(
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
        raise ApiError(
            response.status_code,
            rjson['errorId'],
            rjson['errorMessage'])

    return rjson
