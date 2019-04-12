# ======================================================================
# convective_transition_diag_v1r3.py
#
#   Convective Transition Diagnostic Package
#   
#   Version 1 revision 3 13-Nov-2017 Yi-Hung Kuo (UCLA)
#   Contributors: K. A. Schiro (UCLA), B. Langenbrunner (UCLA), F. Ahmed (UCLA), 
#    C. Martinez (UCLA), C.-C. (Jack) Chen (NCAR)
#   PI: J. David Neelin (UCLA)
#
#   Currently consists of following functionalities:
#    (1) Convective Transition Basic Statistics (convecTransBasic.py)
#    (2) Convective Transition Critical Collapse (convecTransCriticalCollape.py)
#    *(3) Moisture Precipitation Joint Probability Density Function (cwvPrecipJPDF.py)
#    *(4) Super Critical Precipitation Probability (supCriticPrecipProb.py)
#    More on the way...(* under development)
#
#   All scripts of this package can be found under
#    /var_code/convective_transition_diag
#    & data under /obs_data/convective_transition_diag
#
#   The following Python packages are required:
#    os,glob,json,Dataset,numpy,scipy,matplotlib
#    & networkx,warnings,numba, netcdf4
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
#    Kuo et al (2017a): Convective transition statistics over tropical oceans
#      for climate model diagnostics: Observational baseline. Submitted to JAS.*
#    Kuo et al (2017b): Convective transition statistics over tropical oceans
#      for climate model diagnostics: GCM performance. In preparation.*
#    *See http://research.atmos.ucla.edu/csi//REF/pub.html for updates.
#    Neelin, J. D., O. Peters, and K. Hales, 2009: The transition to strong
#      convection. J. Atmos. Sci., 66, 2367-2384, doi:10.1175/2009JAS2962.1.
#    Sahany, S., J. D. Neelin, K. Hales, and R. B. Neale, 2012:
#      Temperature-moisture dependence of the deep convective
#      transition as a constraint on entrainment in climate models.
#      J. Atmos. Sci., 69, 1340-1358, doi:10.1175/JAS-D-11-0164.1.
#    Schiro, K. A., J. D. Neelin, D. K. Adams, and B. R. Linter, 2016:
#      Deep convection and column water vapor over tropical land
#      versus tropical ocean: A comparison between the Amazon and
#      the tropical western Pacific. J. Atmos. Sci., 73, 4043-4063,
#      doi:10.1175/JAS-D-16-0119.1.
#    Kuo, Y.-H., J. D. Neelin, and C. R. Mechoso, 2017: Tropical Convective 
#      Transition Statistics and Causality in the Water Vapor-Precipitation
#      Relation. J. Atmos. Sci., 74, 915-931, doi:10.1175/JAS-D-16-0182.1.
#   See also:
#    Peters, O., and J. D. Neelin, 2006: Critical phenomena in
#      atmospheric precipitation. Nat. Phys., 2, 393-396,
#      doi:10.1038/nphys314. 
#    Holloway, C. E., and J. D. Neelin, 2009: Moisture vertical structure
#      column water vapor, and tropical deep convection. J. Atmos. Sci.,
#      66, 1665-1683, doi:10.1175/2008JAS2806.1.
#    Sahany, S., J. D. Neelin, K. Hales, and R. B. Neale, 2014: Deep
#      convective transition characteristics in the NCAR CCSM and changes
#      under global warming. J. Climate, 27, 9214-9232, 
#      doi: 10.1175/2010JCLI3498.1.
#
# OPEN SOURCE COPYRIGHT Agreement TBA
# ======================================================================
# Import standard Python packages
import os
import glob


os.environ["pr_file"] = "*."+os.environ["pr_var"]+".1hr.nc"
os.environ["prw_file"] = "*."+os.environ["prw_var"]+".1hr.nc"
os.environ["ta_file"] = "*."+os.environ["ta_var"]+".1hr.nc"
os.environ["tave_file"] = "*."+os.environ["tave_var"]+".1hr.nc"
os.environ["qsat_int_file"] = "*."+os.environ["qsat_int_var"]+".1hr.nc"

## Model output filename convention
os.environ["MODEL_OUTPUT_DIR"]=os.environ["DATADIR"]+"/1hr"
#os.environ["pr_file"] = "*."+os.environ["pr_var"]+".1hr.nc"
#os.environ["prw_file"] = "*."+os.environ["prw_var"]+".1hr.nc"
#os.environ["ta_file"] = "*."+os.environ["ta_var"]+".1hr.nc"
#os.environ["tave_file"] = "*."+os.environ["tave_var"]+".1hr.nc"
#os.environ["qsat_int_file"] = "*."+os.environ["qsat_int_var"]+".1hr.nc"

