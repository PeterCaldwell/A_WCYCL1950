#!/usr/bin/env python
"""
Test whether 1950 DMS file works.
"""

#IMPORT STUFF:
#=======================
from netCDF4 import Dataset
import pylab as pl
import numpy as np

#COMPARE OLD AND NEW MODEL OUTPUT
#====================================
#model output before making DMS change
f_orig=Dataset('/global/cscratch1/sd/petercal/ACME_simulations/edison.A_WCYCL1950.1850_test1.ne30_oECv3_ICG/run/edison.A_WCYCL1950.1850_test1.ne30_oECv3_ICG.cam.h0.0001-01-01-00000-rgr.nc')

#model output after making DMS change
f_new=Dataset('/global/cscratch1/sd/petercal/ACME_simulations/edison.A_WCYCL1950.1950_dms2.ne30_oECv3_ICG/run/edison.A_WCYCL1950.1950_dms2.ne30_oECv3_ICG.cam.h0.0001-01-01-00000-rgr.nc')


vars=['SFDMS','DMS_SRF','AQ_DMS','DF_DMS']

for var in vars:
    vo=f_orig.variables[var]
    vn=f_new.variables[var]

    lats=f_orig.variables['lat'][:]
    lons=f_orig.variables['lon'][:]
    LONS,LATS=pl.meshgrid(lons,lats)

    if len(vo[:].squeeze().shape)==3: #time,lat,lon
        pl.figure()
        pl.subplot(2,1,1)
        pl.pcolor(LONS,LATS,vo[-1])
        pl.colorbar()
        pl.title(vo.long_name+' orig')

        pl.subplot(2,1,2)
        pl.pcolor(LONS,LATS,vn[-1])
        pl.colorbar()
        pl.title(vn.long_name+' new')

        if var=='SFDMS':
            pl.savefig(var+'.png')

    else:
        print "Don't know how to plot "+var+' w/ dims = '+str(len(vo[:].squeeze().shape))

#leave open for debugging.
#f_orig.close()
#f_new.close()


#COMPARE OLD AND NEW INPUTDATA FILES:
#=====================================
#this is the original inputdata file
fo=Dataset('/project/projectdirs/acme/inputdata/atm/cam/chem/trop_mozart_aero/emis/DMSflux.1850.1deg_latlon_conserv.POPmonthlyClimFromACES4BGC_c20160416.nc')

#this is my new inputdata file
fn=Dataset('/global/cscratch1/sd/petercal/junk/CMIP6/DMSflux.1950.1deg_latlon_conserv.POPmonthlyClimFromACES4BGC_c20171210.nc')

#AUTOMATED CHECK OF ALL VARIABLES:
#---------------------------------
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
