#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
from mutant_util import *
from operators import *
from compute_minimal_mutants import *
from short_compute_one_sequence import *


"""
Use this fuction to restore the selection of mutants and testcases in a proteum session
"""
def restore_original_session(program):

   print "I: Restoring the original data from the session"

   # enable all test cases again for futher execution
   statement = 'tcase -e ' + program
   os.system(statement)
   print statement

   #enable all mutants again for futher execution
   statement = 'exemuta -select -u- 1 ' + program
   os.system(statement)
   print statement

   #exemuta to validate the changes
   statement = 'exemuta -exec ' + program
   os.system(statement)
   print statement




def run_experiment(program, operators):

   #at the beginning of the experiment restore the proteum session 
   restore_original_session(program)

   print "I: Begin of the experiment execution"

   #seed controls the order that the testcases are selected in each iteration of the experiment (check proteum manpages)
   seed = 0

   #files to store the results
   total_file = open("result.txt", "w")
   results_file_list = []

   #creating the result files
   while (seed < 10):
      fname = "result" + str(seed) + ".txt"
      results_file_list.append(open(fname, "w"))
      seed += 1


   # for each operator select 10 different testset
   # and check the score relative to all operators agains the minimal mutants

   #will analyze each operator
   for operator in operators:

      print "I: Evaluating the operator: {}".format(operator)

      seed = 0
      total_test_cases     = 0   #number of test cases used for all operators
      total_mutation_score = 0.0 #mutation score obteined for all operators
      
      #run 10 different samples
      while (seed < 10):

         print "I: Runing the seed: {}   ################################".format(seed)

         results = getOpProgDataV4(program, seed, operator)

         minimal_mutation_score_by_op  = results[0] #mutation socore achived using the testset of a given operator against the minimal set
         number_of_mutants_by_op       = results[1] #number of mutants for the op set
         number_equivalents_by_op      = results[2] #this will always be zero
         number_test_cases_by_op       = results[3] #number of testcases used in every op

         #saving the results for each iteration in a file
         results_file_list[seed].write(operator + "\n" + str(minimal_mutation_score_by_op)     + 
                                                  "\n" + str(number_of_mutants_by_op)  + 
                                                  "\n" + str(number_equivalents_by_op) + 
                                                  "\n" + str(number_test_cases_by_op)  + "\n")

         #mantain the total for all iteration
         total_mutation_score += minimal_mutation_score_by_op
         total_test_cases += number_test_cases_by_op
         
         #update the seed
         seed += 1 

      #after the 10x execution save the total
      total_file.write(operator + "\n" + str(total_mutation_score)     + 
                                  "\n" + str(number_of_mutants_by_op)  + 
                                  "\n" + str(number_equivalents_by_op) + 
                                  "\n" + str(total_test_cases)         + "\n")

      
   #closing the files 
   total_file.close();
   for f in results_file_list:
      f.close()


   #control wheter we want to return the data to normal state after minimal set execution
   reset_data = False

   #reset the data to normal stage. eg:. all mutants and test cases selected, thus mutation score = 1.0
   if reset_data:

      #restore original data
      restore_original_session(program)

   print "I: Finish the execution for program: {}".format(program)	


# If this script is run as a program        
if __name__== "__main__":                       

   #enter inside the programs folder
   r = os.chdir('programs')

   #get the name of the programs
   programs_list = list_programs()

   #get all operators -> [usual_operators, deletion_operators, operators_set]
   operators_list = get_operators()



   for program in programs_list:

      print "############## {} ##############".format(program)

      # change to the program directory
      r = os.chdir(program)

      #run the experiment for a single program
      run_experiment(program, operators_list[2])

      #return back the the main program dir
      r = os.chdir("..")

      print "############## END ##############"
      print ''