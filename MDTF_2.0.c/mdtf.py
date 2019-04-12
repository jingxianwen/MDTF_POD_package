# ======================================================================
# NOAA Model Diagnotics Task Force (MDTF) Diagnostic Driver
#
# Dec 2018  
# Dani Coleman, NCAR
# Chih-Chieh (Jack) Chen, NCAR, 
# Yi-Hung Kuo, UCLA
#
# This release uses the following Python modules: 
#     os, glob, json, dataset, numpy, scipy, matplotlib, 
#     networkx, warnings, numba, netcdf4
# ======================================================================
#
# Changes from previous version DRB
#
# Add documentation of namelist, varlist, settings
#
# setenv('VARNAME',VALUE,envvars) should be used instead of os.environ['VARNAME']  = VALUE
# It calls os.environ AND saves the setting to archive in WKDIR/namelist for repeatability
#
#
# ======================================================================
# Function definition follows, then MAIN program below
# ======================================================================

def setenv (varname,varvalue,env_dict,verbose=0):
   # Not currently used. Needs to be a dictionary to be dumped once file is created
   #
   # Ideally this could be a wrapper to os.environ so any new env vars 
   # automatically get written to the file
   "replaces os.environ to set the variable AND save it to write out in namelist"

   if (verbose > 2 ): print "Saving ",varname," = ",varvalue
   os.environ[varname] = varvalue
   env_dict[varname]   = varvalue
   if ( verbose > 2) : print "Check ",varname," ",env_dict[varname]

def get_var_from_namelist(varname,vartype,vardict,default,verbose=0):
   if (varname in vardict): 
      if verbose > 2: print "get_var_from_namelist found key ",varname," of type ",type(default)," in dict"

      if type(default) == type(True):    #boolean
         var = get_boolean_from_namelist(varname,vardict,default,verbose) 
      elif type(default) == type(0):     #int
         var = get_int_from_namelist(varname,vardict,default,verbose) 
      elif type(default) == type('s'):   #string
         var = vardict['varname']
      else:
         errstr= "get_var_from_namelist cannot deal with vartype ",vartype
         return return_default_from_namelist(varname,default,errstr=errstr,verbose=verbose)

      if verbose > 2: print "VAR from namelist: ",varname," = ",var
      return var

   else:
      errstr = "Did not find varname ",varname," in dict"
      return return_default_from_namelist(varname,default,errstr=errstr,verbose=verbose)


def get_boolean_from_namelist(varname,vardict,default,verbose=0):

   if verbose > 2: print "get_boolean_from_namelist ",varname
   
   try:
      var = eval(vardict[varname])
   except:
      errstr = "Failed to eval() ",varname," = ",vardict[varname]
      return return_default_from_namelist(varname,default,errstr=errstr,verbose=verbose)

   if ( type(var) != type(True) ):
      errstr = "Conversion to boolean erroneously returned type "+type(var)
      return return_default_from_namelist(varname,default,errstr=errstr,verbose=verbose)
   else:
      if verbose > 2: print "SUCCESS: trying for boolean, var ',varname,' is type ",type(var)

   return var


def get_int_from_namelist(varname,vardict,default,verbose=0):

   if verbose > 2: print "get_int_from_namelist ",varname
   
   try:
      var = int(vardict[varname])
   except:
      errstr = "Conversion to int failed, for ",varname," = ",vardict[varname]
      return return_default_from_namelist(varname,default,errstr=errstr,verbose=verbose)

   if ( type(var) != type(0) ):
      errstr = "Conversion to int erroneously returned type "+type(var)
      return return_default_from_namelist(varname,default,errstr=errstr,verbose=verbose)
   else:
      if verbose > 2: print "SUCCESS: trying for intvar ',varname,' is type ",type(var)

   return var

def check_required_dirs(verbose, already_exist =[], create_if_nec = []):
   
   for dir_in in already_exist + create_if_nec : 
      if not dir_in in os.environ:
         print(errstr+" envvar "+dir_in+" not defined")    
         exit()
      dir = os.environ[dir_in]
      if not os.path.exists(dir):
         print "create_if_nec ",create_if_nec
         print "test dir ",dir
         if not dir_in in create_if_nec:
            print(errstr+dir_in+" = "+dir+" directory does not exist")
            exit()
         else:
            print(dir_in+" = "+dir+" created")
            os.makedirs(dir)
      else:
         print(dir_in+" = "+dir)

# ======================================================================
# === MAIN =============================================================
# ======================================================================

