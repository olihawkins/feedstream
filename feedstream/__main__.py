# -*- coding: utf-8 -*-

# Imports ---------------------------------------------------------------------

import feedstream.download as download

# Functions -------------------------------------------------------------------

def main():

    print('')
    print('Getting data from Feedly ...')
    filename = download.write_entries_csv(download.download_entries())
    print('Data downloaded to {0} in the data directory'.format(filename))

# Main ------------------------------------------------------------------------
main()
