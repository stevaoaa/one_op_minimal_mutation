#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import csv
import pandas as pd


from numpy import percentile
from numpy.random import rand

# calculate a 5-number summary
if __name__ == "__main__":

    #gonna save the results here to export to a csv file
    all_results = []

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
                valid_mutants = sum_mutants - sum_eqv_mutants
                mutants_by_tc = (sum_mutants - sum_eqv_mutants)/sum_tc
                #avoid information of op that produce lower score or dont generate mutants
                if ms_data_max == 0:
                    pass
                else:

                    #put the results inside a list
                    result = [csv_file[:-4], ms_data_min, quartiles[0], quartiles[1], avg_ms, quartiles[2], ms_data_max, std, sum_tc, valid_mutants, mutants_by_tc]
                    all_results.append(result)

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
                    print('Number of Mutants: {}'.format(valid_mutants))
                    print('Mutants/TC: {} \n'.format(mutants_by_tc))
    
    #after print all results, gonna save then in a csv file
    results_file = 'sumary_best_op.csv'

    #open the csv file
    with open(results_file, "w") as sheet_results:
        
        #creat the csv obj to write the results
        out = csv.writer(sheet_results, delimiter=',',quoting=csv.QUOTE_ALL)
        
        #for every result
        for result in all_results:    
            out.writerow(result) #write the result into the csv file