print "==== Starting "+__file__


import os
import sys
import glob
import shutil
import subprocess
import timeit
sys.path.insert(0,'var_code/util/')
import read_files
import write_files 



os.system("date")


errstr = "ERROR "+__file__+" : "

# ======================================================================
# default script settings. Can/should be overrided by namelist input
verbose = 1                           # 0 = sparse, 1 = normal, 2 = a lot, 3 = every possible thing
test_mode = False                     # False = run the packages, True = don't make the calls, just say what would be called

# dictionary of all the environment variables set in this script, to be archived in variab_dir/namelist file
envvars = {}   
setenv('CLEAN',"0",envvars)           # default = 0: don't delete old files, 1 = delete them
setenv('make_variab_tar',"1",envvars) # default = 1 : create tar file of results, tar file in wkdir



# ======================================================================
# DIRECTORIES: set up locations
# ======================================================================

# ======================================================================
#  Home directory for diagnostic code (needs to have 'var_code',  sub-directories)
setenv("DIAG_HOME",os.getcwd(),envvars)   # eg. mdtf/MDTF_2.0
setenv("DIAG_ROOT",os.path.dirname(os.environ["DIAG_HOME"]),envvars)

path_var_code_absolute = os.environ["DIAG_HOME"]+'/var_code/util/'

if ( verbose > 1): print "Adding absolute path to modules in "+path_var_code_absolute
sys.path.insert(0,path_var_code_absolute)

# ======================================================================
# inputdata contains model/$casename, obs_data/$package/*  #drb change?
setenv("DATA_IN",os.environ["DIAG_ROOT"]+"/inputdata/",envvars)

# ======================================================================
# output goes into wkdir & variab_dir (diagnostics should generate .nc files & .ps files in subdirectories herein)
setenv("WKDIR",os.getcwd()+"/wkdir",envvars)

check_required_dirs(verbose, create_if_nec = ["WKDIR"])
os.chdir(os.environ["WKDIR"])

# ======================================================================
# Input settings from namelist file (name = argument to this script, default DIAG_HOME/namelist)
# to set CASENAME,model,FIRSTYR,LASTYR, POD list and environment variables 
# Namelist class defined in read_files, contains: case (dict), pod_list (list), envvar (dict)

try:
   namelist_file = read_files.determine_namelist_file(sys.argv,verbose=verbose)
except Exception as error:
   print error
   exit()

# case info (type dict) =  {['casename',casename],['modeltype',model],['startyr',startyr],['endyr',endyr]}
namelist  = read_files.read_text_file(namelist_file,verbose).namelist    

# pod_list (type list) =  [pod_name1,pod_name2,...]
pod_do    = namelist.pod_list   # list of pod names to do here

# Check if any required namelist/envvars are missing  
read_files.check_required_envvar(verbose,["CASENAME","model","FIRSTYR","LASTYR","NCARG_ROOT"])

# update local variables used in this script with env var changes from reading namelist
# variables that are used through os.environ don't need to be assigned here (eg. CLEAN, NCARG_ROOT)
test_mode = get_var_from_namelist('test_mode','bool',namelist.envvar,default=test_mode,verbose=verbose)
verbose   = get_var_from_namelist('verbose','int',namelist.envvar,default=verbose,verbose=verbose)

