load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/shea_util.ncl"

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

DIR_in     = getenv("OUTDIR")
DIR_in0    = getenv("OUTDIR")
DIR_in1    = getenv("MONDIR")
DIR_out    = getenv("MONDIR")

vo_var     = getenv("vo_var")
bas_var    = getenv("bas_var")

INDEXs= (/"CCSM4.INDEX_so.fx.nc", "CCSM4.INDEX_vo.fx.nc"/)
ncs0  = "CCSM4.dxdydz_vo.fx.nc"
ncs1  = "CCSM4."+vo_var+".mon.nc"

vo_var = getenv("vo_var")
bas_var = getenv("bas_var")
time_var = getenv("time_var")
lev_var = getenv("lev_var")
lat_var = getenv("lat_var")
lon_var = getenv("lon_var")

;***************************************************************************************************************************
nc  = DIR_in+INDEXs(0)
print("Loading ... "+nc)
fin = addfile(nc,"r") 
vit = fin->$bas_var$
delete(vit@_FillValue)

nc  = DIR_in0+ncs0
print("Loading ... "+nc)
fin = addfile(nc,"r") 
dx = fin->dx
dy = fin->dy
dz = fin->dz
;----------------------------------------------------------------------------------------------------
nc  = DIR_in+INDEXs(1)
print("Loading ... "+nc)
fin = addfile(nc,"r") 
viv = fin->$bas_var$
delete(viv@_FillValue)

nc  = DIR_in1+ncs1
print("Loading ... "+nc)
fin = addfile(nc,"r") 
vo = fin->$vo_var$(0,:,:,:)

;----------------------------------------------------------------------------------------------------
fNames = getfilevarnames(fin)
numf=dimsizes(fNames)

var=fin->$vo_var$(0,0:0,0:0,0:0)
vNames=getVarDimNames(var)
delete(var)

numv=dimsizes(vNames)

nums=numf-numv-1
Names=fNames(0:nums)
Names=""
n=0
do v=0,numf-1
   vvv=fin->$fNames(v)$!0
   if(all( vNames.ne.fNames(v)) .and. fNames(v).ne."vo" .and. vvv.ne."time")then
      Names(n)=fNames(v)
      n=n+1
   end if
end do

;----------------------------------------------------------------------------------------------------
kmt = dimsizes(dz(:,0,0))
jmt = dimsizes(dz(0,:,0))
imt = dimsizes(dz(0,0,:))
kmv = dimsizes(vo(:,0,0))
jmv = dimsizes(vo(0,:,0))
imv = dimsizes(vo(0,0,:))
;----------------------------------------------------------------------------------------------------
viv=where(ismissing(vo),0,viv)

dz =where(vit.eq.2, dz, dz@_FillValue)
vo=where(viv.eq.2,vo,vo@_FillValue)

zzz=vo
zzz=dz(:,0:jmv-1,:)

zzz=where(viv.eq.2,zzz,zzz@_FillValue)
Nt = num(viv.eq.2)
Nv = num(.not.ismissing(vo))
Ns = num(.not.ismissing(zzz))

do j=0,jmv-1
   if(.not.any(viv(:,j,:).eq.2))then
      continue
   end if

   do k=0,kmv-1
      if(.not.any(viv(k,j,:).eq.2))then
         continue
      end if

      do i=0,imv-1
         if(viv(k,j,i).eq.2 .and. vit(k,j,i).ne.2)then
;----------------------------------------------------------------------------------------------------
            ia=i
            ib=i
            ja=j
            jb=j
            d=0 
            do while(all(ismissing(dz(k,ja:jb,ia:ib))))
               d=d+1
               ia=max((/i-d,0/))
               ib=min((/i+d,imt-1/))
               ja=max((/j-d,0/))
               jb=min((/j+d,jmt-1/))
            end do
            zzz(k,j,i)=avg(dz(k,ja:jb,ia:ib))
         end if
      end do ;;; i loop
   end do ;;; k loop 
end do ;;; t loop 

delete(dz)
delete(viv)

zzz@long_name="layer thickness"
zzz@units    ="m"

Nv = num(.not.ismissing(vo))
Ns = num(.not.ismissing(zzz))

if(Nv.ne.Ns)then
   print("ERROR!!! Interpolation failed, PLZ check. "+Nv+" "+Ns)
end if
;----------------------------------------------------------------------------------------------------
;----------------------------------------------------------------------------------------------------
  system("rm "+DIR_out+"CCSM4.dxdydz_vo.fx.nc")
fout = addfile(DIR_out+"CCSM4.dxdydz_vo.fx.nc","c")
;=============================================================================
fout->dx = dx
fout->dy = dy
fout->dz = zzz
do n=0,nums-1
   if(Names(n).ne."")then
      fout->$Names(n)$ = fin->$Names(n)$
   end if
end do

delete(zzz)
delete(vo)
