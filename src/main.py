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
        #indicators have 6 parameters, short, long, sig, period, macd_window, and macd_spread
        #short - time period for short EMA
        #long - time period for long EMA
        #sig - time period for signal line EMA
        #period - each of the above is taken over a certain time period, period scales each of the above three by a constant
        #macd_window - when a sell is triggered, i.e. the macd (histogram) crossed over, one more contition must be satisfied
        #before a sell signal is given. in the last (macd_window) values of the macd the histogram must have had a value larger
        #than some threshold, which is called the macd_spread
        
        short = range(11,15)
        long_ = range(22,31)
        sig = range(5,16)
        period = range(10,100,10)
        macd_window = range(20,130,10)#what is this, i don't even know


        last = self.float_cast(self.ticker_data[:,LAST])
        for ii in range(len(short)):
            for jj in range(len(long_)):
                for kk in range(len(sig)):
                    for ll in range(len(period)):
                        for mm in range(len(macd_window)):
                            #print 'MACD(%d, %d, %d)x%d' % (short[ii], long_[jj], sig[kk], period[ll])
                            macd, macd_line, signal_line = self.moving_average_convergence_divergence(last,
                            short[ii], long_[jj], sig[kk], period[ll])
                            delta_macd = numpy.append(0, macd[1:] - macd[0:-1])

                            #so many variables bro, you should probably make a struct or something man,
                            #stop sucking at coding
                            threshold = 0
                            positive = False
                            count_since_switch = 0
                            sell_price = []
                            sell_time = []
                            sell_delta = []
                            sell_change = []
                            sell_index = []
                            buy_price = []
                            buy_time = []
                            max_since_switch = []
                            min_since_switch = []
                            sell_spread = []
                            sell_ongoing = False
                            buy_holdout_timer = 0
                            
                            #COPY PASTA-ING MOST OF THIS, PROBABLY WILL NEVER WORK
                            for nn in range(len(macd)):
                                if positive:
                                    if(macd[nn] > 0):#if we're still positive
                                        count_since_switch += 1
                                    else:#if we've flipped to negative
                                        #not sure what the first condition does, but the second condition checks
                                        #to see if the macd filter has settled down yet
                                        if((count_since_switch > threshold) and (nn > (period[ll] * long_[jj]))):
                                            sell_price.append(last[nn])
                                            sell_time.append(self.ticker_data[nn,UPDATED])
                                            if nn > len(change_in_future_2880[0]):
                                                sell_change.append(0)
                                            else:
                                                sell_change.append(change_in_future_2880[0][nn])
                                            sell_delta.append(delta_macd[nn])
                                            sell_index.append(nn)
                                            sell_spread.append(max(macd[max(0,(nn-macd_window[mm])):nn]))
                                            sell_ongoing = True
                                        positive = False
                                        count_since_switch = 0
                                        max_since_switch = 0
                                        min_since_switch = 0
                                else:
                                    if macd[nn] < 0:
                                        min_since_switch = min(min_since_switch, macd[nn])
                                        count_since_switch += 1
                                    else:
                                        if sell_ongoing:
                                            buy_price.append(last[nn])
                                            buy_time.append(self.ticker_data[nn,UPDATED])
                                            sell_ongoing = False
                                        count_since_switch = 0
                                        positive = True
                                        max_since_switch = 0
                                        min_since_switch = 0
                            #fuck start here
                            profit_number, spread_thresh, sell_count, per_sale = self.calc_profit_spread(sell_change, sell_spread, 1)
                            if sell_count > 1:
                                print 'MACD(%d, %d, %d)x%d, %d - %f, %f, %f, %f' % (short[ii], long_[jj], sig[kk], period[ll], macd_window[mm],profit_number, spread_thresh, sell_count, per_sale)

                            
                            

    def calc_profit_spread(self, change_in_future, sell_spread, max_outliers):
        if len(sell_spread) == 0:
            return (0,0,0,0)
        sell_spread = self.float_cast(sell_spread)
        change_in_future = self.float_cast(change_in_future)
        ix = numpy.argsort(sell_spread)
        ix = ix[::-1]#fliplr
        sell_spread = sell_spread[ix]
        change_in_future = change_in_future[ix]
        
        total_profit = 0
        total_outliers = 0
        slope = 0
        count = 0
        for ii in range(len(ix)):
            if change_in_future[ii] < -.01:#why is this hardcodedTODO TODO TODO
                total_profit = total_profit + change_in_future[ii]
                count = count + 1
            else:
                if ii == 0:
                    slope = 0
                else:
                    slope = sell_spread[ii-1]
                break
        if count == 0:
            count = -1
        per_sale = total_profit/count
        return (total_profit, slope, count, per_sale)
            
                            
    def exponential_moving_average(self, data, alpha):
        maf = [0] * len(data)
        maf = self.float_cast(maf)
        for ii in range(len(data)):
            if ii == 0:
                maf[ii] = data[ii]
            else:
                maf[ii] = (alpha * data[ii]) + ((1-alpha) * maf[ii-1])
        return maf
                            
    def moving_average_convergence_divergence(self, data, short, long_, signal, delta_t):
        short_emaf = self.exponential_moving_average(data, (2.0/((short+1)*delta_t)))
        long_emaf = self.exponential_moving_average(data, (2.0/((long_+1)*delta_t)))
        macd_line = short_emaf - long_emaf
        signal_line = self.exponential_moving_average(macd_line, (2.0/((signal+1) * delta_t)))
        macd = macd_line - signal_line
        return (macd, macd_line, signal_line)
                            

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
        plt.show(block=False)
        
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

