load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/shea_util.ncl"

begTime = get_cpu_time()

DIR_in0=getenv("OUTDIR")
DIR_out=getenv("OUTDIR")
which=getenv("which_mean")

time_var = getenv("time_var")

setfileoption("nc","Format","LargeFile")

files = systemfunc("ls "+DIR_in0+"CCSM4.vmo_????-????.yr.nc")
f=addfiles(files,"r")
tmt=dimsizes(f[:]->$time_var$)

print("Loading ... "+files)

;print("----------------------------- CCSM4 --------------------------------------")
ListSetType (f, "cat")        ; concatenate (=default)

if(which .eq. "occur_times")then
  vmo= dim_avg_n_Wrap(f[:]->vmo,0)
else
  vmo= dim_sum_n_Wrap(f[:]->vmo,0)
  vmo= vmo/tmt
end if  

vmo@_FillValue=1e20
;printVarSummary(vmo)

fNames = getfilevarnames(f[0])
numf=dimsizes(fNames)
;print(""+fNames)

;print("==============================")
var=f[0]->vmo(0:0,0:1,0:1,0:0)
vNames=getVarDimNames(var)
delete(var)

numv=dimsizes(vNames)
;print(""+vNames)

;print("==============================")
nums=numf-numv-1
Names=fNames(0:nums)
Names=""
n=0
do v=0,numf-1
   vvv=f[0]->$fNames(v)$!0
   if(all( vNames.ne.fNames(v)) .and. fNames(v).ne."vmo" .and. vvv.ne."time")then
      Names(n)=fNames(v)
      n=n+1
   end if
end do   

numo=nums-n
if(numo.ne.0)then
oNames=fNames(0:numo-1)
if(n.eq.0)then
   do v=0,numf-1
      if(all( vNames.ne.fNames(v)) .and. fNames(v).ne."vmo")then
         oNames(n)=fNames(v)
         n=n+1
      end if
   end do   
else   
   do v=0,numf-1
      if( all( vNames.ne.fNames(v)) .and. fNames(v).ne."vmo" .and. all(Names.ne.fNames(v)) )then
         oNames(n)=fNames(v)
         n=n+1
      end if
   end do   
end if
end if

;print("numo="+numo)
;print("Extra Coords:"+Names)
;print("Out variables: "+oNames)

  system("rm "+DIR_out+"CCSM4.vmo.clim.nc")
fout = addfile(DIR_out+"CCSM4.vmo.clim.nc","c")
do n=0,nums-1
   if(Names(n).eq."")then
      break
   end if
;   print(""+Names(n))
   fout->$Names(n)$ = f[0]->$Names(n)$
end do
fout->vmo  = vmo
if(numo.ne.0)then
do n=0,numo-1
   if(oNames(n).eq."")then
      break
   end if
;   print(""+oNames(n))
   if(which .eq. "occur_times")then
      var=dim_avg_n_Wrap(f[:]->$oNames(n)$,0)
   else
      var=dim_sum_n_Wrap(f[:]->$oNames(n)$,0)
      var=var/tmt
   end if
   fout->$oNames(n)$ = var
   delete(var)
end do
end if
