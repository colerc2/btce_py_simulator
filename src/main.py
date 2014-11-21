#!/usr/bin/python

import sys
import csv
import os
import datetime
import numpy
import matplotlib.pyplot as plt

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

CHANGE_LOW = 0
CHANGE_HIGH = 1

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
    
        #read csvs and convert to numpy arrays
        self.ticker_data = []
        self.read_csvs(self.filenames, training_length)
        self.ticker_data = numpy.array(self.ticker_data)
        print len(self.ticker_data)
        #for row in self.ticker_data:
        #    print row[LAST]
        
        #crunch numbers
        print 'start'
        change_in_future_2880 = self.change_in_future(2880)
        plt.plot(range(change_in_future_2880),change_in_future_2880)
        plt.show()
        print 'end'

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

    def change_in_future(self, time_period):
        change = []
        low = [0] * (len(self.ticker_data)-time_period+1)
        high = [0] * (len(self.ticker_data)-time_period+1)
        temp_last_array = self.ticker_data[:,LAST]
        temp_last_array = temp_last_array.astype(numpy.float64)
        for ii in range(len(self.ticker_data)-time_period+1):
            changes = temp_last_array[(ii):(ii+time_period-1)]
            changes = changes - temp_last_array[ii]
            changes = changes / temp_last_array[ii]#make it a percent relative to current value
            low[ii] = min(changes)
            high[ii] = max(changes)
        change.append(low)
        change.append(high)
        return change

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

