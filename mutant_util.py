#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

#The method recives a vector with mutants 'Numbers' and converts to a string suitable to be used
#In the exemuta module
#SAMPLE: 
#mutantVector = ['4','8','45','57','61','66','254']
#string_mutant = mutant_string(mutantVector)
#statment = 'exemuta -select -x \"' + string_mutant + '\" ' + program
#Expected statment: exemuta -select -x "4 8 45 57 61 66 254" program  

def mutant_string(mutantVector):
    string_mutant = str(mutantVector)
    string_mutant = string_mutant[1:-1] #removing the '[]' of the vector from the string
    string_mutant = string_mutant.replace(',','') #removing ',' from the string
    string_mutant = string_mutant.replace('\'','') #removing ',' from the string    
    return string_mutant


"""
Used to define how retrive informations from de module "muta -l"
Require the use of one routine for capturing the shell output in a  variable.
Se the sample at the end of file
"""
def get_mutant(shell_output):

    start  = shell_output.find('#')
    start2 = shell_output.find('Operator:')
    start3 = shell_output.find('Status')
    start4 = shell_output.find('Causa')

    if start == -1:
        return None,0,0,0,0

    start_op     = shell_output.find('(', start2)  #begin of operator
    start_mutant = shell_output.find('# ', start)   #begin of mutant
    start_status = shell_output.find(' ',start3)   #begin of status
    start_causa  = shell_output.find(' - ',start4) #begin of causa mortis

    end_op   = shell_output.find('\n', start_op)     #end position for operator
    end_mutant = shell_output.find('\n', start_mutant) #end position for mutant
    end_status = shell_output.find('\n', start_status) #end position for status
    end_causa  = shell_output.find('\n', start_causa)  #end position for causa mortis

    mutant     = shell_output[start_mutant+1:end_mutant].strip() #retriving the mutant information
    operator     = shell_output[start_op+1:end_op-1].strip()       #retriving the operator information
    status     = shell_output[start_status+1:end_status].strip() #retriving the status information
    causa_mortis = shell_output[start_causa+3:end_causa].strip()   #retriving the causa mortis information

    return mutant,operator,status,causa_mortis, end_op



"""
Used to retrive all the information existent on "shellOutput" which was defined on "get_mutant"
In this case, return a hashtable where: key = Mutant Operator; Value = Mutants genereted by the operator
"""
def get_all_mutants(shell_output):

    mutants_status    = {} #This keeps a dictionary with some information for every mutant where: Key = Mutant index and Value contains some informations for that mutant
    mutants_by_operator = {} #This keeps a dictionary like where: Key = Operator and Value = List of mutants for that operator

    while True:

        mutant, operator, status, causa_mortis, end_op = get_mutant(shell_output)

        if mutant:

            mutants_status[mutant] = (status,causa_mortis,operator) #Populate the dict mutants_status

            if operator in mutants_by_operator:
                mutants_by_operator[operator].append(mutant) #If the Key 'Operator' already exists, add the mutant at the value of this key
            else:
                mutants_by_operator[operator] = [mutant] #Else, create a key and add the mutant to the vector of mutants relateds to that operator

            shell_output = shell_output[end_op:] #Refresh the content of the shellOutput

        else:
            break #When mutant is None the loop finish the read  of shell_output content

    return mutants_by_operator,mutants_status




def timedcall(fn, *args):
    "Call function with args; return the time in seconds and result"
    t0 = time.clock()
    result = fn(*args)
    t1 = time.clock()
    return t1-t0, result

def timedcalls(n,fn,*args):
    """Call function fn(*args) repeatedly: N times if N is an int, or up to N seconds if N is a float; 
    return the min, avg, and max time.
    """
    if isinstance(n,int):
        times = [timedcall(fn,*args)[0] for _ in range(n)]
    else:
        times = []
        while sum(times)<n:
            times.append(timedcall(fn,*args)[0])
    return min(times), average(times), max(times)

def average(numbers):
    "Return the average of a sequence of numbers"
    return sum(numbers)/float(len(numbers))





##SAMPLE#########
#import subprocess
#statement = 'muta -l -x "4 8 45 57 61 66 254" program 
#shellOutput = str(subprocess.check_output(statement, shell=True)) 

#Espected Shell Content in shellOutput is something like this:

"""MUTANT # 4
    Status Dead Active
    Causa Mortis: Stdout - Test Case 3
    Descriptor size.: 68
    Calling function starts at: 10069
    Called function starts at: -1
    Sequencial numbering: -1 6
    Last test case used: 9
    Operator: 33 (u-Cccr)
    Descriptor:
        Tipo: 1
        Program graph node: 3
        Offset: 10331, get out 43 characters
        Get on: ( ((m4 != 0) || ((m100 == 2) && (m400 != 0))) )

MUTANT # 8
    Status Dead Active
    Causa Mortis: Stdout - Test Case 4
    Descriptor size.: 68
    Calling function starts at: 10069
    Called function starts at: -1
    Sequencial numbering: -1 11
    Last test case used: 9
    Operator: 33 (u-Cccr)
    Descriptor:
        Tipo: 1
        Program graph node: 3
        Offset: 10331, get out 43 characters
        Get on: ( ((m4 != 0) || ((m100 == 0) && (m400 != 2))) )

MUTANT # 45
    Status Dead Active
    Causa Mortis: Stdout - Test Case 5
    Descriptor size.: 36
    Calling function starts at: 10069
    Called function starts at: -1
    Sequencial numbering: -1 4
    Last test case used: 9
    Operator: 35 (u-Ccsr)
    Descriptor:
        Tipo: 1
        Program graph node: 1
        Offset: 10178, get out 18 characters
        Get on: ( (1 == month1) )

MUTANT # 57
    Status Dead Active
    Causa Mortis: Stdout - Test Case 0
    Descriptor size.: 44
    Calling function starts at: 10069
    Called function starts at: -1
    Sequencial numbering: -1 16
    Last test case used: 9
    Operator: 35 (u-Ccsr)
    Descriptor:
        Tipo: 1
        Program graph node: 2
        Offset: 10203, get out 22 characters
        Get on:  (numDays = (day2 - 2)) ;

MUTANT # 61
    Status Dead Active
    Causa Mortis: Stdout - Test Case 1
    Descriptor size.: 64
    Calling function starts at: 10069
    Called function starts at: -1
    Sequencial numbering: -1 20
    Last test case used: 9
    Operator: 35 (u-Ccsr)
    Descriptor:
        Tipo: 1
        Program graph node: 3
        Offset: 10331, get out 43 characters
        Get on: ( ((0 != 0) || ((m100 == 0) && (m400 != 0))) )

MUTANT # 66
    Status Dead Active
    Causa Mortis: Stdout - Test Case 2
    Descriptor size.: 64
    Calling function starts at: 10069
    Called function starts at: -1
    Sequencial numbering: -1 25
    Last test case used: 9
    Operator: 35 (u-Ccsr)
    Descriptor:
        Tipo: 1
        Program graph node: 3
        Offset: 10331, get out 43 characters
        Get on: ( ((m4 != 0) || ((0 == 0) && (m400 != 0))) )

MUTANT # 254
    Status Dead Active
    Causa Mortis: Stdout - Test Case 7
    Descriptor size.: 40
    Calling function starts at: 10069
    Called function starts at: -1
    Sequencial numbering: -1 9
    Last test case used: 9
    Operator: 40 (u-OABN)
    Descriptor:
        Tipo: 1
        Program graph node: 6
        Offset: 10496, get out 15 characters
        Get on:  (i = (month1 | 1)) ;
"""