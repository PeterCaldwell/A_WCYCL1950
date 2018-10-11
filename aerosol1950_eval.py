#!/usr/bin/env python
"""
Evaluate implementation of 1950 aerosol file. 
"""

#IMPORT STUFF:
#======================
import numpy as np
import pylab as pl
from netCDF4 import Dataset

#ANALYZE THE MODEL OUTPUT:
#===================================
#model output before making change
#f_orig=Dataset('/global/cscratch1/sd/petercal/ACME_simulations/edison.A_WCYCL1950.1850_test1.ne30_oECv3_ICG/run/edison.A_WCYCL1950.1850_test1.ne30_oECv3_ICG.cam.h0.0001-01-01-00000-rgr.nc')

f_orig=Dataset('/global/cscratch1/sd/petercal/ACME_simulations/edison.A_WCYCL1950.baseline.ne30_oECv3_ICG/run/edison.A_WCYCL1950.baseline.ne30_oECv3_ICG.cam.h0.0001-01-01-00000-rgr.nc')

#model output after making change
f_new=Dataset('/global/cscratch1/sd/petercal/ACME_simulations/edison.A_WCYCL1950.1950_oxid.ne30_oECv3_ICG/run/edison.A_WCYCL1950.1950_oxid.ne30_oECv3_ICG.cam.h0.0001-01-01-00000-rgr.nc')


vars=['TMSOAG','TMso4_a1','TMpom_a1','TMsoa_a1','TMbc_a1','TMdst_a1','TMncl_a1','TMmom_a1','TMnum_a1','TMso4_a2','TMsoa_a2','TMncl_a2','TMmom_a2','TMnum_a2','TMdst_a3','TMncl_a3','TMso4_a3','TMbc_a3','TMpom_a3','TMsoa_a3','TMmom_a3','TMnum_a3','TMpom_a4','TMbc_a4','TMmom_a4','TMnum_a4']

['dst_a1SF','dst_a3SF','num_a1SF','num_a3SF','DSTSFMBL','LND_MBL','SSTSFMBL','ncl_a1SF','ncl_a2SF','ncl_a3SF','mom_a1SF','mom_a2SF','mom_a4SF','SSTSFMBL_OM']

['CT_SOAG','SFSOAG','CT_so4_a1','SFso4_a1','CT_pom_a1','SFpom_a1','CT_soa_a1','SFsoa_a1','CT_bc_a1','SFbc_a1','CT_dst_a1','SFdst_a1','CT_ncl_a1','SFncl_a1','CT_mom_a1','SFmom_a1','CT_num_a1


NOT DONE YET!!!

                        kg/kg/s            72 A  num_a1 source/sink
 1297 SFnum_a1                          1/m2/s             1 A  num_a1 surface flux
 1298 CT_so4_a2                        kg/kg/s            72 A  so4_a2 source/sink
 1299 SFso4_a2                         kg/m2/s             1 A  so4_a2 surface flux
 1300 CT_soa_a2                        kg/kg/s            72 A  soa_a2 source/sink
 1301 SFsoa_a2                         kg/m2/s             1 A  soa_a2 surface flux
 1302 CT_ncl_a2                        kg/kg/s            72 A  ncl_a2 source/sink
 1303 SFncl_a2                         kg/m2/s             1 A  ncl_a2 surface flux
 1304 CT_mom_a2                        kg/kg/s            72 A  mom_a2 source/sink
 1305 SFmom_a2                         kg/m2/s             1 A  mom_a2 surface flux
 1306 CT_num_a2                        kg/kg/s            72 A  num_a2 source/sink
 1307 SFnum_a2                          1/m2/s             1 A  num_a2 surface flux
 1308 CT_dst_a3                        kg/kg/s            72 A  dst_a3 source/sink
 1309 SFdst_a3                         kg/m2/s             1 A  dst_a3 surface flux
 1310 CT_ncl_a3                        kg/kg/s            72 A  ncl_a3 source/sink
 1311 SFncl_a3                         kg/m2/s             1 A  ncl_a3 surface flux
 1312 CT_so4_a3                        kg/kg/s            72 A  so4_a3 source/sink
 1313 SFso4_a3                         kg/m2/s             1 A  so4_a3 surface flux
 1314 CT_bc_a3                         kg/kg/s            72 A  bc_a3 source/sink
 1315 SFbc_a3                          kg/m2/s             1 A  bc_a3 surface flux
 1316 CT_pom_a3                        kg/kg/s            72 A  pom_a3 source/sink
 1317 SFpom_a3                         kg/m2/s             1 A  pom_a3 surface flux
 1318 CT_soa_a3                        kg/kg/s            72 A  soa_a3 source/sink
 1319 SFsoa_a3                         kg/m2/s             1 A  soa_a3 surface flux
 1320 CT_mom_a3                        kg/kg/s            72 A  mom_a3 source/sink
 1321 SFmom_a3                         kg/m2/s             1 A  mom_a3 surface flux
 1322 CT_num_a3                        kg/kg/s            72 A  num_a3 source/sink
 1323 SFnum_a3                          1/m2/s             1 A  num_a3 surface flux
 1324 CT_pom_a4                        kg/kg/s            72 A  pom_a4 source/sink
 1325 SFpom_a4                         kg/m2/s             1 A  pom_a4 surface flux
 1326 CT_bc_a4                         kg/kg/s            72 A  bc_a4 source/sink
 1327 SFbc_a4                          kg/m2/s             1 A  bc_a4 surface flux
 1328 CT_mom_a4                        kg/kg/s            72 A  mom_a4 source/sink
 1329 SFmom_a4                         kg/m2/s             1 A  mom_a4 surface flux
 1330 CT_num_a4                        kg/kg/s            72 A  num_a4 source/sink
 1331 SFnum_a4                          1/m2/s             1 A  num_a4 surface flux


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

