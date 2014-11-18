#!/usr/bin/python

import sys
import csv
import os


#read data
def read_file(filename):
    with open(filename, 'rb') as file:
        print 'called'
        reader = csv.reader(file)
        for row in reader:
            placeholder = 0
            #print row


def main(argv=None):
    if argv is None:
        argv = sys.argv
    base = 'ticker_data/btc_usd'
    #get list of directories
    for (dirpath, dirnames, filenames) in os.walk(base):
        for file in filenames:
            read_file(base + '/' + file)
    
if __name__ == "__main__":
    main()
