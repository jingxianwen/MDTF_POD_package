# INCOMPLETE!

import os
import set_variables_CESM        #in var_code/util
from varlist import check_varlist


mdtf_dir = "/glade/u/home/bundy/mdtf/MDTF_20180920"  
casename = "f.e20.F2000.f09_f09.cesm2_1_alpha01d"
arch_dir = "/glade/scratch/bundy/archive/"+casename+"/atm/proc/tseries"

print "=========================================="

dirs_in = os.listdir(arch_dir)
print "found dirs ",dirs_in
#found dirs  ['hour_1', 'hour_3', 'month_1', 'day_1']

#dict = {'Name': 'Zara', 'Age': 7, 'Class': 'First'}
#print "dict['Name']: ", dict['Name']
#print "dict['Age']: ", dict['Age']
dict = {'hour_1': '1hr', 'hour_3': '3hr', 'day_1': 'day', 'montht_1': 'mon'}

#eg. day/f.e20.F2000.f09_f09.cesm2_1_alpha01d.PRECT.day.nc
for dir_in in dirs_in:
    print "dir_in ",dir_in
    file_list = os.listdir(os.path.join(arch_dir,dir_in))
    file = file_list[1]
    print(file)

#ln -s /glade/scratch/bundy/archive/f.e20.F2000.f09_f09.cesm2_1_alpha01d/atm/proc/tseries/day_1/f.e20.F2000.f09_f09.cesm2_1_alpha01d.cam.h2.$var.00010101-00051231.nc f.e20.F2000.f09_f09.cesm2_1_alpha01d.$var.day.nc

    
