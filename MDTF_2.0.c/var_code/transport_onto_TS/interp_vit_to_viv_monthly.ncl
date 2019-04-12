load "$NCARG_ROOT/lib/ncarg/nclscripts/contrib/calendar_decode2.ncl"
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

DIR_in     = getenv("OUTDIR")
DIR_in1    = getenv("MONDIR")
DIR_in2    = getenv("OUTDIR")
DIR_out    = getenv("OUTDIR")
STAYR      = stringtointeger(getenv("STAYR"))
ENDYR      = stringtointeger(getenv("ENDYR"))

thetao_var = getenv("thetao_var")
so_var = getenv("so_var")
vmo_var = getenv("vmo_var")
bas_var = getenv("bas_var")
time_var = getenv("time_var")

INDEXs= (/"CCSM4.INDEX_so.fx.nc", "CCSM4.INDEX_vo.fx.nc"/)
ncs1  = (/"CCSM4."+thetao_var+".mon.nc", "CCSM4."+so_var+".mon.nc"/)
ncs2  = "CCSM4.vmo_185001-186012.mon.nc"

;----------------------------------STAYR--------------------------------------ENDYR------------------               
;-----------------------yyyy0------yyyy0------yyyy0-----------------yyyy1-----yyyy1-----yyyy1--------               
; Time starts from:       +          0          0                    end       end       -                 

nc  = DIR_in1+ncs1(0)
print("Loading ... "+nc)
fin0 = addfile(nc,"r") 

time=fin0->$time_var$
tmt=dimsizes(time)
ymt=tmt/12

years=tointeger(floor(cd_calendar(time,4)))
yyyy0=years(0)
yyyy1=years(tmt-1)

nc  = DIR_in1+ncs1(1)
print("Loading ... "+nc)
fin1= addfile(nc,"r") 

nc  = DIR_in2+ncs2
print("Loading ... "+nc)
fin2 = addfile(nc,"r") 

nc  = DIR_in+INDEXs(0)
print("Loading ... "+INDEXs(0))
fina= addfile(nc,"r") 

nc  = DIR_in+INDEXs(1)
print("Loading ... "+INDEXs(1))
finb= addfile(nc,"r") 

;***************************************************************************************************************************
do y=0,ymt-1
  year=yyyy0+y
  yyyymm=year+"01-"+year+"12"
  print("Processing ... "+yyyymm)
  ta=y*12
  tb=ta+11

  thetao = fin0->$thetao_var$(ta:tb,:,:,:)
  if(max(thetao(0,0:1,:,:)).gt.100)then
     thetao= thetao - 273.15
  end if

  so = fin1->$so_var$(ta:tb,:,:,:)
  if(max(so(0,0:1,:,:)).lt.10)then
     so= so * 1000.
  end if

  vmo = fin2->$vmo_var$(0:11,:,:,:)

;----------------------------------------------------------------------------------------------------
fNames = getfilevarnames(fin2)
numf=dimsizes(fNames)
;print(""+fNames)

;print("==============================")
var=fin2->$vmo_var$(0:0,0:0,0:0,0:0)
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
   vvv=fin2->$fNames(v)$!0
   if(all( vNames.ne.fNames(v)) .and. fNames(v).ne."vmo" .and. vvv.ne."time")then
      Names(n)=fNames(v)
      n=n+1
   end if
end do

;print(""+Names)
  

;print("==================== Data Loading OK ====================")
;----------------------------------------------------------------------------------------------------
  tmt = dimsizes(thetao(:,0,0,0))
  kmt = dimsizes(thetao(0,:,0,0))
  jmt = dimsizes(thetao(0,0,:,0))
  imt = dimsizes(thetao(0,0,0,:))
  tmv = dimsizes(   vmo(:,0,0,0))
  kmv = dimsizes(   vmo(0,:,0,0))
  jmv = dimsizes(   vmo(0,0,:,0))
  imv = dimsizes(   vmo(0,0,0,:))
  if(tmt.ne.tmv)then
     print("ERROR!!! time dimention differs, PLZ check.")
     exit
  end if

