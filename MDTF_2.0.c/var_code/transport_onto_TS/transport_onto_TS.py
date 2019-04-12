#   Version 1 revision 3 8-Jan-2017 Fuchang Wang (FSU/COAPS)
#   Contributors: 
#   PI: Xiaobiao Xu (FSU/COAPS)
#
#   Currently consists of following functionalities:
#    (1) Calculate volume transport from velocity (recover_vmo_by_vo.py)
#    (2) Calculate yearly mean from monthly data (monthly_to_yearly.py)
#    (3) Calculate long-term mean from yearly data (yearly_to_climate.py)
#    (4) Calculate Stream Functionion on Depth coordinate (AMOC_T2B_from_climate.py)
#    (5) Interpolate Tracer grid to Velocity grid (interp_vit_to_viv_monthly.py)
#    (6) Project Transport (V) onto Temperature/Salinity (T/S)plane (trans_lats_monthly.py)
#    (7) Calculate Stream Functionion on Density coordinate (AMOC_qts_from_yearly.py)
#    (8) Transport weighted Temperature and Salinity (trans_wgt_TS_yearly.py)
#    (9) Meridional Heat Transport (MHT) and Freshwater Transport (MFWT) (MHT_MFWT_qts_from_yearly.py)
#    (10) Ploting results (transport_onto_TS_plot.py)
#    (11) Ploting observation or high-resolution HYCOM results (obs_transport_onto_TS.py)
#
#   All scripts of this package can be found under
#    /var_code/transport_onto_TS
#    & data under /obs_data/transport_onto_TS
#
#   The following Python packages are required:
#    os,glob,shutil,subprocess

#   Use Anaconda:
#    These Python packages are already included in the standard installation
#
#   The following 3 3-D (lat-lon-time) model fields are required:
#     (1) precipitation rate (units: mm/s = kg/m^2/s)
#     (2) column water vapor (CWV, or precipitable water vapor; units mm = kg/m^2)
#     (3) mass-weighted column average temperature (units: K) 
#          or column-integrated saturation specific humidity (units mm = kg/m^2)
#          with column being 1000-200 hPa by default 
#    Since (3) is not standard model output yet, this package will automatically
#    calculate (3) if the follwoing 4-D (lat-lon-pressure-time) model field is available:
#     (4) air temperature (units: K)
#
#   Reference: 
#    Xu X., P. B. Rhines, and E. P. Chassignet (2016): Temperature-Salinity Structure of the North Atlantic Circulation and Associated Heat and Freshwater Transports. J. Cli., 29, 7723-7742, doi: 10.1175/JCLI-D-15-0798.1
#
# OPEN SOURCE COPYRIGHT Agreement TBA
# ======================================================================
# Import standard Python packages
import os
import sys
import glob
import shutil
import subprocess

os.environ["DT"]     =  "0.2"
os.environ["DS"]     =  "0.04"
os.environ["LAT0"]   =  "26.5"
#os.environ["MODELS"] =  ', '.join(CMIP5_MODELS)
os.environ["MODELS"] =  os.environ["CASENAME"]
os.environ["SRCDIR"] =  os.environ["DIAG_HOME"]+"/var_code/transport_onto_TS/"
os.environ["HTMDIR"] =  os.environ["DIAG_HOME"]+"/var_code/transport_onto_TS/"
os.environ["RGBDIR"] =  os.environ["DIAG_HOME"]+"/var_code/util/rgb/"

os.environ["REFDIR"] =  os.environ["DATA_IN"]+"/obs_data/transport_onto_TS/"
os.environ["CLMREF"] =  os.environ["DATA_IN"]+"/obs_data/transport_onto_TS/clim/"
os.environ["FIXREF"] =  os.environ["DATA_IN"]+"/obs_data/transport_onto_TS/fx/"

