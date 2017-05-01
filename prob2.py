# -*- coding: utf-8 -*-
"""
TDI Challenge
Question #2

My assumptions about some ambiguities:
    1. Assuming that the data for the academic years 2013-2014 is for "2013 admittees".
        - This is my stupid ambiguity. I am confused for choosing which of 12-13 and 13-14 data is correct for the question's "2013 only",
        though it is very much likely that the 13-14 data is for the question's "2013 only". 
    2. For the ethnicity problem, I do not count non-resident aliens or unknowns, 
        considering white, black, hispanic, asian, native american, hwaiian, and 2more.  

Comments : 
        - caluations of the required statistics are simple and straight-forward for Q2, as you know. 
        Most of time is spent on reading the manual of data description to identify 
        which columns are appropriate for solving each problem. 

        - this script is written, tested, and run in ipython on the Spyder-IDE. 
        
        
@author: shong
"""

import numpy as np
import pickle


"""
###############################
# read headers and rawbodies 
# and save them as a pickle binary
with open('MERGED2013_14_PP.csv','r') as f:
    tmpline = f.readline()
    #print headers
    headers = tmpline.split(',')
    
    rawdata = f.readlines()

# save data as a pickle for easier readouts in the future analyses
with open('data13to14.pickle','wb') as fp:
    pickle.dump([headers,rawdata],fp)
###############################
"""


with open('data13to14.pickle') as fp:
    headers, rawdata = pickle.load(fp)

lenheaders = len(headers)
lenrawdata = len(rawdata)
print lenheaders, lenrawdata



# find which columns are for HIGHDEG, SAT_AVG, etc
isat = -1
ideg = -1
ilevel = -1 
iugds = -1
for i in range(0,lenheaders):
    if headers[i] == 'SAT_AVG':
        isat = i
    if headers[i] == 'HIGHDEG':
        ideg = i
    if headers[i] == 'ICLEVEL':
        ilevel = i
    if headers[i] == 'UGDS':
        iugds = i
print isat, ideg, ilevel, iugds      
print headers[isat], headers[ideg], headers[ilevel], headers[iugds]




# read SAT_AVG, HIGHDEG, etc. values as generic objects
strsatscores = np.empty(lenrawdata,dtype=object)
strdegflag = np.empty(lenrawdata,dtype=object)
strlevelflag = np.empty(lenrawdata,dtype=object)
strugds = np.empty(lenrawdata,dtype=object)


for i in range(0,lenrawdata):
    thisdata = rawdata[i].split(',')
    #print thisdata[isat]
    strsatscores[i] = thisdata[isat]
    strdegflag[i] = thisdata[ideg]
    strlevelflag[i] = thisdata[ilevel]
    strugds[i] = thisdata[iugds]
    #print strsatscores[i], strdegflag[i], strlevelflag[i],strugds[i]
   


#########################################
#Problem [1] : Find the average SAT score

print ">>> Problem #1 >>>"   
# locate valid indices 
badflag = np.zeros(lenrawdata,dtype=int)

ifail = np.where(strsatscores == 'NULL')
badflag[ifail] += 1
ifail = np.where(strdegflag != '4') # only HIHGDEG == 4
badflag[ifail] += 1

for i in range(len(badflag)): # add badflags if data are None
    if (strsatscores[i] == None or strdegflag[i] == None or strugds[i] == None):
        badflag[i] += 1

#print badflag

ivalid = np.where(badflag == 0)
ifail = np.where(badflag > 0)
#print strsatscores[ivalid], strdegflag[ivalid], strugds[ivalid]

satscores = strsatscores[ivalid].astype(np.double)
degflag = strdegflag[ivalid].astype(np.int) # sanity check for HIGHDEG==4 
numstudents = strugds[ivalid].astype(np.double)
approxnum = numstudents/4.0
#print len(satscores), len(degflag), len(numstudents)

numvalid = len(satscores)
totsat = np.double(0.0)
totstudent = np.double(0.0)

for i in range(numvalid):
    totsat += satscores[i]*approxnum[i]
    totstudent += approxnum[i]

