# ======================================================================
# AMOC_qts_from_yearly.py
#
#   Calculate Stream Function on Density
#    as part of functionality provided by (transport_onto_TS.py)
#
#   Version 1 revision 2 8-Jan-2017 Fuchang Wang (FSU/COAPS)
#   Contributors: 
#   PI: Xiaobiao Xu (FSU/COAPS)
#
#   Equation:
#    Stream Function = definite integral of volume transport along Density, based on Q(T,S)
#    At specific time and latitude:
#     Q(T,S) + Density r(T,S) --> Q(r)
#                r
#     Psai(r) = S Q(r) * dr
#                0
#  
#   Generates plots of:
#    (1) stream function on density (AMOC_qts_plot.ncl)
#   
#   Depends on the following scripts:
#    (1) AMOC_qts_from_yearly.ncl
#
#   The following 3 variables are required:
#     (1) 2D Density r(T,S) (sig2, units: "kg/m^3", TMP.sigma2.fx.ncl)
#     (2) 1D y axis latitude( lat, units: "degrees_north", lat_extract.py)
#     (3) 4D Volume Transport onto T/S (trans, m^3/s, trans_lats_monthly.py)
#    
# OPEN SOURCE COPYRIGHT Agreement TBA
# ======================================================================

def AMOC_qts_from_yearly(model,ncl_script):
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
    ncs = glob.glob(os.environ["OUTDIR"]+model+".trans_????-????.yr*.nc")
    print("ncs:---------------------------------")
    print(ncs)
    num_vmo_files=len(ncs)
    if num_vmo_files > 0:
       for nc in ncs:
#          print nc
          npos = nc.index('.yr.nc')
          yyyymm = nc[npos-9:npos]
          yyyy0 = yyyymm[0:4]
          yyyy1 = yyyymm[5:9]
          print yyyymm, yyyy0, yyyy1

          script=os.environ["SRCDIR"]+ncl_script
          sname=os.path.splitext(os.path.basename(script))[0]
          ncl=os.environ["SRCDIR"]+sname+"_"+model+"_"+yyyymm+".ncl"
          shutil.copy(script,ncl)
          subprocess.call(["sed", "-i", "s#CCSM4#"+model+"#g", ncl])
          subprocess.call(["sed", "-i", "s#1850-1860#"+yyyy0+"-"+yyyy1+"#g", ncl])
          subprocess.call(["sed", "-i", "s#year=1850#year="+yyyy0+"#g", ncl])
          print("COMPUTING AMOCr from QTS ... "+model)
          execute_ncl_calculate(ncl)
          os.system("rm -f "+ncl)
