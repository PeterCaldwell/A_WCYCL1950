#!/usr/bin/env python
"""
Take E3SM 1850 solar input file and modify it for 1950 by:

1. changing times, calyear, calmonth, calday, and date from 1850 to 1950
2. strip variables with plev and glat dimensions because 
   these don't exist in the TR file on inputs4mips so I don't 
   know what values to use for 1950. Will test empirically that 
   these vars aren't needed by the model.
3. replace ssi, tsi, ssn, ap, kp, and f107 with the average over all 
   monthly values from 1950+/-11 yrs.

Note that E3SM solar input file differs from the input4mips version by:
1. has 2 times rather than 1.
2. uses dimension 'wavelength' instead of 'wlen'
3. variable 'wlenbinsize' has been converted to 'band_width'

This routine borrows from ~/py/acme/tr2seas.py
"""

#IMPORT STUFF:
#==============
import numpy as np
import pylab as pl
from netCDF4 import Dataset
import time

#USER-SPECIFIED STUFF:
#==============
start_yr=1939
end_yr=1962 #will take all times up to but not including end_yr
user='Peter Caldwell'
titl='Solar input for 1950 control simulation computed as average from 1939 through the end of 1951 of solarforcing-ref-mon_input4MIPs_solar_CMIP_SOLARIS-HEPPA-3-2_gn_18500101-22991231.nc. Time info and variables without a time dimension are taken directly from Solar_1850control_input4MIPS_c20171101.nc (note the time/date info is not correct in this file since it is not correct in the 1850 control file either.'

#this is the 1850 file I'll basically copy.
in_file = '/global/project/projectdirs/acme/inputdata/atm/cam/solar/Solar_1850control_input4MIPS_c20171101.nc'

#this is the 1950 file we're creating here.
out_file = '/global/cscratch1/sd/petercal/junk/CMIP6/Solar_1950control_input4MIPS_c20'+time.strftime('%y%m%d')+'.nc'

#this is the transient file we get data from.
#It is version '20170103' downloaded from https://esgf-node.llnl.gov/search/input4mips/
data_file = '/global/cscratch1/sd/petercal/junk/CMIP6/solarforcing-ref-mon_input4MIPs_solar_CMIP_SOLARIS-HEPPA-3-2_gn_18500101-22991231.nc'

#skip stuff refers to variables I want to remove entirely from output file
skip_dims=['plev','glat'] #don't have transient info for related vars.
skip_vars=skip_dims+['glat_bnds','iprp','iprg','iprm']

#time_vars refers to variables that include the time dimension, but which 
#have 1850 values which don't really fit 1850, so I'm assuming they aren't 
#used or must be kludged to the weird values they have.
time_vars=['time','time_bnds','date','calyear','calmonth','calday']

#OPEN FILES:
#==============
fi=Dataset(in_file)
fd=Dataset(data_file)
fo=Dataset(out_file,'w',format='NETCDF3_CLASSIC')

#INITIALIZE TIME INFO FROM DATA FILE:
#==============
t=fd['time'][:]

#time units are inconsistent across input files and 'units' attribute isn't always available.
#Thus I'm testing difference btwn consecutive samples to empirically check units. 
if np.abs( (t[1]-t[0])*365. - 30.)<3: #tests whether units are years
    #find index of first time >start_yr and first time>end_yr
    start_ind=pl.find(t>=start_yr)[0] 
    end_ind=pl.find(t>=end_yr)[0]
elif fi['time'].units=='days since 1850-01-01 00:00:00':
    t=1850.+t/365.
    start_ind=pl.find(t>=start_yr)[0] 
    end_ind=pl.find(t>=end_yr)[0]
else:
    raise Exception('Unknown time units')

#DEAL WITH DIMENSIONS:
#==============
#Copy dimensions. Got code from https://gist.github.com/guziy/8543562
for dname, the_dim in fi.dimensions.iteritems():
    if dname not in skip_dims:
        fo.createDimension(dname, len(the_dim))

#TRANSFER VARS:
#===============
# Copy variables. Code from https://gist.github.com/guziy/8543562
for v_name, varin in fi.variables.iteritems():
    if v_name not in skip_vars:

        #correct inconsistent name btwn wavelength and wlen_bnds
        if v_name=='wlen_bnds':
            v_name='wavelength_bnds'

        outVar = fo.createVariable(v_name, varin.datatype, varin.dimensions)
        outVar.setncatts({k: varin.getncattr(k) for k in varin.ncattrs()})

        #HANDLE VARIABLES THAT DON'T REQUIRE AVERAGING:
        #------------------------------------
        if 'time' not in varin.dimensions or v_name in time_vars:
            print '  Copying ',v_name
            outVar[:] = varin[:]
      
        #AVERAGE VARIABLES WHERE NEEDED.
        #------------------------------------
        else:
            print '  Averaging ',v_name
            inVar=fd.variables[v_name]

            if inVar.dimensions[0]!='time':
                raise Exception('Expected time to be first axis for '+v_name)

            #Get average:
            if v_name=='ssi':
                #fd has units W/m2/nm and fo has units mW/m2/nm
                val=np.average(inVar[start_ind:end_ind]*1000.,axis=0)
            else:
                val=np.average(inVar[start_ind:end_ind],axis=0)

            #Write averages:
            outVar[0]=val
            outVar[1]=val
                
            #MAKE PLOTS FOR DEBUGGING (COMMENT THIS SECTION OUT)
            if v_name != 'ssi': #ssi has wavelength dim.
                pl.figure()
                pl.plot(t[start_ind:end_ind],inVar[start_ind:end_ind])
                pl.plot([t[start_ind],t[end_ind]],[val,val],'r--')
                pl.title(v_name)
            else:
                pl.figure()
                pl.subplot(2,1,1)
                pl.pcolor(inVar[start_ind:end_ind])
                pl.title(v_name+' input')
                pl.colorbar()
                pl.subplot(2,1,2)
                pl.pcolor(outVar[:])
                pl.colorbar()
                pl.title(v_name+' output')
        
        #masking didn't work and doesn't affect model run, so skipping it.
        #IF VAR IS MASKED IN 1850, ASSUME IT SHOULD BE IN 1950 TOO.
        #if v_name!='wavelength_bnds' and np.ma.is_masked(fi.variables[v_name][:]):
        #    outVar[:]=np.ma.array(outVar[:],mask=fi.variables[v_name][:].mask,dtype=outVar[:].dtype)
        #    outVar.set_fill_on()

#APPEND METADATA
#==============
#First, copy *all* attributes to the new file
fo.setncatts({k: fi.getncattr(k) for k in fi.ncattrs()})

#Now, overwrite selected attributes
fo.title=titl
fo.creation_date=time.asctime()
fo.created_by=user
fo.history='Created '+time.asctime()+' by ~/py/acme/inputdata/solar1950.py; '+fi.history
 
#CLOSE FILES:
#==============
fi.close()
fo.close()
fd.close()

pl.show()

