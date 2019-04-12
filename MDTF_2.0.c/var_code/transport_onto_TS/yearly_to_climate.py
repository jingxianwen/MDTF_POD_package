# ======================================================================
# yearly_to_climate.py
#
#   Calculate long-term mean from yearly data
#    as part of functionality provided by (transport_onto_TS.py)
#
#   Version 1 revision 2 8-Jan-2017 Fuchang Wang (FSU/COAPS)
#   Contributors: 
#   PI: Xiaobiao Xu (FSU/COAPS)
#
#   Equation:
#    average = sum[var] / time
#     ignore   missing grid: time = total_times, ie. number of years
#     consider missing grid: time = occur times, ie. <= total_times
#     user spesify os.environ["which_mean"] to which one
#  
#   Used for variables:
#    (1) Volume Transport (vmo)
#    (2) Temperature (thetao)
#    (3) Salinity (so)
#    (4) Transport(Temperature, Salinity) (trans)
#    (5) Stream Function on Density (moc)
#    (6) Stream Function on Temperature (moc)
#    (7) Stream Function on Salinity (moc)
#    (8) Layered Transport (trans)
#    (9) Transport weighted Temperature (thetao)
#    (10) Transport weighted Salinity (thetao)
#    (11) Meridional Heat Transport (MHT)
#    (12) Meridional Freshwater Transport (MFWT)
#   
#   Depends on the following scripts:
#    (1) monthly_to_yearly.ncl
#    
# OPEN SOURCE COPYRIGHT Agreement TBA
# ======================================================================
#!/usr/bin/python

def yearly_to_climate(model,DIR_in,DIR_out,fname,vname):
    '''
    ----------------------------------------------------------------------
    Note
       Volume Transport
    ----------------------------------------------------------------------
    '''
    import os
    import glob
    import shutil 
    import subprocess
    from post_process import execute_ncl_calculate
    script=os.environ["SRCDIR"]+"yearly_to_climate.ncl"
    sname=os.path.splitext(os.path.basename(script))[0]
    ncs = glob.glob(os.environ["OUTDIR"]+model+"."+fname+"_????-????.yr.nc")
    num_vmo_files=len(ncs)
    if num_vmo_files > 0:
       ncl=os.environ["SRCDIR"]+sname+"_"+model+".ncl"
       shutil.copy(script,ncl)
       subprocess.call(["sed", "-i", "s#CCSM4#"+model+"#g", ncl])
       subprocess.call(["sed", "-i", "s#vmo_#"+fname+"_#g", ncl])
       subprocess.call(["sed", "-i", "s#vmo.clim#"+fname+".clim#g", ncl])
       subprocess.call(["sed", "-i", "s#vmo#"+vname+"#g", ncl])
       print("COMPUTING Yearly to Climate ... "+vname)
       execute_ncl_calculate(ncl)
       os.system("rm -f "+ncl)
