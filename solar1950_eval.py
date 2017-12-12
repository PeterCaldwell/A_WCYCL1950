#!/usr/bin/env python
"""
Compare model output before and after updating 
solar file.
"""

#IMPORT STUFF:
#=======================
from netCDF4 import Dataset
import pylab as pl
import numpy as np

#COMPARE MODEL OUTPUT:
#=======================
f_orig=Dataset('/global/cscratch1/sd/petercal/ACME_simulations/edison.A_WCYCL1950.1850_test1.ne30_oECv3_ICG/run/edison.A_WCYCL1950.1850_test1.ne30_oECv3_ICG.cam.h0.0001-01-01-00000-rgr.nc')

f_new=Dataset('/global/cscratch1/sd/petercal/ACME_simulations/edison.A_WCYCL1950.1950_aero4.ne30_oECv3_ICG/run/edison.A_WCYCL1950.1950_aero4.ne30_oECv3_ICG.cam.h0.0001-01-01-00000-rgr.nc')

x_old=f_orig.variables['SOLIN']
x_new=f_new['SOLIN']

lat=f_orig.variables['lat'][:]
lon=f_orig.variables['lon'][:]
LON,LAT=pl.meshgrid(lon,lat)

if x_old.shape[0]!=x_new.shape[0]:
    raise Exception('time dim of variables differs between runs')

pl.figure(1)
pl.subplot(2,1,1)
pl.pcolor(LON,LAT,x_old[-1].squeeze())
pl.colorbar()
pl.title('old')

pl.subplot(2,1,2)
pl.pcolor(LON,LAT,x_new[-1].squeeze())
pl.colorbar()
pl.title('new')

pl.savefig('SOLIN-1950-CMIP6.png')

#COMPARE MODEL INPUT:
#====================
fo=Dataset('/project/projectdirs/acme/inputdata/atm/cam/solar/Solar_1850control_input4MIPS_c20171101.nc')
#fn=Dataset('/global/cscratch1/sd/petercal/junk/CMIP6/Solar_1950control_input4MIPS_c20171208.nc')
fn=Dataset('/project/projectdirs/acme/inputdata/atm/cam/solar/Solar_1950control_input4MIPS_c20171208.nc')

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
        else:
            print var+' has too many dims to plot easily'

pl.show()
