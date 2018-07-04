# -*- coding: utf-8 -*-

# Imports ---------------------------------------------------------------------

import datetime
import json
import unittest
import feedstream.data as data
import feedstream.download as download
from unittest.mock import patch

# Mocks -----------------------------------------------------------------------

def get_mock_entry():

    mock_entry = {
        'id': 'entry_id',
        'canonicalUrl': 'http://domain.com/entry',
        'title': 'Title',
        'author': 'Author',
        'origin': {'title': 'Publisher'},
        'actionTimestamp': 1530631149285,
        'published': 1530631149285,
        'summary': {'content': '<p>Lorem ipsum.</p> <p>Doler <b>sit</b> ...'},
        'keywords': ['some', 'keywords']}

    return mock_entry

def mock_requests_get(*args, **kwargs):

    class MockResponse:

        def __init__(self, status_code, json_data):
            self.ok = True if status_code == 200 else False
            self.status_code = status_code
            self.json_data = json_data
            self.text = json.dumps(self.json_data)

    mock_entry = get_mock_entry()

    tag_url = 'http://cloud.feedly.com/v3/tags'
    contents_url = 'http://cloud.feedly.com/v3/streams/contents?streamId='
    contents_url_id_a = '{0}{1}'.format(contents_url, 'id_a')
    contents_url_id_b = '{0}{1}'.format(contents_url, 'id_b')
    contents_url_id_b_con = '{0}{1}{2}'.format(contents_url, 'id_b',
        '&continuation=1')

    if args[0] == tag_url:
        return MockResponse(200, [
            {'id': 'id_a', 'label': 'lab_a'},
            {'id': 'id_b', 'label': 'lab_b'}])

    if args[0] == contents_url_id_a:
        return MockResponse(200, {'id': 'id_a', 'items': [mock_entry]})

    if args[0] == contents_url_id_b:
        return MockResponse(200, {'id': 'id_b', 'items': [
            mock_entry, mock_entry], 'continuation': '1'})

    if args[0] == contents_url_id_b_con:
        return MockResponse(200, {'id': 'id_b', 'items': [
            mock_entry, mock_entry]})

    return MockResponse(404, {'errorCode': 404,
        'errorId': 'ap3int-sv2.2018070302.2773846',
        'errorMessage': 'API handler not found'})

# Tests -----------------------------------------------------------------------

class TestDownloadEntries(unittest.TestCase):

    @patch('feedstream.fetch.requests.get', side_effect=mock_requests_get)
    @patch('feedstream.fetch.settings.access_token', 'access token')
    @patch('feedstream.fetch.settings.download_new', False)
    @patch('feedstream.data.settings.timezone', 'Europe/London')
    def test_download_entries(self, mock_get):

        """
        Test that download_entries returns the expected output with mocked
        responses from the API. Specifically this function tests that
        download_entries first downloads a set of tag_ids, and then downloads
        the entries for each tag in turn, handling continuation ids in the
        returned data, and returns the expected json. It does not test whether
        the function correctly download all entries or just the new entries
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

        # Check the mock entry was processed correctly
        mock_entry = get_mock_entry()
        test_entry = entries['entries'][0]

        self.assertEqual(sorted(list(test_entry.keys())), sorted(fieldnames))
        self.assertEqual(test_entry['tag_id'], 'id_a')
        self.assertEqual(test_entry['tag_label'], 'lab_a')
        self.assertEqual(test_entry['article_id'], mock_entry['id'])
        self.assertEqual(test_entry['url'], mock_entry['canonicalUrl'])
        self.assertEqual(test_entry['title'], mock_entry['title'])
        self.assertEqual(test_entry['author'], mock_entry['author'])
        self.assertEqual(test_entry['summary'], 'Lorem ipsum. Doler sit ...')

        self.assertEqual(test_entry['publisher'],
            mock_entry['origin']['title'])

        self.assertEqual(test_entry['add_timestamp'],
            mock_entry['actionTimestamp'])

        self.assertEqual(test_entry['keywords'],
            ' : '.join(mock_entry['keywords']))

        self.assertEqual(test_entry['pub_date'], datetime.date(2018, 7, 3))
        self.assertEqual(test_entry['add_date'], datetime.date(2018, 7, 3))
        self.assertEqual(test_entry['add_time'], '16:19:09')
