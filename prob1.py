# -*- coding: utf-8 -*-
"""
TDI challenge
Problem #1

comments : 
        - notorious N Factorial complexity
        - this script is written, tested, and run in ipython on the Spyder-IDE. 
 
@author: shong
"""
import itertools as itt
import numpy as np

def getSalary(coins):
    salary = np.int(0)
    lencoins = len(coins)
    
    salary += coins[0]
    for i in range(1,lencoins):
        salary += np.abs(coins[i-1] - coins[i])
    
    return salary

"""
######### N = 10 ##########    
The crazy O(N!) 
But we can find the exact solution for this small N=10.
"""
#Define Coins and Set Parameters

numcoins = 10
thresholdSalary = 45
coins = np.arange(1,numcoins+1, dtype=np.int)
lendata = len(coins) #lendata == numcoins


cperm = np.zeros(lendata, dtype=np.int)
totalSalary = np.double(0.0)
totalSalarySquare = np.double(0.0)
thisSalary = np.double(0.0)
thisSalaryInt = np.int(0)
numPerm = np.double(0.0)
numHighSalary = np.double(0.0)

# Do maths
for cperm in itt.permutations(coins):
    #print cperm
    #print getSalary(cperm)
    thisSalaryInt = getSalary(cperm)
    #thisSalaryInt = getSalaryReverse(cperm)    
    if thisSalaryInt >= thresholdSalary:
        #print thisSalaryInt,"/",thresholdSalary
        numHighSalary += np.double(1.0)
    
    thisSalary = np.double(thisSalaryInt)
    totalSalary += thisSalary
    totalSalarySquare += thisSalary*thisSalary
    numPerm += np.double(1.0)
    
    
print "coins = ",coins
print "    numPerm = ",numPerm
print "    numHighSalary = ",numHighSalary
print "    totalSalary = ",totalSalary
print "    totalSalarySquare = ",totalSalarySquare

meanSalary = totalSalary/numPerm
stddevSalary = totalSalarySquare/numPerm
stddevSalary = np.sqrt(stddevSalary - meanSalary*meanSalary)

print "Mean Salary = ",meanSalary
print "Std Salary = ",stddevSalary
print "HighSalary Fraction = ",numHighSalary/numPerm





"""
############ N = 20 #############
The crazy O(N!) 

We can't sample the whole permutations in our life time. 

A quick and dirty approximation would be random permutation sequences, 
by assuming there is no significant duplications in the generated sequences. 

The code below follows this quick and dirty rule. 


"""

numcoins = 20
thresholdSalary = 160
coins = np.arange(1,numcoins+1, dtype=np.int)
lendata = len(coins) #lendata == numcoins


cperm = np.zeros(lendata, dtype=np.int)
totalSalary = np.double(0.0)
totalSalarySquare = np.double(0.0)
thisSalary = np.double(0.0)
thisSalaryInt = np.int(0)
numPerm = np.double(0.0)
numHighSalary = np.double(0.0)

printingCounter = np.int(0)

print "coins = ",coins
# Do maths
# Since O(N!),keep printing on-the-fly results, with watching over the convergence within the precision
while totalSalarySquare < np.infty: # virtually, infinite loop
    cperm = np.random.permutation(coins) # this numpy.random uses MT19937; hence, less affected by the finite cyclic period of pseudo-random generator
    #print cperm
    #print getSalary(cperm)
    thisSalaryInt = getSalary(cperm) #reverse sum to remove the permutation bias, caused by the first coin rule
    if thisSalaryInt >= thresholdSalary:
        #print thisSalaryInt,"/",thresholdSalary
        numHighSalary += np.double(1.0)
    
    thisSalary = np.double(thisSalaryInt)
    totalSalary += thisSalary
    totalSalarySquare += thisSalary*thisSalary
    numPerm += np.double(1.0)
    printingCounter += 1

    # On-the-fly prints     
    if printingCounter == 10000000 :
        printingCounter = 0
        print "    numPerm = ",numPerm
        print "    numHighSalary = ",numHighSalary
        print "    totalSalary = ",totalSalary
        print "    totalSalarySquare = ",totalSalarySquare

        meanSalary = totalSalary/numPerm
        stddevSalary = totalSalarySquare/numPerm
        stddevSalary = np.sqrt(stddevSalary - meanSalary*meanSalary)

        print "Mean Salary = ",meanSalary
        print "Std Salary = ",stddevSalary
        print "HighSalary Fraction = ",numHighSalary/numPerm