finalMeanSAT = totsat/totstudent 

print "mean sat score = ", finalMeanSAT


##############################################
#Problem [2] : Pearson Correlation Coefficient
iwdy2 = -1
isat = -1 # redundant process

for i in range(0,lenheaders):
    if headers[i] == 'WDRAW_ORIG_YR2_RT':
        iwdy2 = i
    if headers[i] == 'SAT_AVG': # redundant
        isat = i
#print iwdy2     
print ">>> Problem #2 >>>"
print headers[isat], headers[iwdy2]

rawsat = np.empty(lenrawdata,dtype=object)
rawwd = np.empty(lenrawdata,dtype=object)

for i in range(0,lenrawdata):
    thisdata = rawdata[i].split(',')
    #print thisdata[isat]
    rawsat[i] = thisdata[isat]
    rawwd[i] = thisdata[iwdy2]

    print rawsat[i], rawwd[i]

# locate valid indices, again
badflag = np.zeros(lenrawdata,dtype=int)

ifail = np.where(rawsat == 'NULL')
badflag[ifail] += 1
ifail = np.where(rawwd == 'NULL')
badflag[ifail] += 1
ifail = np.where(rawwd == 'PrivacySuppressed')
badflag[ifail] += 1

#print badflag
ivalid = np.where(badflag == 0)
ifail = np.where(badflag > 0)
#print rawsat[ivalid]
#print rawwd[ivalid]
#print rawsat[ifail]
#print rawwd[ifail]


sat = rawsat[ivalid].astype(np.double)
wd = rawwd[ivalid].astype(np.double)
enroll = 1.0 - wd
lendata = len(sat)
#print len(sat), len(wd)

# plot the data for sanity checks
import matplotlib.pyplot as plt
plt.rc('font', family='serif') 
plt.rc('font', serif='Times New Roman') 
plt.rcParams.update({'font.size': 18})
fig = plt.figure(figsize=(5,5))
plt.xlabel(r'SAT Score')
plt.ylabel(r'Fraction of Enrollments after 2 years')
plt.scatter(sat,enroll,marker='x',color='g',s=10)
plt.show()

# Pearson Coeff
from scipy.stats.stats import pearsonr
print "Pearson Correlation Coefficient : ",pearsonr(sat,enroll)


##############################################
#Problem [3] : the most diverse institute 
#comments : non-alien residents and unknowns are not counted as ethnicity

print ">>> Problem #3 : the most diverse university" 
iwhite, iblack, ihisp, iasian, inative, ihawaii, imore = -1,-1,-1,-1,-1,-1,-1
for i in range(lenheaders):
    if headers[i] == 'UGDS_WHITE':
        iwhite = i
    if headers[i] == 'UGDS_BLACK':
        iblack = i
    if headers[i] == 'UGDS_HISP':
        ihisp = i
    if headers[i] == 'UGDS_ASIAN':
        iasian = i
    if headers[i] == 'UGDS_AIAN':
        inative = i
    if headers[i] == 'UGDS_NHPI':
        ihawaii = i
    if headers[i] == 'UGDS_2MOR':
        imore = i

#print headers[iwhite],headers[iblack],headers[ihisp],headers[iasian]
#print headers[inative],headers[ihawaii],headers[imore]

rawwhite = np.empty(lenrawdata,dtype=object)
rawblack = np.empty(lenrawdata,dtype=object)
rawhisp = np.empty(lenrawdata,dtype=object)
rawasian = np.empty(lenrawdata,dtype=object)
rawnative = np.empty(lenrawdata,dtype=object)
rawhawaii = np.empty(lenrawdata,dtype=object)
rawmore = np.empty(lenrawdata,dtype=object)

for i in range(lenrawdata):
    thisdata = rawdata[i].split(',')
    
    rawwhite[i] = thisdata[iwhite]
    rawblack[i] = thisdata[iblack]
    rawhisp[i] = thisdata[ihisp]
    rawasian[i] = thisdata[iasian]
    rawnative[i] = thisdata[inative]
    rawhawaii[i] = thisdata[ihawaii]
    rawmore[i] = thisdata[imore]

    print rawwhite[i], rawblack[i], rawmore[i]


