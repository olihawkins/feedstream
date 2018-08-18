# -*- coding: utf-8 -*-

# Imports ---------------------------------------------------------------------

import feedstream.download as download

# Functions -------------------------------------------------------------------

def main():

    print('Getting data from Feedly ...')
    filename = download.download_entries_csv()
    print('Data downloaded to {0} in the data directory'.format(filename))

# Main ------------------------------------------------------------------------

main()