os.environ["FIXDIR"] =  os.environ["DIAG_HOME"]+"/"+os.environ["CASENAME"]+"/fx/"
os.environ["MONDIR"] =  os.environ["DIAG_HOME"]+"/"+os.environ["CASENAME"]+"/mon/"

os.environ["CASDIR"] =  os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/"
os.environ["QTSDIR"] =  os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/transport_onto_TS/"
os.environ["PNGDIR"] =  os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/transport_onto_TS/model/"
os.environ["FIGDIR"] =  os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/transport_onto_TS/model/PS/"
os.environ["OUTDIR"] =  os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/transport_onto_TS/model/netCDF/"
os.environ["TMPDIR"] =  os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/transport_onto_TS/model/netCDF/mon_yr/"
os.environ["FIGREF"] =  os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/transport_onto_TS/obs/PS/"
os.environ["PNGREF"] =  os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/transport_onto_TS/obs/"
if not os.path.exists(os.environ["SRCDIR"]):
   os.makedirs(os.environ["SRCDIR"])
if not os.path.exists(os.environ["CLMREF"]):
   os.makedirs(os.environ["CLMREF"])
if not os.path.exists(os.environ["FIXREF"]):
   os.makedirs(os.environ["FIXREF"])
if not os.path.exists(os.environ["FIXDIR"]):
   os.makedirs(os.environ["FIXDIR"])
if not os.path.exists(os.environ["MONDIR"]):
   os.makedirs(os.environ["MONDIR"])
if not os.path.exists(os.environ["FIGDIR"]):
   os.makedirs(os.environ["FIGDIR"])
if not os.path.exists(os.environ["FIGREF"]):
   os.makedirs(os.environ["FIGREF"])
if not os.path.exists(os.environ["TMPDIR"]):
   os.makedirs(os.environ["TMPDIR"])

#os.system("\cp "+os.environ["RGBDIR"]+"*.rgb "+os.environ["NCARG_ROOT"]+"/lib/ncarg/colormaps/")
os.system("\cp -f "+os.environ["HTMDIR"]+"mdtf_diag_banner.png "+os.environ["QTSDIR"])
#os.system("\cp -f "+os.environ["HTMDIR"]+"mdtf_diag_banner.png "+os.environ["CASDIR"])
#os.system("\cp -f "+os.environ["HTMDIR"]+"mdtf1.html           "+os.environ["CASDIR"]+"index.html")
print(os.environ["HTMDIR"]+"mdtf1.html")
print(os.environ["QTSDIR"]+"index.html")

a = os.system("cat "+os.environ["variab_dir"]+"/index.html | grep transport_onto_TS")
if a != 0:
   os.system("echo '<H3><font color=navy>3D structure of AMOC<A HREF=\"transport_onto_TS/transport_onto_TS.html\">plots</A></H3>' >> "+os.environ["variab_dir"]+"/index.html")


ncs=glob.glob(os.environ["MONDIR"]+os.environ["CASENAME"]+"."+os.environ["vmo_var"]+".mon.nc") + \
   glob.glob(os.environ["MONDIR"]+os.environ["CASENAME"]+"."+os.environ["vo_var"] +".mon.nc")
print(ncs)
if ncs:
   nc = ncs[-1]
   os.system("python "+os.environ["SRCDIR"]+"obs_transport_onto_TS.py")
   os.system("python "+os.environ["SRCDIR"]+"basin_lat_dxdydz.py")
   os.system("python "+os.environ["SRCDIR"]+"transport_onto_TS_v1.py")
else:
   print("No eligible nc file exists in"+os.environ["MONDIR"])
   print("transport_onto_TS is NOT Executed as Expected!")
   
a = os.system("cat "+os.environ["variab_dir"]+"/index.html | grep transport_onto_TS")
if a != 0:
   os.system("echo '<H3><font color=navy>Moist Static Energy diagnostics<A HREF=\"transport_onto_TS.html\">plots</A></H3>' >> "+os.environ["variab_dir"]+"/index.html")
