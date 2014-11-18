#!/usr/bin/python

import sys
import csv
import os
import datetime


#read data
def read_file(filename):
    print filename
    with open(filename, 'rb') as file:
        print 'called'
        reader = csv.reader(file)
        for row in reader:
            placeholder = 0
            testing = 0
            print row


def main(argv=None):
    if argv is None:
        argv = sys.argv
        
    if len(argv) < 1:
        print 'now you fucked up'
        print 'you have fucked up'
        print 'now you fucked up'
        sys.exit(1)

    #get pair from command line
    pair = argv[1]
    directory = 'ticker_data/' + pair
        
    #get list of dates from 3/06 to 11/17
    start_date = datetime.date(2014, 3, 6)
    end_date = datetime.date(2014, 11, 17)
    
    filenames = []
    #construct filenames and check if they exist
    while start_date != end_date:
        filename = pair + '_' + str(start_date.year) + '_' + str('%02d' % start_date.month) + '_' + str('%02d' % start_date.day) + '.tkr'
        if os.path.isfile(directory + '/' + filename):
            filenames.append(directory + '/' + filename)
            #print 'cannot find file: %s' % filename
            #read_file(directory + '/' + filename)
        start_date = start_date + datetime.timedelta(days=1)

    for file in filenames:
        read_file(file)
    
    #get list of directories
    # for (dirpath, dirnames, filenames) in os.walk(directory):
    #     filenames = [f for f in filenames if not f[0] == '.']#ignore hidden files (i.e. files starting with '.')
    #     for file in filenames:
    #         placeholder = 0
    #         #read_file(directory + '/' + file)
    
if __name__ == "__main__":
    main()
