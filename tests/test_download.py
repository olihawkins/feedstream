# -*- coding: utf-8 -*-

# Imports ---------------------------------------------------------------------

import datetime
import json
import os
import unittest
import feedstream.data as data
import feedstream.download as download

from unittest.mock import patch, call
from tests.test_data import get_mock_entry

# Mocks -----------------------------------------------------------------------

def mock_requests_get(*args, **kwargs):

    class MockResponse:

        def __init__(self, status_code, json_data):
            self.ok = True if status_code == 200 else False
            self.status_code = status_code
            self.json_data = json_data
            self.text = json.dumps(self.json_data)

    mock_entry = get_mock_entry()

    tag_url = 'https://cloud.feedly.com/v3/tags'
    contents_url = 'https://cloud.feedly.com/v3/streams/contents?streamId='

    contents_url_id_a = '{0}{1}'.format(contents_url, 'id_a')
    contents_url_id_b = '{0}{1}'.format(contents_url, 'id_b')
    contents_url_id_b_con = '{0}{1}{2}'.format(contents_url, 'id_b',
        '&continuation=1')

    contents_url_id_a_nt = '{0}{1}{2}'.format(contents_url, 'id_a',
        '&newerThan=100')
    contents_url_id_b_nt = '{0}{1}{2}'.format(contents_url, 'id_b',
        '&newerThan=100')
    contents_url_id_b_con_nt = '{0}{1}{2}'.format(contents_url, 'id_b',
        '&newerThan=100&continuation=1')

    if args[0] == tag_url:
        return MockResponse(200, [
            {'id': 'id_a', 'label': 'lab_a'},
            {'id': 'id_b', 'label': 'lab_b'}])

    if args[0] == contents_url_id_a or args[0] == contents_url_id_a_nt:
        return MockResponse(200, {'id': 'id_a', 'items': [mock_entry]})

    if args[0] == contents_url_id_b or args[0] == contents_url_id_b_nt:
        return MockResponse(200, {'id': 'id_b', 'items': [
            mock_entry, mock_entry], 'continuation': '1'})

    if args[0] == contents_url_id_b_con or args[0] == contents_url_id_b_con_nt:
        return MockResponse(200, {'id': 'id_b', 'items': [
            mock_entry, mock_entry]})

    return MockResponse(404, {'errorCode': 404,
        'errorId': 'ap3int-sv2.2018070302.2773846',
        'errorMessage': 'API handler not found'})

def mock_get_last_downloaded():
    return 100

# Tests -----------------------------------------------------------------------

class TestDownloadEntries(unittest.TestCase):

    @patch('feedstream.fetch.requests.get', side_effect=mock_requests_get)
    @patch('feedstream.fetch.settings.access_token', 'access token')
    @patch('feedstream.fetch.settings.enterprise', False)
    @patch('feedstream.fetch.settings.download_new', False)
    @patch('feedstream.data.settings.timezone', 'Europe/London')
    def test_download_entries(self, mock_get):

        """
        Test that download_entries returns the expected output with mocked
        responses from the API. Specifically this function tests that
        download_entries first downloads a set of tag_ids, and then downloads
        the entries for each tag in turn, handling continuation ids in the
        returned data, and returns the expected json. It does not test whether
        the function correctly downloads all entries or just the new entries
        depending on the setttings: this is tested separately below.

        """

        entries = download.download_entries()

        # Check downloaded is an integer timestamp that parses as a datetime
        self.assertIsInstance(entries['downloaded'], int)
        self.assertIsInstance(datetime.datetime.fromtimestamp(
            int(entries['downloaded'] / 1000)), datetime.datetime)

        # Check fieldnames are as expected
        fieldnames = data.FIELDNAMES
        self.assertEqual(entries['fieldnames'], fieldnames)

        # Check the number of entries are as expected
        self.assertEqual(len(entries['entries']), 5)

        # Check the json for each entry has the expected structre
        for test_entry in entries['entries']:
            self.assertEqual(
                sorted(list(test_entry.keys())),
                sorted(data.FIELDNAMES))

    @patch('feedstream.fetch.requests.get', side_effect=mock_requests_get)
    @patch('feedstream.fetch.settings.access_token', 'access token')
    @patch('feedstream.fetch.settings.enterprise', False)
    @patch('feedstream.fetch.settings.download_new', False)
    @patch('feedstream.data.settings.timezone', 'Europe/London')
    def test_download_entries_all(self, mock_get):

        """
        Test that download_entries downloads all entries if the download_new
        setting is False.

        """

        entries = download.download_entries()
        headers = {'Authorization': 'OAuth {0}'.format('access token')}
        calls = [
            call('https://cloud.feedly.com/v3/tags', headers=headers),
            call('{0}{1}'.format('https://cloud.feedly.com/v3/streams/contents',
                '?streamId=id_a'), headers={'Authorization':
                'OAuth access token'}),
            call('{0}{1}'.format('https://cloud.feedly.com/v3/streams/contents',
                '?streamId=id_b'), headers={'Authorization':
                'OAuth access token'}),
            call('{0}{1}'.format('https://cloud.feedly.com/v3/streams/contents',
                '?streamId=id_b&continuation=1'), headers={'Authorization':
                'OAuth access token'})]

        mock_get.assert_has_calls(calls)

    @patch('feedstream.fetch.requests.get', side_effect=mock_requests_get)
    @patch('feedstream.fetch.settings.access_token', 'access token')
    @patch('feedstream.fetch.settings.enterprise', False)
    @patch('feedstream.fetch.settings.download_new', True)
    @patch('feedstream.data.settings.timezone', 'Europe/London')
    @patch('feedstream.download.get_last_downloaded', mock_get_last_downloaded)
    def test_download_entries_new(self, mock_get):

        """
        Test that download_entries downloads just new entries if the
        download_new setting is True.

        """

        entries = download.download_entries()
        headers = {'Authorization': 'OAuth {0}'.format('access token')}
        calls = [
            call('https://cloud.feedly.com/v3/tags', headers=headers),
            call('{0}{1}'.format('https://cloud.feedly.com/v3/streams/contents',
                '?streamId=id_a&newerThan=100'), headers={'Authorization':
                'OAuth access token'}),
            call('{0}{1}'.format('https://cloud.feedly.com/v3/streams/contents',
                '?streamId=id_b&newerThan=100'), headers={'Authorization':
                'OAuth access token'}),
            call('{0}{1}'.format('https://cloud.feedly.com/v3/streams/contents',
                '?streamId=id_b&newerThan=100&continuation=1'),
                headers={'Authorization': 'OAuth access token'})]

        mock_get.assert_has_calls(calls)

class TestTimestampFunctions(unittest.TestCase):

    """
    Tests that timestamps are correctly written to and read from the
    timestamp file.

    """

    def setUp(self):

        self.timestamp = 1000
        self.timestamp_file = 'timestamp.txt'
        open(self.timestamp_file, 'a').close()

    @patch('feedstream.download.TIMESTAMP_FILE', 'timestamp.txt')
    def test_get_and_set_last_downloaded(self):

        download.set_last_downloaded(self.timestamp)
        timestamp = download.get_last_downloaded()
        self.assertEqual(timestamp, self.timestamp)

    def tearDown(self):
        os.remove(self.timestamp_file)
