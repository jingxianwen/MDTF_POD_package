


if __name__ == '__main__':
    print 'This program is being run by itself'
else:
    pass

from varlist import check_varlist
import os

# verbose = 0 gives one line for each combo 
#           1 gives names of missing files
#           2 debug
#           3 super debug
verbose = 1


# diagnostic True  just list the requested files
#            False send error messages if they're not found
diagnostic = False
#diagnostic = True

package_name_all = ["MJO_suite",
                    "EOF_500hPa",
                    "precip_diurnal_cycle",
                    "MJO_teleconnection",
                    "convective_transition_diag"]
#                   "MJO_diag" not in yet because of complicated directory structure

#package_name_all = ["EOF_500hPa"]
#casename_all = ["QBOi.EXP1.AMIP.001","CCSM4"]
casename_all = ["f.e20.F2000.f09_f09.cesm2_1_alpha01d"]
#casename_all = ["b.e21.BHIST.f09_g17.CMIP6-historical.003"]

#varnames_all = ["CESM","CMIP"]
varnames_all = ["CESM"]
basedir =  "/glade/u/home/bundy/mdtf/MDTF_20180920"

print "========================================== "
if verbose > 1:
    print "Running in DEBUG mode. To reduce output, set verbose = 0 or 1"

if verbose > 0 and diagnostic:
    print "Running in diagnostic mode to tell what variables are needed at which frequencies."
    print "To check for existing files, set diagnostic = False"

if verbose > 0:
    print "========================================== "

for package_name in package_name_all:
    for casename in casename_all:
        for varname in varnames_all:

            if varname == "CESM":
                import set_variables_CESM        #in var_code/util
            elif varname == "CMIP":
                import set_variables_CMIP
            else:
                print "ERROR in "+__file__+", varname "+varname+" not recognized"

            if verbose > 1:
                print "Calling check_varlist for package",package_name
                
            test = check_varlist(package_name = package_name, 
                                 casename = casename,
                                 basedir = basedir,
                                 stop_on_missing_required = False,
                                 diagnostic = diagnostic, 
                                 verbose = verbose  )

            all_found = test[0]
            error_message = test[1]

            if ( diagnostic ):
                mystring1 = " "
            else:
                if ( all_found ):
                    mystring1 = "---PASS: "+package_name+" case "+casename+" "+varname+" "+error_message+"\n"
                else:
                    mystring1 = "---FAIL: "+package_name+" case "+casename+" "+varname+" "+error_message+"\n"

            print mystring1


