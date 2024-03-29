load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/shea_util.ncl"

begTime = get_cpu_time()

DIR_in0 = getenv("OUTDIR")
DIR_out = getenv("OUTDIR")
which=getenv("which_mean")

time_var = getenv("time_var")

nc=DIR_in0+"CCSM4.vmo_185001-186012.mon.nc"

print("Loading ... "+nc)

f=addfile(nc,"r")
vmo= f->vmo
replace_ieeenan (vmo, vmo@_FillValue, 0)

;----------------------------------------------------------------------------------------------------
fNames = getfilevarnames(f)
numf=dimsizes(fNames)

var=f->vmo(0:0,0:1,0:1,0:1)
vNames=getVarDimNames(var)
delete(var)

numv=dimsizes(vNames)

nums=numf-numv-1
Names=fNames(0:nums)
Names=""
n=0
do v=0,numf-1
   vvv=f->$fNames(v)$!0
   if(all( vNames.ne.fNames(v)) .and. fNames(v).ne."vmo" .and. vvv.ne."time")then
      Names(n)=fNames(v)
      n=n+1
   end if
end do

;----------------------------------------------------------------------------------------------------

time=f->$time_var$
if("CCSM4".eq."FGOALS-s2")then
   time@units = "days since 1850-01-01 00:00:00"
end if
time=(/cd_convert(time,"days since 1850-01-01 00:00")/)
time@units="days since 1850-01-01 00:00"
time@calendar="standard"
num_time=dimsizes(time)
num_year=max((/num_time/12,1/))

;============================================================================= yearly
tmp=vmo(0:num_year-1,:,:,:)
tim0=time(0:num_year-1)
do y=0,num_year-1
   ta=y*12
   tb=(y+1)*12-1
   tb=min((/tb,num_time-1/))
   tim0(y)=(/avg(time(ta:tb))/)
   if(which .eq. "occur_times")then
      tmp(y,:,:,:) =(/dim_avg_n_Wrap(vmo(ta:tb,:,:,:),0)/)
   else
     tmp(y,:,:,:) =dim_sum_n_Wrap(vmo(ta:tb,:,:,:),0)/(tb-ta+1)
   end if
end do
tmp&time = tim0

  system("rm "+DIR_out+"CCSM4.vmo_1850-1860.yr.nc")
fout = addfile(DIR_out+"CCSM4.vmo_1850-1860.yr.nc","c")
do n=0,nums-1
   if(Names(n).eq."")then
      break
   end if
   fout->$Names(n)$ = f->$Names(n)$
end do
fout->vmo  = tmp
