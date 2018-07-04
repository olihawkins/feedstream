# feedstream

A Python library for downloading data from the Feedly API. This is not a wrapper for the full Feedly API but a library that is designed to support a particular workflow, in which articles are classified in Feedly using boards and data on the articles is downloaded for analysis.

## Usage

Simply set the API token and timezone in settings.py and download data on all articles that have been added as entries to boards in Feedly with `download_entries()`. This returns a dictionary with three keys:

- `downloaded` contains a Feedly timestamp of the last time data was downloaded
- `fieldnames` is a list of fieldnames used as keys for each entry in the list
- `entries` is a list of all entries on boards, along with the id and name of their board

You can set the library to only download articles that have been added to boards since the last time data was downloaded by setting `download_new` to `True` in settings.py. The downloaded entries can be written to a csv with `write_entries(entries)`, or converted directly to a pandas dataframe with `pandas.DataFrame(entries['entries'])`.

Run the program directly on the command line with `python -m feedstream`, which downloads the data to a csv in the data directory.

## Tests
Run `python -m unittest -v` to run the unit tests.
