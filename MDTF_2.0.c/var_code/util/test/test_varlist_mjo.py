
from varlist import check_varlist
import os

# verbose = 0 gives one line for each combo 
#           1 gives names of missing files
#           2 debug
verbose = 1


# diagnostic True  list the requested files (for example to make a model run)
#            False return errors if requested files are not found
diagnostic = False
#diagnostic = True

#package_name_all = ["MJO_suite"]
package_name_all = ["EOF_500hPa",\
                    "Wheeler_Kiladis",\
                    "precip_diurnal_cycle",\
                    "convective_transition_diag",\
                    "fortran_example",\
                    "MJO_suite",\
                    "MJO_telecon_diag",\
                    "MSE_diag_COMPOSITE",\
                    "MSE_diag_MSE",\
                    "MSE_diag_MSE_VAR",\
                    "transport_onto_TS"]


#casename_all = ["QBOi.EXP1.AMIP.001","CCSM4"]
casename_all = ["f.e20.F2000.f09_f09.cesm2_1_alpha01d"]
#casename_all = ["b.e21.BHIST.f09_g17.CMIP6-historical.003"]

#varnames_all = ["CESM","CMIP"]
varnames_all = ["CESM"]
basedir =  "/glade/u/home/bundy/mdtf/MDTF_20180920"

print "=========================================="



for package_name in package_name_all:
    for casename in casename_all:
        for varname in varnames_all:

            if varname == "CESM":
                import set_variables_CESM        #in var_code/util
            elif varname == "CMIP":
                import set_variables_CMIP
            else:
                print "ERROR in "+__file__+", varname "+varname+" not recognized"

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


