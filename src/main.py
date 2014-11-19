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

class SignalAnalysis():
    def __init__(self, pair, training_length, directory):
        self.pair = pair
        self.training_length = training_length
        self.directory = directory
        
        #get list of dates from 3/06 to 11/17
        self.start_date = datetime.date(2014, 3, 6)#great coding style
        self.end_date = datetime.date(2014, 11, 17)   
        self.filenames = []
        self.create_filenames(self.start_date, self.end_date)
    
        #read csvs
        self.ticker_data = []
        ticker_data = self.read_csvs(self.filenames, training_length)
        print len(self.ticker_data)

    #read data
    def read_file(self, filename):
        num_lines = sum(1 for line in open(filename))
        day = []
        with open(filename, 'rb') as file:
            reader = csv.reader(file)
            for row in reader:
                day.append(row)
        return (day, num_lines)

    def create_filenames(self, start_date, end_date):
        #construct filenames and check if they exist
        while start_date != end_date:
            filename = pair + '_' + str(start_date.year) + '_' + str('%02d' % start_date.month) + '_' + str('%02d' % start_date.day) + '.tkr'
            if os.path.isfile(directory + '/' + filename):
                self.filenames.append(directory + '/' + filename)
            start_date = start_date + datetime.timedelta(days=1)

    def read_csvs(self, filenames, training_length):
        for file in filenames[0:training_length]:
            file_data = self.read_file(file)
            self.ticker_data += (file_data[0])
            print 'Added file %s, %d lines' % (file,file_data[1])

if __name__ == '__main__':
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

    sinal_analysis = SignalAnalysis(pair, training_length, directory)

