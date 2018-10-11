#!/usr/bin/env python
"""
Evaluate implementation of 1950 oxid file. For the moment
I'm just using the 1955 time for the existing oxid file rather 
than interpolating, so there's not much to check here.
"""

#IMPORT STUFF:
#======================
import numpy as np
import pylab as pl
from netCDF4 import Dataset

#ANALYZE THE ORIGINAL INPUTDATA FILE
#====================================
fo=Dataset('/global/project/projectdirs/acme/inputdata/atm/cam/chem/trop_mozart_aero/oxid/oxid_1.9x2.5_L26_1850-2015_c20171110.nc')

vars=['H2O2','HO2','NO3','O3','OH']

#note: lev is sigma pressure coordinates so top comes first.
#print 'levs are:',fo.variables['lev'][:]
#print 'lev units are:',fo.variables['lev'].units

t=fo.variables['date'][:]/1e4 #get year, using integer divide

for var in vars:
    vo=fo.variables[var]
    x=vo[0::12,vo.shape[1]/2,vo.shape[2]/2,-1]
    pl.figure()
    pl.plot(t[0::12],x)
    pl.title('Jan '+var)

    if var=='O3':
        pl.savefig('O3_jan_times.png')

#fo.close() #leave open for debugging.

#ANALYZE THE MODEL OUTPUT:
#===================================
#model output before making change
#f_orig=Dataset('/global/cscratch1/sd/petercal/ACME_simulations/edison.A_WCYCL1950.1850_test1.ne30_oECv3_ICG/run/edison.A_WCYCL1950.1850_test1.ne30_oECv3_ICG.cam.h0.0001-01-01-00000-rgr.nc')

f_orig=Dataset('/global/cscratch1/sd/petercal/ACME_simulations/edison.A_WCYCL1950.baseline.ne30_oECv3_ICG/run/edison.A_WCYCL1950.baseline.ne30_oECv3_ICG.cam.h0.0001-01-01-00000-rgr.nc')

#model output after making change
f_new=Dataset('/global/cscratch1/sd/petercal/ACME_simulations/edison.A_WCYCL1950.1950_oxid.ne30_oECv3_ICG/run/edison.A_WCYCL1950.1950_oxid.ne30_oECv3_ICG.cam.h0.0001-01-01-00000-rgr.nc')

#note: the SF (surf flux) variables 'SFH2O2','SFO3' are always zero so ignoring.

vars=['TMH2O2','OH','NO3','HO2','cnst_O3'] 
#Not in default output: 

lats=f_orig.variables['lat'][:]
lons=f_orig.variables['lon'][:]
LONS,LATS=pl.meshgrid(lons,lats)

for var in vars:
    vo=f_orig.variables[var]
    vn=f_new.variables[var]

    if len(vo[:].squeeze().shape)==3: #time,lat,lon
        pl.figure()
        pl.subplot(2,1,1)
        pl.pcolor(LONS,LATS,vo[-1])
        pl.colorbar()
        pl.title(var+' orig')

        pl.subplot(2,1,2)
        pl.pcolor(LONS,LATS,vn[-1])
        pl.colorbar()
        pl.title(var+' new')

    #if 3d, use lowest level.
    elif len(vo[:].squeeze().shape)==4: #time,lev,lat,lon
        pl.figure()
        pl.subplot(2,1,1)
        pl.pcolor(LONS,LATS,vo[-1,-1])
        pl.colorbar()
        pl.title(var+' orig: bot lev')

        pl.subplot(2,1,2)
        pl.pcolor(LONS,LATS,vn[-1,-1])
        pl.colorbar()
        pl.title(var+' new: bot lev')


    else:
        print "Don't know how to plot "+var+' w/ dims = '+str(len(vo[:].squeeze().shape))

#leave open for debugging.
#f_orig.close()
#f_new.close()




pl.show()

