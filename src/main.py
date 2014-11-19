#!/usr/bin/python

import sys
import csv
import os
import datetime

#stuff
HIGH = 0
LOW = 1
AVG = 2
VOL = 3
VOL_CUR = 4
LAST = 5
BUY = 6
SELL = 7
UPDATED = 8
SERVER_TIME = 9

#read data
def read_file(filename):
    num_lines = sum(1 for line in open(filename))
    day = []
    with open(filename, 'rb') as file:
        reader = csv.reader(file)
        for row in reader:
            day.append(row)
    return (day, num_lines)
            

def main(argv=None):
    if argv is None:
        argv = sys.argv
        
    if len(argv) < 2:
        print 'now you fucked up'
        print 'you have fucked up'
        print 'now you fucked up'
        sys.exit(1)

    #get pair from command line
    pair = argv[1]
    training_length = int(argv[2])
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
        start_date = start_date + datetime.timedelta(days=1)

    #read csvs
    ticker_data = []
    for file in filenames[0:training_length]:
        file_data = read_file(file)
        ticker_data.append(file_data[0])
        print 'Added file %s, %d lines' % (filename,file_data[1])
    
    #get list of directories
    # for (dirpath, dirnames, filenames) in os.walk(directory):
    #     filenames = [f for f in filenames if not f[0] == '.']#ignore hidden files (i.e. files starting with '.')
    #     for file in filenames:
    #         placeholder = 0
    #         #read_file(directory + '/' + file)
    
if __name__ == "__main__":
    main()
