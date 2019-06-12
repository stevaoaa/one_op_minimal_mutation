#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pandas as pd


from numpy import percentile
from numpy.random import rand

# calculate a 5-number summary
if __name__ == "__main__":

    #enter inside the programs folder
    r = os.chdir('general')

    #read the files
    for root, dirs, files in os.walk(".", topdown=False):
        for csv_file in files:    
            
            #check wheter it's a valid csv file
            if csv_file[-4:] != ".csv":
                continue #ignore
            
            #valid csv file, open it
            else:
                
                #open with pandas
                csv_data = pd.read_csv(csv_file)                

                #get the mutation score results (second column)
                ms_data = csv_data.iloc[:,1]
                tc_data = csv_data.iloc[:,2]
                mutants_data = csv_data.iloc[:,3]
                eqv_mutants_data = csv_data.iloc[:,4]

                # calculate quartiles
                quartiles = percentile(ms_data, [25, 50, 75])

                # calculate min/max
                ms_data_min, ms_data_max = ms_data.min(), ms_data.max()

                #calclate de average
                avg_ms = ms_data.mean()
                avg_tc = tc_data.mean()
                avg_mutants = mutants_data.mean()
                avg_eq_mutants = eqv_mutants_data.mean()

                #sum
                sum_tc = tc_data.sum()
                sum_mutants = mutants_data.sum()
                sum_eqv_mutants = eqv_mutants_data.sum()

                #standard deviation
                std = ms_data.std()

                #avoid information of op that produce lower score or dont generate mutants
                if ms_data_max == 0:
                    pass
                else:

                    # print summary
                    print('Results for Operator: {}'.format(csv_file[:-4]))
                    print('Min MS: %.3f' % ms_data_min)
                    print('Q1 MS: %.3f' % quartiles[0])
                    print('Median MS: %.3f' % quartiles[1])
                    print('Average MS: %.3f' % avg_ms)
                    print('Q3 MS: %.3f' % quartiles[2])
                    print('Max MS: %.3f' % ms_data_max)
                    print('St. Dev. MS: %.3f' % std)
                    print('Number of TC: {}'.format(sum_tc))
                    print('Number of Mutants: {}'.format(sum_mutants - sum_eqv_mutants))
                    print('Mutants/TC: {} \n'.format( (sum_mutants - sum_eqv_mutants)/sum_tc))