# -*- coding: utf-8 -*-
"""
TDI Challenge
Question #3

Proposed Project:




@author: shong
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


"""
Airports, Stations, and Seaports data

source : http://openflights.org/data.html
"""

idnum, lat, lon, alt, iden = np.loadtxt('airports-extended.dat',delimiter=',', usecols=(0,6,7,8,12),dtype=object, unpack=True)

iden = iden.astype(str)
iairport = np.where(iden == '"airport"')
iseaport = np.where(iden == '"port"')
istation = np.where(iden == '"station"')
#print len(iairport[0]), len(iseaport[0]), len(istation[0]), len(idnum)


## Trim the data for each kind
idair = idnum[iairport].astype(np.int)
lonair = lon[iairport].astype(np.double)
latair = lat[iairport].astype(np.double)
altair = alt[iairport].astype(np.double)

idsea = idnum[iseaport].astype(np.int)
lonsea = lon[iseaport].astype(np.double)
latsea = lat[iseaport].astype(np.double)
altsea = alt[iseaport].astype(np.double)

idstat = idnum[istation].astype(np.int)
lonstat = lon[istation].astype(np.double)
latstat = lat[istation].astype(np.double)
altstat = alt[istation].astype(np.double)



### Plot data on the Earth
plt.rc('font', family='serif') 
plt.rc('font', serif='Times New Roman') 
plt.rcParams.update({'font.size': 18})
fig = plt.figure(figsize=(15,15))
# setup Lambert Conformal basemap.
# set resolution=None to skip processing of boundary datasets.
map = Basemap(projection='mill',llcrnrlat=-80,urcrnrlat=80,\
            llcrnrlon=-180,urcrnrlon=180,resolution='c')
#m.drawcoastlines(color)
map.fillcontinents(color='grey',lake_color='white',alpha=0.2)
# draw parallels and meridians.
#m.drawparallels(np.arange(-90.,91.,30.))
#m.drawmeridians(np.arange(-180.,181.,60.))
map.drawmapboundary(fill_color='white')

ax, ay = map(lonair,latair)
map.scatter(ax, ay,color='g', marker='o',s=10)

tx, ty = map(lonstat,latstat)
map.scatter(tx, ty,color='coral', marker='o',s=10)


sx, sy = map(lonsea,latsea)
map.scatter(sx, sy,color='b', marker='o',s=10)


plt.title("Airports, Train Stations, and Seaports")
plt.savefig('geolocations.png')
plt.show()




"""
Urbanization Data 