# ======================================================================
# OUTPUT
# output goes into wkdir & variab_dir (diagnostics should generate .nc files & .ps files in subdirectories herein)
setenv("variab_dir",os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"],envvars)

# ======================================================================
# INPUT: directory of model output
setenv("DATADIR",os.environ["DATA_IN"]+"model/"+os.environ["CASENAME"],envvars)

# ======================================================================

# ======================================================================
# Software 
# ======================================================================
#
# Diagnostic package location and settings
#
# The environment variable DIAG_HOME must be set to run this script
#    It indicates where the variability package source code lives and should
#    contain the directories var_code and obs_data although these can be 
#    located elsewhere by specifying below.
setenv("VARCODE",os.environ["DIAG_HOME"]+"/var_code",envvars)
setenv("VARDATA",os.environ["DATA_IN"]+"obs_data/",envvars)
setenv("RGB",os.environ["VARCODE"]+"/util/rgb",envvars)

# ======================================================================
# set variable names based on model
# ======================================================================
if os.environ["model"] == "CESM":
   import set_variables_CESM        #in var_code/util

if os.environ["model"] == "CMIP":
   import set_variables_CMIP

if os.environ["model"] == "AM4":
   import set_variables_AM4


# ======================================================================
# Check for programs that must exist (eg ncl)
# To Do: make a dictionary 'program name':'ENV VARNAME' and loop like dir_list below
# ======================================================================

ncl_err = os.system("which ncl")
if ncl_err == 0:
   setenv("NCL",subprocess.check_output("which ncl", shell=True),envvars)
   print("using ncl "+os.environ["NCL"])
else:
   print(errstr+ ": ncl not found")
   
# ======================================================================
# Check directories that must already exist
# ======================================================================

check_required_dirs(verbose, already_exist =["DIAG_HOME","VARCODE","VARDATA","NCARG_ROOT"], create_if_nec = ["WKDIR","variab_dir"])



# ======================================================================
# set up html file
# ======================================================================
if os.path.isfile(os.environ["variab_dir"]+"/index.html"):
   print("WARNING: index.html exists, not re-creating.")
else: 
   os.system("cp "+os.environ["VARCODE"]+"/html/mdtf_diag_banner.png "+os.environ["variab_dir"])
   os.system("cp "+os.environ["VARCODE"]+"/html/mdtf1.html "+os.environ["variab_dir"]+"/index.html")


# ======================================================================
# Record settings in file variab_dir/namelist_YYYYMMDDHHRR for rerunning
#====================================================================
write_files.write_namelist(os.environ["variab_dir"],namelist,envvars,verbose=verbose)  


# ======================================================================
# Diagnostics:
# ======================================================================

# Diagnostic logic: call a piece of python code that: 
#   (A) Calls NCL, python (or other languages) to generate plots (PS)
#   (B) Converts plots to png
#   (C) Adds plot links to HTML file

for pod in pod_do:

   if verbose > 0: print("--- MDTF.py Starting POD "+pod+"\n")

   # Find and confirm POD driver script , program (Default = {pod_name,driver}.{program} options)
   # Each pod could have a settings files giving the name of its driver script and long name

   pod_dir = os.environ["VARCODE"]+"/"+pod
   try:
      pod_settings = read_files.read_text_file(pod_dir+"/settings",verbose).pod_settings
   except AssertionError as error:  
      print str(error)
   else:

      run_pod = pod_settings['program']+" "+pod_settings['driver']
      if ('long_name' in pod_settings) and verbose > 0: print "POD long name: ",pod_settings['long_name']

      # Check for files necessary for the pod to run (if pod provides varlist file)

      missing_file_list = read_files.check_varlist(pod_dir,verbose=verbose)
      if ( missing_file_list  ):
         print "WARNING: POD ",pod," Not executed because missing required input files:"
         print missing_file_list
      else:  # all_required_files_found
         if (verbose > 0): print "No known missing required input files"
         if test_mode:
            print("TEST mode: would call :  "+run_pod)
         else:
            start_time = timeit.default_timer()
            try:
               print("Calling :  "+run_pod)
               os.system(run_pod)
            except OSError as e:
               print('ERROR :',e.errno,e.strerror)
               print(errstr + " occured with call: " +run_pod)
            finally:
               elapsed = timeit.default_timer() - start_time
               print(pod+" Elapsed time ",elapsed)

   if verbose > 0: print("---  MDTF.py Finished POD "+pod+"\n")
        
# ==================================================================================================
#  Make tar file
# ==================================================================================================
if ( ( verbose < 1 ) and ( os.environ["make_variab_tar"] == "0" ) ):
   print "Not making tar file because make_variab_tar = ",os.environ["make_variab_tar"]
if ( verbose > 0 ):print "make tar file?",os.environ["make_variab_tar"]
if os.environ["make_variab_tar"] == "1":
   if os.path.isfile( os.environ["variab_dir"]+".tar" ):
      print "Moving existing "+os.environ["variab_dir"]+".tar to "+os.environ["variab_dir"]+".tar_old"
      os.system("mv -f "+os.environ["variab_dir"]+".tar "+os.environ["variab_dir"]+".tar_old")
      os.chdir(os.environ["WKDIR"])

   print "Creating "+os.environ["variab_dir"]+".tar "
   status = os.system("tar --exclude='*netCDF' --exclude='*nc' --exclude='*ps' --exclude='*PS' -cf MDTF_"+os.environ["CASENAME"]+".tar MDTF_"+os.environ["CASENAME"])
   if not status == 0:
      print("ERROR $0")
      print("trying to do:     tar -cf "+os.environ["variab_dir"]+".tar "+os.environ["variab_dir"])
      exit()

print "Exiting normally from ",__file__
exit()
