#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import math
import pdb

from programs import list_programs


def compute_minimal_set(program):

    print "I: Computing the minimal set of mutants"
            
    statement = "report -trace -L 2 " + program
    os.system(statement)
    report = program+".trc"
    repfile = open(report, "r")
    cont = -2
    mutants = [] # list of mutants still to analyze
    hashset = dict()
    for line in repfile:
        if (cont < 0 or line.find("TOTAL") >= 0):
            cont += 1
            continue
        tcLine = line.split()
        #print line
        #print tcLine
        s =  set()
        i = 0
        for tc in tcLine:
            k = int(tc)
            if ( k > 1 and k < 6 ): # mutant is dead
                s.add(i)  # tc is includeed in teh mutant set
            i += 1
        if (len(s) > 0): # equiv mutants have size 0
            hashset[cont] = s
            mutants.append(cont)
        cont += 1
    # at this point each mutant has an entry in the list mutants
    # and in the hashset variable. hashset holds the test cases
    # that kill each mutant
    
    before = len(mutants)
    counter = dict()
    
    #print program + " had " + str(before) + " mutants ",
    for m in mutants[:]:
        if ( not hashset.has_key(m)):
            continue
        s = hashset[m]
        counter[m] = 0
        remove = set()
        for m2 in mutants[:]:
            if (m2 == m):
                continue
            if ( not hashset.has_key(m2)):
                continue
            s2 = hashset[m2]
            if (s <= s2): #m subsumes m2 -> (Change <= by < includes all minimal candidates)
                #print "Mutant " + str(m) + " subsumes "  + str(m2)
                #print s
                #print s2
                remove.add(m2)
                counter[m] = counter[m] + 1
        for m2 in remove:
            mutants.remove(m2)
            hashset.pop(m2)
    after = len(mutants)
    #print "ended with " + str(after) +  " (" + "%5.2f" % (float(after)/ float(before) * 100.0) + "%)"
    
    minFile = open("minimal.txt", "w")
    for m in mutants:
        minFile.write(str(m) + " ")
    minFile.close()

    soma = 0.0
    max = 0
    min = 1000000
    # this is number of test cases that kill each mutant
    minFile = open("minimal-sizes.txt", "w")
    for m in mutants:
        s = len(hashset[m])
        soma += s
        if (s < min):
            min = s
        if (s > max):
            max = s
        minFile.write(str(m) + " " + str(s) + "\n")
    minFile.write("Min: "+ str(min)+ "\n") 
    minFile.write("Max: "+ str(max)+ "\n")
    minFile.write("Avg: "+ str(soma/float(len(mutants))) + "\n")
    minFile.close()

    soma = 0.0
    max = 0
    min = 1000000
    # this is number of mutants subsumed by each minimal mutant
    minFile = open("minimal-subsume-sizes.txt", "w")
    for m in mutants:
        s = counter[m]
        soma += s
        if (s < min):
            min = s
        if (s > max):
            max = s
        minFile.write(str(m) + " " + str(s) + "\n")
    minFile.write("Min: "+ str(min)+ "\n") 
    minFile.write("Max: "+ str(max)+ "\n")
    minFile.write("Avg: "+ str(soma/float(len(mutants))) + "\n")
    minFile.close()
   
    return mutants



if __name__=="__main__":                       # If this script is run as a program:

    r = os.chdir('programs')

    programs_list = list_programs()

    for program in programs_list:

        #enter the dir
        r = os.chdir(program)
        
        #compute minimal set
        compute_minimal_set(program)    
        
        #Return to the root of the programs to open the next one.
        r = os.chdir("..")