source : http://openflights.org/data.html
"""
# read headers and rawbodies 
# and save them as a pickle binary
with open('urbanizationUS.csv','r') as f:
    tmpline = f.readline()
    tmpline = tmpline.strip()
    #print headers
    headers = tmpline.split(',')
    
    rawdata = f.readlines()

numheaders = len(headers)
numcities = len(rawdata)
print numheaders, numcities

rawnames = np.empty(numcities,dtype=object)
rawlons = np.empty(numcities,dtype=object)
rawlats = np.empty(numcities,dtype=object)
earlypop = np.empty(numcities,dtype=np.int) # AD_1000 - AD_1800
midpop = np.empty(numcities,dtype=np.int)   # AD_1800 - AD_1920
latepop = np.empty(numcities,dtype=np.int)  # AD_1920 - AD_1975


# headers[108] = AD_1000
# headers[683] = AD_1800
# headers[792] = AD_1920
# headers[808] = AD_1950 
for i in range(numcities):
    thisline = rawdata[i].strip()
    thisdata = thisline.split(',')
    #print thisdata
    rawnames[i] = thisdata[0]
    rawlats[i] = thisdata[3]
    rawlons[i] = thisdata[4]
    
    maxearlypop = -1
    maxmidpop = -1
    maxlatepop = -1
    for k in range(108,len(thisdata)):
        currentpop = 0
        if thisdata[k] != '':
            #print thisdata[k]
            currentpop = np.int(thisdata[k])
        #print currentpop

        if k < 683:
            if maxearlypop < currentpop:
                maxearlypop = currentpop
        if k >= 683 and k < 792:
            if maxmidpop < currentpop:
                maxmidpop = currentpop
        if k >= 792:
            if maxlatepop < currentpop:
                maxlatepop = currentpop
    #print maxearlypop, maxmidpop, maxlatepop
    
    earlypop[i] = maxearlypop
    midpop[i] = maxmidpop
    latepop[i] = maxlatepop
    
# remove the bugging \xa0 character
rawlonsstr = rawlons.astype(str)
lenlons = len(rawlonsstr)
for i in range(lenlons):
    rawlonsstr[i] = rawlonsstr[i].replace('\xa0', '')



## final useful data, plus pop data above
lats = rawlats.astype(np.double)
lons = rawlonsstr.astype(np.double)
names = rawnames.astype(str)


## locate the cities for each urbanization epoch
iearly = np.where(earlypop > 0)
imid = np.where(midpop > 0)
ilate = np.where(latepop > 0)

#print lons[iearly],earlypop[iearly]
#print lons[imid],midpop[imid]
#print lons[ilate],latepop[ilate]






### Plot data on the Earth
plt.rc('font', family='serif') 
plt.rc('font', serif='Times New Roman') 
plt.rcParams.update({'font.size': 18})
fig = plt.figure(figsize=(10,18))

######
plt.subplot(311)
plt.title("Seaports vs. Urbanized Cities AD1000-1800 ")

map = Basemap(projection='mill',llcrnrlat=22,urcrnrlat=55,\
            llcrnrlon=-130,urcrnrlon=-60,resolution='c')
#m.drawcoastlines(color)
map.fillcontinents(color='grey',lake_color='blue',alpha=0.2)
# draw parallels and meridians.
#m.drawparallels(np.arange(-90.,91.,30.))
#m.drawmeridians(np.arange(-180.,181.,60.))
map.drawmapboundary(fill_color='white')

#ax, ay = map(lonair,latair)
#map.scatter(ax, ay,color='g', marker='.',s=20, alpha=0.5)
#tx, ty = map(lonstat,latstat)
#map.scatter(tx, ty,color='coral', marker='.',s=20, alpha=0.5)

sx, sy = map(lonsea,latsea)
map.scatter(sx, sy,color='b', marker='o',s=20, alpha=0.5)

ex, ey = map(lons[iearly],lats[iearly])
map.scatter(ex, ey,color='b', marker='x',s=80, alpha=0.9)

########
plt.subplot(312)
plt.title("Train Stations vs. Urbanized Cities AD1800-1920 ")

map = Basemap(projection='mill',llcrnrlat=22,urcrnrlat=55,\
            llcrnrlon=-130,urcrnrlon=-60,resolution='c')
#m.drawcoastlines(color)
map.fillcontinents(color='grey',lake_color='blue',alpha=0.2)
# draw parallels and meridians.
#m.drawparallels(np.arange(-90.,91.,30.))
#m.drawmeridians(np.arange(-180.,181.,60.))
map.drawmapboundary(fill_color='white')

#ax, ay = map(lonair,latair)
#map.scatter(ax, ay,color='g', marker='.',s=20, alpha=0.5)

tx, ty = map(lonstat,latstat)
map.scatter(tx, ty,color='coral', marker='o',s=20, alpha=0.5)


#sx, sy = map(lonsea,latsea)
#map.scatter(sx, sy,color='b', marker='.',s=20, alpha=0.5)


mx, my = map(lons[imid],lats[imid])
map.scatter(mx, my,color='coral', marker='x',s=80, alpha=0.9)

#########
plt.subplot(313)
plt.title("Airports vs. Urbanized Cities AD1920-1970 ")

map = Basemap(projection='mill',llcrnrlat=22,urcrnrlat=55,\
            llcrnrlon=-130,urcrnrlon=-60,resolution='c')
#m.drawcoastlines(color)
map.fillcontinents(color='grey',lake_color='blue',alpha=0.2)
# draw parallels and meridians.
#m.drawparallels(np.arange(-90.,91.,30.))
#m.drawmeridians(np.arange(-180.,181.,60.))
map.drawmapboundary(fill_color='white')

ax, ay = map(lonair,latair)
map.scatter(ax, ay,color='g', marker='.',s=20, alpha=0.5)

#tx, ty = map(lonstat,latstat)
#map.scatter(tx, ty,color='coral', marker='.',s=20, alpha=0.5)

#sx, sy = map(lonsea,latsea)
#map.scatter(sx, sy,color='b', marker='.',s=20, alpha=0.5)

lx, ly = map(lons[ilate],lats[ilate])
map.scatter(lx, ly,color='g', marker='x',s=120, alpha=0.9)



plt.savefig('urbanization.png')
plt.show()