# locate valid indices, again
badflag = np.zeros(lenrawdata,dtype=int)

ifail = np.where(rawwhite == 'NULL')
badflag[ifail] += 1
ifail = np.where(rawblack == 'NULL')
badflag[ifail] += 1
ifail = np.where(rawhisp == 'NULL')
badflag[ifail] += 1
ifail = np.where(rawasian == 'NULL')
badflag[ifail] += 1
ifail = np.where(rawnative == 'NULL')
badflag[ifail] += 1
ifail = np.where(rawhawaii == 'NULL')
badflag[ifail] += 1
ifail = np.where(rawmore == 'NULL')
badflag[ifail] += 1

ifail = np.where(rawwhite == '0')
badflag[ifail] += 1
ifail = np.where(rawblack == '0')
badflag[ifail] += 1
ifail = np.where(rawhisp == '0')
badflag[ifail] += 1
ifail = np.where(rawasian == '0')
badflag[ifail] += 1
ifail = np.where(rawnative == '0')
badflag[ifail] += 1
ifail = np.where(rawhawaii == '0')
badflag[ifail] += 1
ifail = np.where(rawmore == '0')
badflag[ifail] += 1

# sanity check
print badflag[:20]
for i in range(20):
    print rawwhite[i], rawblack[i], rawhisp[i], rawasian[i],\
        rawnative[i], rawhawaii[i], rawmore[i]

ivalid = np.where(badflag == 0)
ifail = np.where(badflag > 0)

# trim data and do maths
white = rawwhite[ivalid].astype(np.double)
black = rawblack[ivalid].astype(np.double)
hisp = rawhisp[ivalid].astype(np.double)
asian = rawasian[ivalid].astype(np.double)
native = rawnative[ivalid].astype(np.double)
hawaii = rawhawaii[ivalid].astype(np.double)
mores = rawmore[ivalid].astype(np.double)

lendata = len(white)
print lendata

ethnicMetric = np.zeros(lendata)

for i in range(lendata):
    mostrep = np.max([white[i],black[i],hisp[i],asian[i],\
                    native[i],hawaii[i],mores[i]])
    leastrep = np.min([white[i],black[i],hisp[i],asian[i],\
                    native[i],hawaii[i],mores[i]])
                    
    ethnicMetric[i] = np.abs(mostrep - leastrep)


# sanity check
for i in range(100):
    print white[i], black[i], hisp[i], asian[i],\
        native[i], hawaii[i], mores[i], ethnicMetric[i]

# Final answer
print ">>> the minimum Ethnic Metric = ", np.min(ethnicMetric)

# Inspect the result, since it is odd
i = np.argmin(ethnicMetric)
print white[i], black[i], hisp[i], asian[i],\
        native[i], hawaii[i], mores[i], ethnicMetric[i]
# the majority fraction of white students is 0.1873 ?
# So.. most of students are unknown?








##############################################
#Problem [4] : Completion Difference by Family Income
icomp = -1
icompt = -1
ifaminc = -1
iindinc = -1
ihigh = -1

for i in range(lenheaders):
    if headers[i] == 'COMP_ORIG_YR4_RT':
        icomp = i
    if headers[i] == 'FAMINC':
        ifaminc = i
    if headers[i] == 'FAMINC_IND':
        iindinc = i
print ">>> Problem #3 >>>"
print headers[icomp], headers[ifaminc], headers[iindinc]


rawcomp = np.empty(lenrawdata,dtype=object)
rawfaminc = np.empty(lenrawdata,dtype=object)
rawindinc = np.empty(lenrawdata,dtype=object)
for i in range(lenrawdata):
    thisdata = rawdata[i].split(',')
    #print thisdata[isat]
    rawcomp[i] = thisdata[icomp]
    rawfaminc[i] = thisdata[ifaminc]
    rawindinc[i] = thisdata[iindinc]

    print rawcomp[i], rawfaminc[i], rawindinc[i]








