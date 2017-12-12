#!/usr/bin/bash
#NOTE: THIS FILE IS NOT USED ANY MORE BECAUSE DMS SHOULD BE INTERPOLATED
#      BETWEEN 1850 AND 2000 VALUES RATHER THAN COPIED FROM 1850.
#
#Just take the existing 1850 DMS emission file and change its 
#date variable to be 1950 instead of 1850 so the model will run
#for 1950 compsets. Easiest to do this in nco.
#Note that running this code raised 
#"ncap2: WARNING assign(): Var being read and written in ASSIGN date"
#error, but ncdumping the old vs new file shows that the results are 
#exactly what was desired.

module load nco

ncap2 -s 'date(:)={19500115,19500215,19500315,19500415,19500515,19500615,19500715,19500815,19500915,19501015,19501115,19501215}' /project/projectdirs/acme/inputdata/atm/cam/chem/trop_mozart_aero/emis/DMSflux.1850.1deg_latlon_conserv.POPmonthlyClimFromACES4BGC_c20160416.nc $CSCRATCH/junk/CMIP6/tmp.nc 

ncatted -O -a comment,global,c,c,'Peter Caldwell: This 1950 file is identical to the 1850 file noted in history except date has been changed to 1950. This is a hack designed to get the 1950 compset running in the absence of 1950 DMS info.' $CSCRATCH/junk/CMIP6/tmp.nc $CSCRATCH/junk/CMIP6/DMSflux.1950.1deg_latlon_conserv.POPmonthlyClimFromACES4BGC_c20171208.nc
