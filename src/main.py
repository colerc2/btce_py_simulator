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
        print 'Reading in data...'
        self.ticker_data = []
        self.read_csvs(self.filenames, training_length)
        self.ticker_data = numpy.array(self.ticker_data)
        print '%s data points read.' % str(len(self.ticker_data))
        
        #crunch numbers
        print 'Crunching some numbers...'
        change_in_future_2880 = self.change_in_future(2880)
        temp_last_array = self.ticker_data[:,LAST]
        temp_last_array = temp_last_array.astype(numpy.float64)
        self.make_future_change_plot(temp_last_array, change_in_future_2880)
        print 'Done crunching'

        #values for this run
        short = range(11,15)
        long = range(22,31)
        sig = (5,16)
        period = range(10,100,10)#what is this, i don't even know
        macd_window = range(20,130,10)#what is this, i don't even know


        last = float_cast(self.ticker_data(:,LAST))
        for ii in short:
            for jj in long:
                for kk in sig:
                    for ll in period:
                        for mm in macd_window:
                            
        

    def exponential_moving_average(data, alpha):
        maf = [0] * len(data)
        for ii in range(len(data)):
            if ii == 1:
                maf[ii] = data[ii]
            else:
                maf[ii] = alpha * data[ii] + (1-alpha)*maf[ii-1]
        return maf
                            
    def moving_average_convergence_divergence(data, short, long, signal, delta_t):
        short_emaf = self.exponential_moving_average(data, (2/((short+1)*delta_t)))
        long_emaf = self.exponential_moving_average(data, (2/((long+1)*delta_t)))
        macd_line = short_emaf - long_emaf
        signal_line = self.exponential_moving_average(macd_line, (2/((signal+1) * delta_t)))
        macd = macd_line - signal_line
        return macd
                            

    def float_cast(self, ary):
        ary = numpy.array(ary)
        return ary.astype(numpy.float64)
        
    #make plot of last sell price with future changes shown
    def make_future_change_plot(self, tkr, change):
        #plt.plot(range(len(tkr)), tkr)
        low = self.float_cast(change[0])
        high = self.float_cast(change[1])
        low = tkr[0:len(low)] + (tkr[0:len(low)]*low)
        high = tkr[0:len(high)] + (tkr[0:len(high)]*high)
        plt.plot(range(len(tkr)), tkr, range(len(low)), low, range(len(high)), high, linewidth=2.0)
        plt.grid(True)
        plt.legend(['tkr', 'low', 'high'])
        plt.show()
        
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
        changes = [0] * (time_period-1)
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

