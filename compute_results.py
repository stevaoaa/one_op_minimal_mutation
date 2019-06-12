#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import csv

from programs import *
from operators import *

"""
recives the results then save in the corresponding csv file
"""
def write_csv_results(operator, results, wipeout = False):

	directory = '../../results'

	#check wheter the dir exists 
	if not os.path.exists(directory):
		os.makedirs(directory)

	#result dir should be empty

	#acess the dir
	r = os.chdir(directory)	

	#file that will be opened
	filename = operator + '.csv'

	#open the file 
	with open(filename, 'a') as csv_file:

		#write the results into the corresponding csv file
		output_writer = csv.writer(csv_file)
		output_writer.writerow(results)


	#back to the original program dir
	program_dir = '../programs/' + results[0]
	r = os.chdir(program_dir)



"""
Read the information from the result file
"""
def read_all_results(program, afile):

	#get all operators -> [[usual_operators], [deletion_operators], [operators_set]]
	operators_list = get_operators()
	operators_list = list(operators_list[2]) #use information of all operators

	#a list with the content of each line of the file
	lines = afile.readlines()   

	i = 0  #a pointer t control the information that will be readed	

	while i < len(lines):

		#base case.. the result file always will ends in a empty line
		if lines[i] == '':
			break
		
		#read the userful information
		mutation_operator    = lines[i].strip()
		mutation_score_avg   = float(lines[i + 1].strip()) #this should be divided by 10 because this value reffers to 10 iterations
		mutants_by_operator  = lines[i + 2].strip()
		equivalent_mutants   = lines[i + 3].strip()
		number_testcases_avg = int(lines[i + 4].strip()) #this should be divided by 10 because this value reffers to 10 iterations

		#save this information into a csv file
		results = [program, mutation_score_avg/10, number_testcases_avg/10, mutants_by_operator, equivalent_mutants]

		#write the results into a valid csv file
		write_csv_results(mutation_operator, results)

		#update the value of the pointer
		i = i + 5


if __name__ == '__main__':

	#enter inside the programs folder
	r = os.chdir('programs')

	#name of the file that store the execution results
	filename = "result.txt"

	#get the name of the programs
	programs_list = list_programs()

	for program in programs_list:
		
		#enter inside a program folder
		r = os.chdir(program)

		#perform some operation with result_file
		with open(filename, "r") as result_file:

			#read the results for that file
			read_all_results(program, result_file)

		#back to programs dir
		r = os.chdir("..")

	#at the end back to root dir
	r = os.chdir("..")
