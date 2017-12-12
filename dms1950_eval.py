#!/usr/bin/env python
"""
Test whether 1950 DMS file works.
"""

#IMPORT STUFF:
#=======================
from netCDF4 import Dataset
import pylab as pl
import numpy as np

#this is the original file
fo=Dataset('/project/projectdirs/acme/inputdata/atm/cam/chem/trop_mozart_aero/emis/DMSflux.1850.1deg_latlon_conserv.POPmonthlyClimFromACES4BGC_c20160416.nc')

#this is my new file
fn=Dataset('/global/cscratch1/sd/petercal/junk/CMIP6/DMSflux.1950.1deg_latlon_conserv.POPmonthlyClimFromACES4BGC_c20171210.nc')

#AUTOMATED CHECK OF ALL VARIABLES:
#=================================
for var in fo.variables.keys():
    try:
        df=np.sum(np.abs(fo.variables[var][:]-fn.variables[var][:]))
    except:
        print var+' in orig not found in new'

    if df<1e-16:
        print var+' is identical between old and new files.'
    else:
        shp=fo.variables[var].shape
        #if fits on line plot:
        if len(shp)==1: 
            pl.figure()
            pl.plot(fo.variables[var][:],'b-')
            pl.plot(fn.variables[var][:],'r--')
            pl.title(var+' b=orig, r=new')
        #if fits in pcolor
        elif len(shp)==2:
            pl.figure()
            pl.subplot(2,1,1)
            pl.pcolor(fo.variables[var][:])
            pl.title(var+' orig')
            pl.colorbar()
            pl.subplot(2,1,2)
            pl.pcolor(fn.variables[var][:])
            pl.title(var+' new')
            pl.colorbar()
        elif var=='DMS':
            pl.figure()
            lat=fo.variables['lat'][:]
            lon=fo.variables['lon'][:]
            LON,LAT=pl.meshgrid(lon,lat)
            pl.subplot(2,1,1)
            pl.pcolor(LON,LAT,np.average(fo.variables[var][:],axis=0).squeeze())
            pl.colorbar()
            pl.title(var+' orig')

            pl.subplot(2,1,2)
            pl.pcolor(LON,LAT,np.average(fn.variables[var][:],axis=0).squeeze())
            pl.colorbar()
            pl.title(var+' new')

            pl.figure()
            ind=0
            while fo.variables[var][:].mask[0,ind,ind]==True:
                ind+=1
            pl.plot(fo.variables[var][:,ind,ind])
            pl.plot(fn.variables[var][:,ind,ind],'r--')
            pl.title('DMS for 1 loc, blue=old, red=new')
            
        else:
            print var+' has too many dims to plot easily'

pl.show()
