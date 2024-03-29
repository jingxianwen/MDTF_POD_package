#======================================================================
# CFODD_warm_rain_microphysics.py
# Contoured Frequency by Optical Depth Diagram (CFODD). 
#
# Version 2.0 (April 21, 2019)
# Contributors: X. Jing (AORI, U-Tokyo), K. Suzuki (AORI, U-Tokyo).
#
# Currently consists of following functionalities:
# (1) compute CFODD statisitcs. (compute_cfodd.ncl)
# (2) plot the figure for CFODD statistics. (cfodd_plot.ncl)
#
# All scripts of this package can be found under
#    ../../var_code/CFODD_warm_rain_microphysics
# Figure of observational data can be found under 
#    ../../../inputdata/obs_data/CFODD_warm_rain_microphysics
#
#    Required variables (v2.0):
#     (1) radar reflectivity (units: dBZ) and cloud_type info (=1: stratiform cloud; 
#         =2: convective cloud) from cloud simulator (e.g. cospOUT%cloudsat_Ze_tot 
#         and cospIN%frac_out from COSP2.0), on subcolumns.
#     (2) cloud optical depth at each model layer.
#     (3) effective radius of cloud droplets at cloud top (or. droplet effective radius profile).
#     (4) cloud water and ice mixing ratio at each model layer (for warm cloud identification)
#     (5) atmospheric temperature profiles (for warm cloud identification).
#
# Note: 
#     All variables should be provided as timeslice output, and vertical profiles outputed on
#     PRESSURE levels.
# 
# Run-where info:
#    The computing of CFODD statistics may be slow depending on the data size. 
#    To know where you are in the whole computing process, please refer to:
#      /variab_dir/MDTF_$casename$/CFODD_warm_rain_microphysics/run_where.txt.
#
# Reference:
#    Suzuki, K., Stephens, G. L., Bodas-Salcedo, et al. (2015). Evaluation
#        of the warm rain formation process in global models with satellite 
#        observations. JAS, 72, 3996-4014.
#    Jing, X., Suzuki, K., Guo, H., et al. (2017). A multimodel study on warm
#        precipitation biases in global models compared to satellite observations.
#        JGR Atmosphere, 122, 11,806-11,824.
#======================================================================
import os
import subprocess


#============================================================
# generate_ncl_plots - call a nclPlotFile via subprocess call
#============================================================
def generate_ncl_plots(nclPlotFile):
   """generate_plots_call - call a nclPlotFile via subprocess call
   
   Arguments:
   nclPlotFile (string) - full path to ncl plotting file name
   """
   # check if the nclPlotFile exists - 
   # don't exit if it does not exists just print a warning.
   try:
      pipe = subprocess.Popen(['ncl {0}'.format(nclPlotFile)], shell=True, stdout=subprocess.PIPE)
      output = pipe.communicate()[0]
      print('NCL routine {0} \n {1}'.format(nclPlotFile,output))            
      while pipe.poll() is None:
         time.sleep(0.5)
   except OSError as e:
      print('WARNING',e.errno,e.strerror)

   return 0
#============================================================
# Set up directories
#============================================================