# Specify parameters for Convective Transition Diagnostic Package
# Use 1:tave, or 2:qsat_int as Bulk Tropospheric Temperature Measure 
os.environ["BULK_TROPOSPHERIC_TEMPERATURE_MEASURE"] = "2"
os.environ["RES"] = "1.00" # Spatial Resolution (degree) for TMI Data (0.25, 0.50, 1.00)

missing_file=0
if len(glob.glob(os.environ["MODEL_OUTPUT_DIR"]+"/"+os.environ["pr_file"]))==0:
    print("Required Precipitation data missing!")
    missing_file=1
if len(glob.glob(os.environ["MODEL_OUTPUT_DIR"]+"/"+os.environ["prw_file"]))==0:
    print("Required Precipitable Water Vapor (CWV) data missing!")
    missing_file=1
if len(glob.glob(os.environ["MODEL_OUTPUT_DIR"]+"/"+os.environ["ta_file"]))==0:
    if (os.environ["BULK_TROPOSPHERIC_TEMPERATURE_MEASURE"]=="2" and \
       len(glob.glob(os.environ["MODEL_OUTPUT_DIR"]+"/"+os.environ["qsat_int_file"]))==0) \
    or (os.environ["BULK_TROPOSPHERIC_TEMPERATURE_MEASURE"]=="1" and \
       (len(glob.glob(os.environ["MODEL_OUTPUT_DIR"]+"/"+os.environ["qsat_int_file"]))==0 or \
        len(glob.glob(os.environ["MODEL_OUTPUT_DIR"]+"/"+os.environ["tave_file"]))==0)):
        print("Required Temperature data missing!")
        missing_file=1

if missing_file==1:
    print("Convective Transition Diagnostic Package will NOT be executed!")
