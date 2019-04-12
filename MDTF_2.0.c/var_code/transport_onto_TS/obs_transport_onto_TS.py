import os
import glob
from post_process import convert_pdf2png_obs
from post_process import execute_ncl_calculate

if len(glob.glob(os.environ["REFDIR"]+"*.png"))==18:
   print("Figures of reference exists. Copy them to "+os.environ["PNGREF"])
   os.system("\cp "+os.environ["REFDIR"]+"*.png "+os.environ["PNGREF"])   
   exit()
else:  
   print("Ploting Figures of reference ...")

# 26.5
script=os.environ["SRCDIR"]+"obs_Q_lat0_z_plot.ncl"
execute_ncl_calculate(script)

script=os.environ["SRCDIR"]+"obs_thetao_lat0_climate_xz_plot.ncl"
execute_ncl_calculate(script)

script=os.environ["SRCDIR"]+"obs_T_lat0_z_plot.ncl"
execute_ncl_calculate(script)

script=os.environ["SRCDIR"]+"obs_so_lat0_climate_xz_plot.ncl"
execute_ncl_calculate(script)

script=os.environ["SRCDIR"]+"obs_S_lat0_z_plot.ncl"
execute_ncl_calculate(script)

script=os.environ["SRCDIR"]+"ref_trans_lat0_climate_TS_plot.ncl"
execute_ncl_calculate(script)

script=os.environ["SRCDIR"]+"ref_AMOCr_r_plot.ncl"
execute_ncl_calculate(script)

script=os.environ["SRCDIR"]+"ref_AMOCT_T_plot.ncl"
execute_ncl_calculate(script)

script=os.environ["SRCDIR"]+"ref_AMOCS_S_plot.ncl"
execute_ncl_calculate(script)

# along latitudes

script=os.environ["SRCDIR"]+"ref_Qavg_lats_y_plot.ncl"
execute_ncl_calculate(script)

script=os.environ["SRCDIR"]+"ref_Twgt_lats_y_plot.ncl"
execute_ncl_calculate(script)

script=os.environ["SRCDIR"]+"ref_Swgt_lats_y_plot.ncl"
execute_ncl_calculate(script)

script=os.environ["SRCDIR"]+"ref_AMOCz_yz_plot.ncl"
execute_ncl_calculate(script)

script=os.environ["SRCDIR"]+"ref_AMOCr_yr_plot.ncl"
execute_ncl_calculate(script)

script=os.environ["SRCDIR"]+"ref_AMOCT_yT_plot.ncl"
execute_ncl_calculate(script)

script=os.environ["SRCDIR"]+"ref_AMOCS_yS_plot.ncl"
execute_ncl_calculate(script)

script=os.environ["SRCDIR"]+"ref_MHT_lats_y_plot.ncl"
execute_ncl_calculate(script)

script=os.environ["SRCDIR"]+"ref_MFWT_lats_y_plot.ncl"
execute_ncl_calculate(script)

#============================================================
# convert pdf to png
#============================================================
convert_pdf2png_obs()


print("**************************************************")
print("obs_transport_onto_TS Package (obs_transport_onto_TS.py) Executed!")
print("**************************************************")
