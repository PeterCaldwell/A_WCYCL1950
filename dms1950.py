#!/usr/bin/env python
"""
Make 1950 dms file by interpolating between each month of 1849 and 2000,
which are the only non-future years DMS data is given for.
"""

#IMPORT STUFF:
#=======================
from netCDF4 import Dataset
import pylab as pl
import numpy as np
import time
import os
import grp
from shutil import copyfile

#use this file as the template for the new file
in_fi='/project/projectdirs/acme/inputdata/atm/cam/chem/trop_mozart_aero/emis/DMSflux.1850.1deg_latlon_conserv.POPmonthlyClimFromACES4BGC_c20160416.nc'
fi=Dataset(in_fi)

#get 1950 data from this file
data_fi='/project/projectdirs/acme/inputdata/atm/cam/chem/trop_mozart_aero/emis/DMSflux.1850-2100.1deg_latlon_conserv.POPmonthlyClimFromACES4BGC_c20160727.nc'
fd=Dataset(data_fi)

#this is the output file
out_fi='/global/cscratch1/sd/petercal/junk/CMIP6/DMSflux.1950.1deg_latlon_conserv.POPmonthlyClimFromACES4BGC_c20'+time.strftime('%y%m%d')+'.nc'
fo=Dataset(out_fi,'w',format='NETCDF3_CLASSIC')

#for some reason I can't write a netcdf3_classic file in the inputdata loc (netcdf4 is fine though!)
#so copy it when done.
fin_fi='/project/projectdirs/acme/inputdata/atm/cam/chem/trop_mozart_aero/emis/DMSflux.1950.1deg_latlon_conserv.POPmonthlyClimFromACES4BGC_c20'+time.strftime('%y%m%d')+'.nc'

#just copying these variables from 1850 file because they aren't used and are 
#garbage values in the 1850 file anyways.
time_vars=['time','time_bound']

titl='DMS input for 1950 control simulation computed by interpolating 1849 and 2000 values (the only non-future years DMS data is given for from the transient DMS file DMSflux.1850-2100.1deg_latlon_conserv.POPmonthlyClimFromACES4BGC_c20160727.nc). Time info is copied directly from the 1850 file since it did not seem to be correct anyways. date info is prescribed to the center of each month of yr 1950.'

user='Peter Caldwell'

#DEAL WITH DIMENSIONS:
#==============
#Copy dimensions. Got code from https://gist.github.com/guziy/8543562
for dname, the_dim in fi.dimensions.iteritems():
    fo.createDimension(dname, len(the_dim))

#TRANSFER VARS TO NEW FILE:
#===============
# Copy variables. Code from https://gist.github.com/guziy/8543562
for v_name, varin in fi.variables.iteritems():

    outVar = fo.createVariable(v_name, varin.datatype, varin.dimensions)
    outVar.setncatts({k: varin.getncattr(k) for k in varin.ncattrs()})

    if v_name=='date':
        print '  overwriting date'
        outVar[:]=np.array([19500115,19500215,19500315,19500415,19500515,19500615,19500715,19500815,19500915,19501015,19501115,19501215])

    #HANDLE VARIABLES THAT DON'T REQUIRE AVERAGING:
    #------------------------------------
    elif 'time' not in varin.dimensions or v_name in time_vars:
        print '  Copying ',v_name
        outVar[:] = varin[:]

    #AVERAGE VARIABLES WHERE NEEDED.
    #------------------------------------
    else:
        print '  Interpolating ',v_name
        inVar=fd.variables[v_name]

        if inVar.dimensions[0]!='time':
            raise Exception('Expected time to be first axis for '+v_name)

        #INTERPOLATE:
        #fd has values for each month of 1849, 2000, and 2101. Thus I can
        #get the 1950 val by linear interpolation
        wt=(2000.-1950.)/(2000.-1849.)
        for k in range(12):
            outVar[k]=wt*inVar[k] + (1-wt)*inVar[k+12]

        #MAKE PLOTS FOR DEBUGGING (COMMENT THIS SECTION OUT)
        if v_name =='DMS': #DMS is the only interesting variable.
            lat=fi.variables['lat'][:]
            lon=fi.variables['lon'][:]
            LON,LAT=pl.meshgrid(lon,lat)
            pl.subplot(2,2,1)
            pl.pcolor(LON,LAT,np.average(fi.variables[v_name][0:12],axis=0).squeeze())
            pl.colorbar()
            pl.title(v_name+' 1850')

            pl.subplot(2,2,2)
            pl.pcolor(LON,LAT,np.average(outVar,axis=0).squeeze())
            pl.colorbar()
            pl.title(v_name+' 1950')

            pl.subplot(2,2,3)
            pl.pcolor(LON,LAT,np.average(inVar[12:24],axis=0).squeeze())
            pl.colorbar()
            pl.title(v_name+' 2000')

            pl.subplot(2,2,4)
            pl.pcolor(LON,LAT,np.average(outVar,axis=0).squeeze()-np.average(inVar[0:12],axis=0).squeeze())
            pl.colorbar()
            pl.title(v_name+': 1950-1850')

            pl.figure()
            ind=0
            while inVar[:].mask[0,ind,ind]==True:
                ind+=1
            pl.plot(np.array([1849,2000,2100]),np.array([inVar[0,ind,ind],inVar[12,ind,ind],inVar[24,ind,ind]]))
            pl.plot(1950,outVar[0,ind,ind],'rx')
            pl.title('DMS for 1 loc as f(time)')


#APPEND METADATA
#==============
#First, copy *all* attributes to the new file
fo.setncatts({k: fi.getncattr(k) for k in fi.ncattrs()})

#Now, overwrite selected attributes
fo.title=titl
fo.creation_date=time.asctime()
fo.created_by=user
fo.history='Created '+time.asctime()+' by ~/py/acme/inputdata/dms1950.py; '+fi.history
 
#CLOSE FILES:
#==============
fi.close()
fo.close()
fd.close()

#FIX FILE PERMISSIONS:
#==============
copyfile(out_fi,fin_fi)
os.chmod(fin_fi,0664) #rw-rw-r, leading 0 tells py this is octal.
uid = os.stat(fin_fi).st_uid
gid=grp.getgrnam('acme').gr_gid
os.chown(fin_fi, uid, gid)

pl.show()

