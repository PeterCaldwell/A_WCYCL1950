#!usr/bin/env python
"""
Get 1950 GHG concentrations. Since these values
are simply written into the use_cases, we don't 
need to write to netcdf here. Also, GHGs increase
smoothly, so we can just read the 1950 values from
the transient files rather than averaging.
"""

from netCDF4 import Dataset
import numpy as np
import pylab as pl

f=Dataset('/project/projectdirs/acme/inputdata/atm/cam/ggas/GHG_CMIP-1-2-0_Annual_Global_0000-2014_c20171026.nc')

"""
<ch4vmr>808.249e-9</ch4vmr>
<n2ovmr>273.0211e-9</n2ovmr>
<f11vmr>32.1102e-12</f11vmr>
<f12vmr>0.0</f12vmr>
"""
#About time: the above file has annual resolution starting in 
#yr 1 and ending in yr 2015. time is in days and is hard to parse.
#date is YYYYMMDD so date[i]/10000 (integer division) is the yr
d=f.variables['date']
ind=1950
if d[1950]/10000 != 1950:
    raise Exception('Expected ind=%i to be yr 1950 but it is not.'%(ind))

vars=['CH4','N2O','f11','f12']
val1850=['808.249e-9','273.0211e-9','32.1102e-12','0.0']
k=-1
for var in vars:
    k+=1
    print '%s = %e4. Units = %s. 1850 val = %s'%(var,f.variables[var][ind],f.variables[var].units,val1850[k])