else:
    # ======================================================================
    # Create directories
    # ======================================================================
    if not os.path.exists(os.environ["variab_dir"]+"/convective_transition_diag"):
        os.makedirs(os.environ["variab_dir"]+"/convective_transition_diag")
    if not os.path.exists(os.environ["variab_dir"]+"/convective_transition_diag/model"):
        os.makedirs(os.environ["variab_dir"]+"/convective_transition_diag/model")
    if not os.path.exists(os.environ["variab_dir"]+"/convective_transition_diag/model/netCDF"):
        os.makedirs(os.environ["variab_dir"]+"/convective_transition_diag/model/netCDF")
    if not os.path.exists(os.environ["variab_dir"]+"/convective_transition_diag/model/PS"):
        os.makedirs(os.environ["variab_dir"]+"/convective_transition_diag/model/PS")
    if not os.path.exists(os.environ["variab_dir"]+"/convective_transition_diag/obs"):
        os.makedirs(os.environ["variab_dir"]+"/convective_transition_diag/obs")
    if not os.path.exists(os.environ["variab_dir"]+"/convective_transition_diag/obs/PS"):
        os.makedirs(os.environ["variab_dir"]+"/convective_transition_diag/obs/PS")
    if not os.path.exists(os.environ["variab_dir"]+"/convective_transition_diag/obs/netCDF"):
        os.makedirs(os.environ["variab_dir"]+"/convective_transition_diag/obs/netCDF")

    ##### Functionalities in Convective Transition Diagnostic Package #####
    # ======================================================================
    # Convective Transition Basic Statistics
    #  See convecTransBasic.py for detailed info
    try:
        os.system("python "+os.environ["VARCODE"]+"/convective_transition_diag/"+"convecTransBasic.py")
    except OSError as e:
        print('WARNING',e.errno,e.strerror)
        print("**************************************************")
        print("Convective Transition Basic Statistics (convecTransBasic.py) is NOT Executed as Expected!")		
        print("**************************************************")

    ## ======================================================================
    ## Convective Transition Critical Collapse
    ##  Requires output from convecTransBasic.py
    ##  See convecTransCriticalCollapse.py for detailed info
    try:
        os.system("python "+os.environ["VARCODE"]+"/convective_transition_diag/"+"convecTransCriticalCollapse.py")
    except OSError as e:
        print('WARNING',e.errno,e.strerror)
        print("**************************************************")
        print("Convective Transition Thermodynamic Critical Collapse (convecTransCriticalCollapse.py) is NOT Executed as Expected!")		
        print("**************************************************")

    ##### THE FOLLOWING FUNCTIONALITIES HAVE NOT BEEN IMPLEMENTED YET!!!#####
    ## ======================================================================
    ## Moisture Precipitation Joint Probability Density Function
    ##  See cwvPrecipJPDF.py for detailed info
    #os.system("python "+os.environ["VARCODE"]+"/convective_transition_diag/"+"cwvPrecipJPDF.py")
    ## ======================================================================
    ## Super Critical Precipitation Probability
    ##  Requires output from convecTransBasic.py
    ##  See supCriticPrecipProb.py for detailed info
    #os.system("python "+os.environ["VARCODE"]+"/convective_transition_diag/"+"supCriticPrecipProb.py")

    ######################### HTML sections below #########################
    # ======================================================================
    #  Copy & modify the template html
    # ======================================================================
    # Copy template html (and delete old html if necessary)
    if os.path.isfile( os.environ["variab_dir"]+"/convective_transition_diag/convective_transition_diag.html" ):
        os.system("rm -f "+os.environ["variab_dir"]+"/convective_transition_diag/convective_transition_diag.html")

    os.system("cp "+os.environ["VARCODE"]+"/convective_transition_diag/convective_transition_diag.html "+os.environ["variab_dir"]+"/convective_transition_diag/.")

    # Replace keywords in the copied html template if different bulk temperature or resolution are used
    if os.environ["BULK_TROPOSPHERIC_TEMPERATURE_MEASURE"] == "2":
        os.system("cat "+os.environ["variab_dir"]+"/convective_transition_diag/convective_transition_diag.html "+"| sed -e s/_tave\./_qsat_int\./g > "+os.environ["variab_dir"]+"/convective_transition_diag/tmp.html")
        os.system("mv "+os.environ["variab_dir"]+"/convective_transition_diag/tmp.html "+os.environ["variab_dir"]+"/convective_transition_diag/convective_transition_diag.html")
    if os.environ["RES"] != "1.00":
        os.system("cat "+os.environ["variab_dir"]+"/convective_transition_diag/convective_transition_diag.html "+"| sed -e s/_res\=1\.00_/_res\="+os.environ["RES"]+"_/g > "+os.environ["variab_dir"]+"/convective_transition_diag/tmp.html")
        os.system("mv "+os.environ["variab_dir"]+"/convective_transition_diag/tmp.html "+os.environ["variab_dir"]+"/convective_transition_diag/convective_transition_diag.html")

    # Replace CASENAME so that the figures are correctly linked through the html
    os.system("cp "+os.environ["variab_dir"]+"/convective_transition_diag/convective_transition_diag.html "+os.environ["variab_dir"]+"/convective_transition_diag/tmp.html")
    os.system("cat "+os.environ["variab_dir"]+"/convective_transition_diag/convective_transition_diag.html "+"| sed -e s/casename/"+os.environ["CASENAME"]+"/g > "+os.environ["variab_dir"]+"/convective_transition_diag/tmp.html")
    os.system("cp "+os.environ["variab_dir"]+"/convective_transition_diag/tmp.html "+os.environ["variab_dir"]+"/convective_transition_diag/convective_transition_diag.html")
    os.system("rm -f "+os.environ["variab_dir"]+"/convective_transition_diag/tmp.html")

    a = os.system("cat "+os.environ["variab_dir"]+"/index.html | grep convective_transition_diag")
    if a != 0:
       os.system("echo '<H3><font color=navy>Convective transition diagnostics <A HREF=\"convective_transition_diag/convective_transition_diag.html\">plots</A></H3>' >> "+os.environ["variab_dir"]+"/index.html")

    # Convert PS to png
    if os.path.exists(os.environ["variab_dir"]+"/convective_transition_diag/model"):
        files = os.listdir(os.environ["variab_dir"]+"/convective_transition_diag/model/PS")
        a = 0
        while a < len(files):
            file1 = os.environ["variab_dir"]+"/convective_transition_diag/model/PS/"+files[a]
            file2 = os.environ["variab_dir"]+"/convective_transition_diag/model/"+files[a]
            os.system("convert -crop 0x0+5+5 "+file1+" "+file2[:-3]+".png")
            a = a+1
        if os.environ["CLEAN"] == "1":
            os.system("rm -rf "+os.environ["variab_dir"]+"/convective_transition_diag/model/PS")
    if os.path.exists(os.environ["variab_dir"]+"/convective_transition_diag/obs"):
        files = os.listdir(os.environ["variab_dir"]+"/convective_transition_diag/obs/PS")
        a = 0
        while a < len(files):
            file1 = os.environ["variab_dir"]+"/convective_transition_diag/obs/PS/"+files[a]
            file2 = os.environ["variab_dir"]+"/convective_transition_diag/obs/"+files[a]
            os.system("convert -crop 0x0+5+5 "+file1+" "+file2[:-3]+".png")
            a = a+1
        if os.environ["CLEAN"] == "1":
            os.system("rm -rf "+os.environ["variab_dir"]+"/convective_transition_diag/obs/PS")
    # ======================================================================
    # End of HTML sections
    # ======================================================================    

    print("**************************************************")
    print("Convective Transition Diagnostic Package (convective_transition_diag_v1r3.py) Executed!")
    print("**************************************************")