if not os.path.exists(os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/CFODD_warm_rain_microphysics"):
   os.makedirs(os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/CFODD_warm_rain_microphysics")
# model figures and data
if not os.path.exists(os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/CFODD_warm_rain_microphysics/model"):
   os.makedirs(os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/CFODD_warm_rain_microphysics/model")

if not os.path.exists(os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/CFODD_warm_rain_microphysics/model/PS"):
   os.makedirs(os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/CFODD_warm_rain_microphysics/model/PS")

if not os.path.exists(os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/CFODD_warm_rain_microphysics/model/netCDF"):
   os.makedirs(os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/CFODD_warm_rain_microphysics/model/netCDF")

# observational figures and data
if not os.path.exists(os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/CFODD_warm_rain_microphysics/obs"):
   os.makedirs(os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/CFODD_warm_rain_microphysics/obs")

if not os.path.exists(os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/CFODD_warm_rain_microphysics/obs/netCDF"):
   os.makedirs(os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/CFODD_warm_rain_microphysics/obs/netCDF")

#============================================================
# Call NCL code here
#============================================================

print("MAKE CFODD PLOTS FROM MODEL DATA ")

print("COMPUTING CFODD ... this may take several hours depending on data size")
print("See "+os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/CFODD_warm_rain_microphysics/runwhere.txt for the status.")

generate_ncl_plots(os.environ["VARCODE"]+"/CFODD_warm_rain_microphysics/compute_cfodd.ncl")

print("PLOTTING CFODD_warm_rain_microphysics")

generate_ncl_plots(os.environ["VARCODE"]+"/CFODD_warm_rain_microphysics/cfodd_plot.ncl")

#============================================================
# Copy Template HTML File to appropriate directory
#============================================================
if os.path.isfile( os.environ["variab_dir"]+"/CFODD_warm_rain_microphysics/CFODD_warm_rain_microphysics.html" ):
   os.system("rm -f "+os.environ["variab_dir"]+"/CFODD_warm_rain_microphysics/CFODD_warm_rain_microphysics.html")

os.system("cp "+os.environ["VARCODE"]+"/CFODD_warm_rain_microphysics/CFODD_warm_rain_microphysics.html "+os.environ["variab_dir"]+"/CFODD_warm_rain_microphysics/.")

os.system("cp "+os.environ["variab_dir"]+"/CFODD_warm_rain_microphysics/CFODD_warm_rain_microphysics.html "+os.environ["variab_dir"]+"/CFODD_warm_rain_microphysics/tmp.html")
os.system("cat "+os.environ["variab_dir"]+"/CFODD_warm_rain_microphysics/CFODD_warm_rain_microphysics.html "+"| sed -e s/casename/"+os.environ["CASENAME"]+"/g > "+os.environ["variab_dir"]+"/CFODD_warm_rain_microphysics/tmp.html")
os.system("cp "+os.environ["variab_dir"]+"/CFODD_warm_rain_microphysics/tmp.html "+os.environ["variab_dir"]+"/CFODD_warm_rain_microphysics/CFODD_warm_rain_microphysics.html")
os.system("rm -f "+os.environ["variab_dir"]+"/CFODD_warm_rain_microphysics/tmp.html")

#============================================================
# Add to HTML File
#  This adds a line to the main html page (index.html)
#============================================================
a = os.system("cat "+os.environ["variab_dir"]+"/index.html | grep CFODD_warm_rain_microphysics")
if a != 0:
   os.system("echo '<H3><font color=navy>CFODD for warm clouds over ocean <A HREF=\"CFODD_warm_rain_microphysics/CFODD_warm_rain_microphysics.html\">plots</A></H3>' >> "+os.environ["variab_dir"]+"/index.html")   

#============================================================
# convert PS to png
#============================================================
if os.path.exists(os.environ["variab_dir"]+"/CFODD_warm_rain_microphysics/model"):
   files = os.listdir(os.environ["variab_dir"]+"/CFODD_warm_rain_microphysics/model/PS")
   a = 0
   while a < len(files):
      file1 = os.environ["variab_dir"]+"/CFODD_warm_rain_microphysics/model/PS/"+files[a]
      file2 = os.environ["variab_dir"]+"/CFODD_warm_rain_microphysics/model/"+files[a]
      os.system("convert -crop 0x0+5+5 "+file1+" "+file2[:-3]+".png")
      a = a+1
   if os.environ["CLEAN"] == "1":
      os.system("rm -f "+os.environ["variab_dir"]+"/CFODD_warm_rain_microphysics/model/PS/*.ps")

#============================================================
# Copy obs gifs into the expected location
#============================================================
   os.system("cp "+os.environ["VARDATA"]+"/CFODD_warm_rain_microphysics/*.gif "+os.environ["variab_dir"]+"/CFODD_warm_rain_microphysics/obs/.")
