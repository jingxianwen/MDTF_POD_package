import os

os.environ["lat_coord"] = "lat"
os.environ["lon_coord"] = "lon"   
os.environ["lev_coord"] = "pfull" # or "pfull" # must be on pressure levels (hPa)
os.environ["time_coord"] = "time"   
os.environ["lat_var"] = "lat"   
os.environ["lon_var"] = "lon"
os.environ["time_var"] = "time"
os.environ["ps_var"] = "PS"
os.environ["pr_conversion_factor"] = "1" #units = m/s
os.environ["prc_conversion_factor"] = "1" #units = m/s
os.environ["prls_conversion_factor"] = "1" #units = m/s

# ------------------------------------------------------------------------
# Variables for Convective Transition Diagnostics module:
os.environ["ta_var"] = "ta" # 3D temperature, units = K   
os.environ["prw_var"] = "prw" # Column Water Vapor (precipitable water vapor), units = mm (or kg/m^2)
os.environ["tave_var"] = "tave" # Mass-Weighted Column Average Tropospheric Temperature, units = K
os.environ["qsat_int_var"] = "qsat_int" # Vertically-Integrated Saturation Specific Humidity, units = mm (or kg/m^2)
# End - Variables for Convective Transition Diagnostics package
# ------------------------------------------------------------------------

# ------------------------------------------------------------------------
#coordinate of subcolumn 
os.environ["subcol_coord"] = "subcol"   

# Variables for CFODD warm rain microphysics Diagnostics module:
os.environ["dtau_s_var"] = "dtau_s" # optical depth profile of stratiform clouds (input for COSP)
os.environ["cldtop_reff_var"] = "cldtop_reff" # cloud top droplet effective radius (m)
os.environ["cld_reff_var"] = "cld_reff" # cloud top droplet effective radius (m)
os.environ["reff_conversion_factor"] = "1.0e+6" # reff need be in micron

os.environ["liq_wat_var"] = "liq_wat" # cloud liquid water mixing ratio (kg/kg)
os.environ["ice_wat_var"] = "ice_wat" # cloud liquid water mixing ratio (kg/kg)
os.environ["temp_var"] = "temp" # cloud liquid water mixing ratio (kg/kg)

# subcolumn outputs from COSP:
#os.environ["NSCOL"] = "25"    # number of subcolumns in a gridbox used in COSP
os.environ["time_freq"] = "6hr" # number of subcolumns in a gridbox used in COSP
os.environ["dbze_var"] = "dbze94" # subcolumn CloudSat radar reflectivity from COSP - remove subcolumn number
os.environ["cloud_type_var"] = "cldtype" # subcolumn cloud type from COSP - remove subcolumn number

# End - Variables for CFODD warm rain microphysics Diagnostics package
# ------------------------------------------------------------------------

