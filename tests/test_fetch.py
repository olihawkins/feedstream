# -*- coding: utf-8 -*-

# Imports ---------------------------------------------------------------------

import json
import unittest
import feedstream.fetch as fetch
from unittest.mock import patch

# Tests -----------------------------------------------------------------------

class TestFetchTagIds(unittest.TestCase):

    @patch('feedstream.fetch.requests.get')
    @patch('feedstream.fetch.settings.access_token', 'access token')
    @patch('feedstream.fetch.settings.enterprise', False)
    def test_fetch_tag_ids(self, mock_get):

        """
        Test that fetch_tag_id passes the correct url and headers for a
        personal account, and returns a json object.

        """

        url = 'https://cloud.feedly.com/v3/tags'
        headers = {'Authorization': 'OAuth {0}'.format('access token')}

        mock_get.return_value.ok = True
        mock_get.return_value.text = '[{{"url": "{0}"}}]'.format(url)

        response = fetch.fetch_tag_ids()
        self.assertEqual(response[0]['url'], url)
        mock_get.assert_called_once_with(url, headers=headers)

    @patch('feedstream.fetch.requests.get')
    @patch('feedstream.fetch.settings.access_token', 'access token')
    @patch('feedstream.fetch.settings.enterprise', True)
    def test_fetch_tag_ids(self, mock_get):

        """
        Test that fetch_tag_id passes the correct url and headers for an
        enterprise account, and returns a json object.

        """

        url = 'https://cloud.feedly.com/v3/enterprise/tags'
        headers = {'Authorization': 'OAuth {0}'.format('access token')}

        mock_get.return_value.ok = True
        mock_get.return_value.text = '[{{"url": "{0}"}}]'.format(url)

        response = fetch.fetch_tag_ids()
        self.assertEqual(response[0]['url'], url)
        mock_get.assert_called_once_with(url, headers=headers)

    @patch('feedstream.fetch.requests.get')
    def test_fetch_tag_ids_api_error(self, mock_get):

        """
        Test that fetch_tag_id raises an ApiError when the response status is
        not ok.

        """

        mock_get.return_value.ok = False
        mock_get.return_value.text = '{0}{1}'.format(
            '{"errorCode":404,"errorId":"ap3int-sv2.2018070302.2773846",',
            '"errorMessage":"API handler not found"}')

        with self.assertRaises(fetch.ApiError):
            response = fetch.fetch_tag_ids()


class TestFetchTagEntryIds(unittest.TestCase):

    @patch('feedstream.fetch.requests.get')
    @patch('feedstream.fetch.settings.access_token', 'access token')
    def test_fetch_tag_entry_ids(self, mock_get):

        """
        Test that fetch_tag_entry_ids passes the correct urls and headers for
        different combinations of arguments, and returns a json object.

        """

        base_url = 'https://cloud.feedly.com/v3/streams/ids?streamId='
        tag_id = 'tag_id'

        url_tag = '{0}{1}'.format(base_url, tag_id)
        url_sin = '{0}{1}{2}'.format(base_url, tag_id, '&newerThan=1')
        url_con = '{0}{1}{2}'.format(base_url, tag_id, '&continuation=2')
        url_cou = '{0}{1}{2}'.format(base_url, tag_id, '&count=3')
        url_all = '{0}{1}{2}'.format(base_url, tag_id,
            '&newerThan=1&continuation=2&count=3')

        headers = {'Authorization': 'OAuth {0}'.format('access token')}

        mock_get.return_value.ok = True

        # Test with just a tag id
        mock_get.return_value.text = '[{{"url": "{0}"}}]'.format(url_tag)
        response = fetch.fetch_tag_entry_ids(tag_id)
        self.assertEqual(response[0]['url'], url_tag)
        mock_get.assert_called_with(url_tag, headers=headers)

        # Test with since argument
        mock_get.return_value.text = '[{{"url": "{0}"}}]'.format(url_sin)
        response = fetch.fetch_tag_entry_ids(tag_id, since=1)
        self.assertEqual(response[0]['url'], url_sin)
        mock_get.assert_called_with(url_sin, headers=headers)

        # Test with continuation argument
        mock_get.return_value.text = '[{{"url": "{0}"}}]'.format(url_con)
        response = fetch.fetch_tag_entry_ids(tag_id, continuation=2)
        self.assertEqual(response[0]['url'], url_con)
        mock_get.assert_called_with(url_con, headers=headers)

        # Test with count argument
        mock_get.return_value.text = '[{{"url": "{0}"}}]'.format(url_cou)
        response = fetch.fetch_tag_entry_ids(tag_id, count=3)
        self.assertEqual(response[0]['url'], url_cou)
        mock_get.assert_called_with(url_cou, headers=headers)

        # Test with all arguments
        mock_get.return_value.text = '[{{"url": "{0}"}}]'.format(url_all)
        response = fetch.fetch_tag_entry_ids(tag_id,
            since=1, continuation=2, count=3)
        self.assertEqual(response[0]['url'], url_all)
        mock_get.assert_called_with(url_all, headers=headers)

    @patch('feedstream.fetch.requests.get')
    def test_fetch_tag_entry_ids_api_error(self, mock_get):

        """
        Test that fetch_tag_entry_ids raises an ApiError when the response
        status is not ok.

        """

        mock_get.return_value.ok = False
        mock_get.return_value.text = '{0}{1}'.format(
            '{"errorCode":404,"errorId":"ap3int-sv2.2018070302.2773846",',
            '"errorMessage":"API handler not found"}')

        with self.assertRaises(fetch.ApiError):
            response = fetch.fetch_tag_entry_ids('tag_id')