;----------------------------------------------------------------------------------------------------
     eps = 1e-6
   trans = new((/tmv,170,150,jmt/),  "float", 1e20)
     sit = new((/tmv,170,150,jmt/),"integer",-9999)
   trans = 0
    sit  = 0

;print("==================== BASIN Setting OK ====================")

ttt=vmo
sss=vmo

ttt=(/thetao(:,:,0:jmv-1,:)/)
sss=(/    so(:,:,0:jmv-1,:)/)

do t=0,tmv-1
   vit = fina->$bas_var$
   delete(vit@_FillValue)
   viv = finb->$bas_var$
   delete(viv@_FillValue)

   viv=where(ismissing(vmo(t,:,:,:)),0,viv)
   vit=where(ismissing( so(t,:,:,:)),0,vit)

   ttt(t,:,:,:)=where(viv.eq.2,ttt(t,:,:,:),ttt@_FillValue)
   sss(t,:,:,:)=where(viv.eq.2,sss(t,:,:,:),sss@_FillValue)

   vmo(t,:,:,:)=where(viv.eq.2,vmo(t,:,:,:),vmo@_FillValue)
   Nv = num(.not.ismissing(vmo(t,:,:,:)))

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
            do while(all(ismissing(thetao(t,k,ja:jb,ia:ib))))
               d=d+1
               ia=max((/i-d,0/))
               ib=min((/i+d,imt-1/))
               ja=max((/j-d,0/))
               jb=min((/j+d,jmt-1/))
;               print(ia+" "+ib+" "+imt)
            end do
            ttt(t,k,j,i)=avg(thetao(t,k,ja:jb,ia:ib))
            sss(t,k,j,i)=avg(    so(t,k,ja:jb,ia:ib))
         end if
         if(viv(k,j,i).ne.2 .and. vit(k,j,i).eq.2)then
            ttt(t,k,j,i)=ttt@_FillValue
            sss(t,k,j,i)=ttt@_FillValue
         end if
      end do ;;; i loop
   end do ;;; k loop 
end do ;;; j loop 
   delete(   vit)
   delete(   viv)

   Ns = num(.not.ismissing(sss(t,:,:,:)))
   if(Nv.ne.Ns)then
      print("ERROR!!! Interpolation failed, PLZ check. "+Nv+" "+Ns)
;   else   
;      print(Nv+" "+Ns)
   end if
end do ;;; t loop 

delete(thetao)
delete(    so)
delete(vmo)

;ttt=where(viv.eq.2,ttt,ttt@_FillValue)
;sss=where(viv.eq.2,sss,sss@_FillValue)

ttt@long_name="Temperature"
sss@long_name="Salinity"
ttt@units    ="DegC"
sss@units    ="psu"

;----------------------------------------------------------------------------------------------------
    system("rm "+DIR_out+"CCSM4."+thetao_var+"_viv_"+yyyymm+".mon.nc")
  fout = addfile(DIR_out+"CCSM4."+thetao_var+"_viv_"+yyyymm+".mon.nc","c")
  ;=============================================================================
do n=0,nums-1
;   print(""+Names(n))
   if(Names(n).ne."")then
     fout->$Names(n)$ = fin2->$Names(n)$
   end if
end do
  fout->$thetao_var$ = ttt

    system("rm "+DIR_out+"CCSM4."+so_var+"_viv_"+yyyymm+".mon.nc")
  fout = addfile(DIR_out+"CCSM4."+so_var+"_viv_"+yyyymm+".mon.nc","c")
  ;=============================================================================
do n=0,nums-1
;   print(""+Names(n))
   if(Names(n).ne."")then
     fout->$Names(n)$ = fin2->$Names(n)$
   end if
end do
  fout->$so_var$ = sss

delete(sss)
delete(ttt)

end do ;;; year loop