class TestFetchEntry(unittest.TestCase):

    @patch('feedstream.fetch.requests.get')
    @patch('feedstream.fetch.settings.access_token', 'access token')
    def test_fetch_tag_ids(self, mock_get):

        """
        Test that fetch_entry passes the correct url and headers, and
        returns a json object.

        """

        url = 'https://cloud.feedly.com/v3/entries/entry_id'
        headers = {'Authorization': 'OAuth {0}'.format('access token')}

        mock_get.return_value.ok = True
        mock_get.return_value.text = '[{{"url": "{0}"}}]'.format(url)

        response = fetch.fetch_entry('entry_id')
        self.assertEqual(response['url'], url)
        mock_get.assert_called_once_with(url, headers=headers)

    @patch('feedstream.fetch.requests.get')
    def test_fetch_entry_api_error(self, mock_get):

        """
        Test that fetch_entry raises an ApiError when the response status is
        not ok.

        """

        mock_get.return_value.ok = False
        mock_get.return_value.text = '{0}{1}'.format(
            '{"errorCode":404,"errorId":"ap3int-sv2.2018070302.2773846",',
            '"errorMessage":"API handler not found"}')

        with self.assertRaises(fetch.ApiError):
            response = fetch.fetch_entry('entry_id')

class TestFetchTagContents(unittest.TestCase):

    @patch('feedstream.fetch.requests.get')
    @patch('feedstream.fetch.settings.access_token', 'access token')
    def test_fetch_tag_entry_ids(self, mock_get):

        """
        Test that fetch_tag_contents passes the correct urls and headers for
        different combinations of arguments, and returns a json object.

        """

        base_url = 'https://cloud.feedly.com/v3/streams/contents?streamId='
        tag_id = 'tag_id'

        url_tag = '{0}{1}'.format(base_url, tag_id)
        url_sin = '{0}{1}{2}'.format(base_url, tag_id, '&newerThan=1')
        url_con = '{0}{1}{2}'.format(base_url, tag_id, '&continuation=2')
        url_cou = '{0}{1}{2}'.format(base_url, tag_id, '&count=3')
        url_all = '{0}{1}{2}'.format(base_url, tag_id,
            '&newerThan=1&continuation=2&count=3')

        headers = {'Authorization': 'OAuth {0}'.format('access token')}

        mock_get.return_value.ok = True

        # Test with just a tag id
        mock_get.return_value.text = '[{{"url": "{0}"}}]'.format(url_tag)
        response = fetch.fetch_tag_contents(tag_id)
        self.assertEqual(response[0]['url'], url_tag)
        mock_get.assert_called_with(url_tag, headers=headers)

        # Test with since argument
        mock_get.return_value.text = '[{{"url": "{0}"}}]'.format(url_sin)
        response = fetch.fetch_tag_contents(tag_id, since=1)
        self.assertEqual(response[0]['url'], url_sin)
        mock_get.assert_called_with(url_sin, headers=headers)

        # Test with continuation argument
        mock_get.return_value.text = '[{{"url": "{0}"}}]'.format(url_con)
        response = fetch.fetch_tag_contents(tag_id, continuation=2)
        self.assertEqual(response[0]['url'], url_con)
        mock_get.assert_called_with(url_con, headers=headers)

        # Test with count argument
        mock_get.return_value.text = '[{{"url": "{0}"}}]'.format(url_cou)
        response = fetch.fetch_tag_contents(tag_id, count=3)
        self.assertEqual(response[0]['url'], url_cou)
        mock_get.assert_called_with(url_cou, headers=headers)

        # Test with all arguments
        mock_get.return_value.text = '[{{"url": "{0}"}}]'.format(url_all)
        response = fetch.fetch_tag_contents(tag_id,
            since=1, continuation=2, count=3)
        self.assertEqual(response[0]['url'], url_all)
        mock_get.assert_called_with(url_all, headers=headers)

    @patch('feedstream.fetch.requests.get')
    def test_fetch_tag_contents_api_error(self, mock_get):

        """
        Test that fetch_tag_contents raises an ApiError when the response
        status is not ok.

        """

        mock_get.return_value.ok = False
        mock_get.return_value.text = json.dumps({
            'errorCode': 404, 'errorId': 'ap3int-sv2.2018070302.2773846',
            'errorMessage': 'API handler not found'})

        with self.assertRaises(fetch.ApiError):
            response = fetch.fetch_tag_contents('tag_id')
